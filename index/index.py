from urllib import request
from bs4 import BeautifulSoup
import json

class Index():

    def __init__(
        self
        ,import_data_path : str
        ,export_index_path : str
        ,timeout : int
        ,export_stat_path : str
        ,print_progress = False
        ) -> None:
        self.url_list = self.__import_data(data_path = import_data_path)
        self.count_documents = len(self.url_list)
        self.count_tokens = 0
        self.count_errors = 0
        self.index = {}
        self.__tokenize_title(timeout = timeout, print_progress = print_progress)

        self.__export_index_data(folder_path=export_index_path)
        self.__export_meta_data(folder_path=export_stat_path)

    def __tokenize_title(self, timeout : int, print_progress = False):
        for i in range(self.count_documents):
            if print_progress:
                print(f"Document actuellement indexé : {i + 1}/{self.count_documents}")
            try:
                url = self.url_list[i]
                html = request.urlopen(url, timeout= timeout).read().decode('utf8')
                html[:60]
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.find('title')

                title_token = title.string.split(sep=' ')
                self.count_tokens += len(title_token)
                for token in title_token:
                    if token in self.index:
                        self.index[token].append(i)
                    else :
                        self.index[token] = [i]
            except Exception as e:
                self.count_errors += 1 

    def __import_data(self, data_path : str):
        file = open(data_path)
        return(json.load(file))

    def __export_index_data(self, folder_path : str):
        with open(folder_path, 'w+') as outfile:
            for token in self.index:
                outfile.write(f'"{token}" : ')
                for url in set(self.index[token]):
                    outfile.write(f'{url}:{self.index[token].count(url)},')
                outfile.write("\n")
            outfile.close()

    def __str__(self):
        return f"--- STATISTIQUES ---\nNombre de documents : {self.count_documents}\nNombre d'erreurs lors de l'indexage : {self.count_errors}\nNombre de tokens : {self.count_tokens}"

    def __export_meta_data(self, folder_path : str):
        with open(folder_path, 'w+') as outfile:
            metadata = {"Nombre de sites indexes" : self.count_documents
            ,"Nombre de tokens totaux" : self.count_tokens
            ,"Nombre de tokens distincts" : len(self.index.keys())
            ,"Nombre d\'erreurs lors de l\'indexation" : self.count_errors}
            json.dump(metadata,outfile)
            outfile.close()
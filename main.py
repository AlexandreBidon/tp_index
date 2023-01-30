from index.index import Index
import click


@click.command()
@click.option('--import_data_path', default="raw_data/crawled_urls.json", help='The path of the URL to index.')
@click.option('--export_index_path',  default= "title.non_pos_index.json")
@click.option('--export_stat_path',  default= "metadata.json")
@click.option('--timeout',  default= 3)
@click.option('--print_progress',  default= False)
def run_index(import_data_path
            ,export_index_path
            ,export_stat_path
            ,timeout
            ,print_progress):
    Index(
        import_data_path=import_data_path
        ,export_index_path=export_index_path
        ,export_stat_path=export_stat_path
        ,timeout=timeout
        ,print_progress= print_progress)

if __name__ == "__main__":
    run_index()


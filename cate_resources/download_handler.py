from cate_resources.cate import CateScraperClient 
import os
import requests

class DownloadHandler(CateScraperClient):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_year_directory(curr_year):
        try:
            os.mkdir(f'../Year-{curr_year}/')
            return
        except FileExistsError:
            return

    def create_term_directory(self, curr_year):
        try:
            os.mkdir(f'../Year-{curr_year}/Term-{self.curr_period // 2 + 1}/')
            return
        except FileExistsError:
            return

    def create_modules_directories(self):
        for key, _ in self.modules_all_specs.items():
            try:
                os.mkdir(f'../Year-{self.current_year[1]}/Term-{self.curr_period // 2 + 1}/{key}/')
            except FileExistsError:
                continue

    def create_file_structure(self):
        self.create_year_directory(self.current_year[1])
        self.create_term_directory(self.current_year[1])
        self.create_modules_directories()

    def download_specs(self):
        self.create_file_structure()
        for key, values in self.modules_all_specs.items():
            curr_path = f'../Year-{self.current_year[1]}/Term-{self.curr_period // 2 + 1}/{key}'
            for val in values:
                if os.listdir(curr_path).__contains__(val[1]):
                    continue
                else:
                    response = requests.get(val[0], auth=self._authentication)
                    if response.ok:
                        with open(f'{curr_path}/{val[1]}.pdf', 'wb') as file:
                            file.write(response.content)

    # implement the latest spec function using the deadlines in the self.deadlines field
    def download_latest_spec(self):
        self.create_file_structure()
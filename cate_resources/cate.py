import re
from credentials import USERNAME, PASSWORD, CURRENT_CLASS
from cate_resources.scraper_init import InitialisationScrapeCient
import requests
from bs4 import BeautifulSoup
import bs4.element
from datetime import datetime
from functools import reduce


class CateScraperClient(InitialisationScrapeCient):
    def __init__(self):
        super().__init__()

    """function to change the self.modules_all_specs dictionary, for each module in the current period and year a list 
    of urls to link and download using download_spec(self, spec_url) method"""

    def get_all_specs(self, table_complete):
        row_nums_modules = list(self.modules_positions_names_dict.values())
        rows_table = table_complete.find_all('tr')
        module_name_index = 0
        for row_num in row_nums_modules:
            self.modules_all_specs[self.module_names.__getitem__(module_name_index)] = []
            spec_urls = []
            for i in range(0, 3):
                curr_row = rows_table.__getitem__(row_num + i)
                curr_row_data = curr_row.find_all('td')
                for data in curr_row_data:
                    try:
                        if data.attrs['bgcolor'] == '#ccffcc' or data.attrs['bgcolor'] == '#cdcdcd' \
                                or data.attrs['bgcolor'] == '#f0ccf0':
                            spec_url = 'https://cate.doc.ic.ac.uk/' + data.find('a').attrs['href']
                            if spec_url.__contains__('mailto:') or spec_url.__contains__('given.'):
                                continue
                            spec_name = str(data.find('a').contents[0]).strip('\t\n')
                            spec_urls.append((spec_url, spec_name))
                        elif data.attrs['bgcolor'] == 'white' and int(data.attrs['colspan']) > 0:
                            spec_url = 'https://cate.doc.ic.ac.uk/' + data.find('a').attrs['href']
                            if spec_url.__contains__('mailto:') or spec_url.__contains__('given.'):
                                continue
                            spec_name = str(data.find('a').contents[0]).strip('\t\n')
                            spec_urls.append((spec_url, spec_name))
                    except KeyError:
                        continue
            self.modules_all_specs[self.module_names.__getitem__(module_name_index)] = spec_urls
            module_name_index += 1

    def get_deadline_for_specs(self, table_main):
        # TODO
        pass

    @staticmethod
    def get_module_name_from_html_text(html_text):
        name = re.split(r'[-:]', html_text)[1][1::].split(' ')
        mod_name = reduce(lambda x, y: x + '-' + y, name)
        return mod_name

    def get_timetable_whole(self) -> bs4.element.Tag:
        page_content = requests.get(self.resource_url, auth=self._authentication).content
        parsed_content = BeautifulSoup(page_content, 'html.parser')
        tables = parsed_content.find_all('table')
        table_main = tables[0]
        for table in tables:
            if len(table.find_all('tr')) > len(table_main.find_all('tr')):
                table_main = table
        return table_main

    def module_row_nums_dict_update(self, table_modules: bs4.element.Tag):
        table_rows = table_modules.find_all('tr')
        counter = 0
        for row in table_rows:
            row_data = row.find_all('td')
            for data in row_data:
                try:
                    if data.attrs['style'] == f'border: 2px solid blue':
                        text_bold = data.find('b').text
                        module_name = self.get_module_name_from_html_text(text_bold)
                        self.modules_positions_names_dict[module_name] = counter
                        self.module_names.append(module_name)
                except KeyError:
                    continue
            counter += 1

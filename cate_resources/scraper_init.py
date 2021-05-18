from credentials import USERNAME, PASSWORD, CURRENT_CLASS
from datetime import datetime

class ClientAuthentication:
    """Class to instantiate the credentials and authenticate the requests.get() call"""
    def __init__(self):
        self.auth = (USERNAME, PASSWORD)
        self.curr_class = CURRENT_CLASS


class InitialisationScrapeCient:
    def __init__(self):
        client_auth = ClientAuthentication().auth
        self._authentication = ClientAuthentication().auth
        self.current_year = ClientAuthentication().curr_class
        # TODO: Find a way to update the period.
        self.curr_period = 1
        self.modules_positions_names_dict = {}
        self.module_names = []
        self.latest_assignment_deadline = {}
        self.modules_all_specs = {}
        self.all_module_deadlines = {}
        # TODO: Make an internal function to assign initial resource url.
        self.resource_url = f'https://cate.doc.ic.ac.uk/timetable.cgi?' \
                            f'&keyt={datetime.today().year if datetime.today().month >= 10 else datetime.today().year - 1}' \
                            f':{self.curr_period}:{self.current_year}:{self._authentication[0]}'
    
    def _init_positions_names_dict(self):
        for name in self.module_names:
            self.modules_positions_names_dict[name] = []

    def _init_all_modules_deadlines(self):
        for name in self.module_names:
            self.all_module_deadlines[name] = []

    def clear_all_fields_scraper(self):
        resource_url = self.resource_url
        curr_period = self.curr_period
        self.__init__()
        self._init_all_modules_deadlines()
        self._init_positions_names_dict()
        self.resource_url = resource_url
        self.curr_period = curr_period

    def update__resource_url(self):
        self.curr_period += 2
        self.resource_url = f'https://cate.doc.ic.ac.uk/timetable.cgi?' \
                            f'&keyt={datetime.today().year if datetime.today().month >= 10 else datetime.today().year - 1}' \
                            f':{self.curr_period}:{self.current_year}:{self._authentication[0]}'
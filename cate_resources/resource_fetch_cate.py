from cate_resources.download_handler import DownloadHandler


def main():
    scraper = DownloadHandler()
    for i in range(0, 3):
        timetable_contents = scraper.get_timetable_whole()
        scraper.module_row_nums_dict_update(timetable_contents)
        scraper.get_all_specs(timetable_contents)
        scraper.download_specs()
        scraper.update__resource_url()
        scraper.clear_all_fields_scraper()


if __name__ == "__main__":
    main()
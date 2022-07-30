from abc import abstractmethod
from datetime import date, datetime

import pandas as pd


class Parser:
    def __init__(self, job_title, location, days, keywords):
        self.website_name = ""
        self.job_title = job_title
        self.location = location
        self.range = int(days)
        self.keywords = keywords
        self.JOBS_PER_PAGE = 0
        self.COLUMN_INDEX = ['A', 'B', 'C', 'D', 'E', 'F']
        self.COLUMNS = ['Job Title', 'Company', 'Location', 'Relevant Keyword', 'Job Link']

        self.extracted_data = []
        self.titles = []
        self.companies = []
        self.locations = []
        self.links = []
        self.relevant_keyword = []

    @abstractmethod
    def parse_job_title(self, job):
        pass

    @abstractmethod
    def parse_job_company(self, job):
        pass

    @abstractmethod
    def parse_job_link(self, job):
        pass

    @abstractmethod
    def parse_job_location(self, job):
        pass

    def is_relevant(self, job_description):
        if job_description == "":
            print("I am empty!")
        job_description = job_description.split()
        for keyword in self.keywords:
            if keyword in job_description:
                return keyword
        return ""

    def add_job(self, job, keyword):
        self.titles.append(self.parse_job_title(job))
        self.companies.append(self.parse_job_company(job))
        self.links.append(self.parse_job_link(job))
        self.locations.append(self.parse_job_location(job))
        self.relevant_keyword.append(keyword)

    def create_table(self):
        """
        Adds of the relevant jobs into an xlsx sheet.
        After all of the data is added, format the table and turn links to "clickable"
        The xlsx will be saved in the directory of the crawler
        :return: xlsx with all of the relevant jobs
        """

        self.extracted_data.append(self.titles)
        self.extracted_data.append(self.companies)
        self.extracted_data.append(self.locations)
        self.extracted_data.append(self.relevant_keyword)
        self.extracted_data.append(self.links)

        jobs_list = {}

        print(self.website_name + " - Done parsing, formatting data to xlsx...")
        for i in range(len(self.COLUMNS)):
            jobs_list[self.COLUMNS[i]] = self.extracted_data[i]

        df = pd.DataFrame(jobs_list)

        writer = pd.ExcelWriter('results-' +
                                self.website_name.lower() + "-" +
                                self.job_title.replace(" ", "-").lower() + '-' +
                                str(date.today()).replace(" ", "-") + '.xlsx')
        df.to_excel(writer, sheet_name=self.website_name + ' Jobs', index=False, na_rep='NaN')

        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_index = df.columns.get_loc(column)
            if self.COLUMNS[col_index] == 'Job Link':
                writer.sheets[self.website_name + ' Jobs'].set_column(col_index, col_index, column_width)
            else:
                writer.sheets[self.website_name + ' Jobs'].set_column(col_index, col_index, column_width + 5)

        writer.save()

        print(self.website_name + " - Done! Results saved into results-" +
              self.website_name.lower() + "-" +
              self.job_title.replace(" ", "-").lower() + '-' +
              str(date.today()).replace(" ", "-") + ".xlsx")

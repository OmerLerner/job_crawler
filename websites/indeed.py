import math

import requests
from bs4 import BeautifulSoup

from websites.parser import Parser


class indeed_Parser(Parser):
    def __init__(self, job_title, location, range, keywords):
        super().__init__(job_title, location, range, keywords)
        self.website_name = "Indeed"
        self.JOBS_PER_PAGE = 15

    def parse_page_count(self, element):
        pages_element = element.text.split()
        return math.ceil(int(pages_element[3]) / self.JOBS_PER_PAGE)

    def parse_job_title(self, element):
        try:
            title_element = element.find('h2', class_='jobTitle')
            title = title_element.text.strip()
        except:
            title = ""
        return title

    def parse_job_company(self, element):
        try:
            company_element = element.find('span', class_='companyName')
            company = company_element.text.strip()
        except:
            company = ""
        return company

    def parse_job_location(self, element):
        try:
            location_element = element.find(class_='companyLocation')
            location = location_element.text.strip()
        except:
            location = ""
        return location

    def parse_job_link(self, element):
        try:
            link_element = element.find('a')['href']
            link = 'https://il.indeed.com' + link_element
        except:
            link = ''
        return link

    def is_relevant(self, job_url):
        page = requests.get(job_url)
        soup = BeautifulSoup(page.content, "html.parser")

        key = ""
        for keyword in self.keywords:
            if keyword in soup.text.lower():
                return keyword

        return key

    def load_jobs(self, page_number):
        """
        Sends a get request, parses page and returns all of the job postings on current page
        :param page_number: Int - current page number to load
        :return: Page containing all jobs
        """
        url = ('https://il.indeed.com/jobs?q='
               + self.job_title +
               '&l=' + self.location +
               '&fromage=' + str(self.range) +
               '&sort=date'
               '&start=' + str(page_number))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        job_soup = soup.find(id="resultsCol")
        pages_element = soup.find(id='searchCountPages')
        return job_soup, self.parse_page_count(pages_element)

    # Indeed has 15 posting per page
    def extract_jobs(self):

        page_number = 0

        job_soup, page_count = self.load_jobs(page_number)
        jobs_list = job_soup.find_all('div', class_='cardOutline')

        print("Indeed - Parsing page 1 out of " + str(page_count))
        for job in jobs_list:
            job_link = self.parse_job_link(job)
            keyword = self.is_relevant(job_link)
            if keyword:
                self.add_job(job, keyword)

        for i in range(1, page_count):
            print("Indeed - Parsing page " + str(i + 1) + " out of " + str(page_count))
            page_number += 10
            job_soup, page_count = self.load_jobs(page_number)
            jobs_list = job_soup.find_all('div', class_='cardOutline')
            for job in jobs_list:
                job_link = self.parse_job_link(job)
                keyword = self.is_relevant(job_link)
                if keyword:
                    self.add_job(job, keyword)

        if len(self.titles) == 0:
            print("Indeed - No jobs with the selected keywords were found.")
        else:
            self.create_table()

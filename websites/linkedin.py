import math
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from websites.parser import Parser


class linkedin_Parser(Parser):
    def __init__(self, job_title, location, range, keywords):
        super().__init__(job_title, location, range, keywords)
        self.website_name = "Linkedin"
        self.JOBS_PER_PAGE = 25

    def parse_page_count(self, element, days_range):
        labels = element.select("label")
        if days_range <= 1:
            value = labels[0].text
        elif days_range <= 7:
            value = labels[1].text
        elif days_range <= 31:
            value = labels[2].text
        else:
            value = labels[3].text
        return int(value[value.find('(') + 1:value.find(')')])

    def generate_range(self, days):
        if days == 1:
            return "f_TPR=r86400&"
        elif days <= 7:
            return "f_TPR=r604800&"
        elif days <= 31:
            return "f_TPR=r2592000&"
        return ""

    def generate_job_title_string(self):
        keywords = self.job_title.split()
        if len(keywords) < 2:
            return self.job_title
        formatted_title = ""
        for i in range(len(keywords) - 1):
            formatted_title += keywords[i] + "%20"
        return formatted_title + keywords[-1]

    def generate_url(self):

        date_posted_range = self.generate_range(self.range)
        url = ('https://www.linkedin.com/jobs/search/?'
               + date_posted_range +
               'keywords='
               + self.generate_job_title_string() +
               '&location=' + self.location)

        return url

    def parse_jobs_list_and_page_count(self, driver):
        count = int(driver.find_element(By.CSS_SELECTOR, "h1>span").get_attribute('innerText'))
        page_count = math.ceil(count / self.JOBS_PER_PAGE)

        for i in range(page_count):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
        driver.execute_script("window.scrollTo(0,0)")

        jobs_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        jobs = jobs_list.find_elements(By.TAG_NAME, 'li')

        return jobs, page_count

    def parse_job_title(self, element):
        try:
            title = element.find_element(By.CLASS_NAME, 'base-search-card__title').text
        except:
            title = ""
        return title

    def parse_job_company(self, element):
        try:
            company = element.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
        except:
            company = ""
        return company

    def parse_job_location(self, element):
        try:
            location = element.find_element(By.CLASS_NAME, 'job-search-card__location').text
        except:
            location = ""
        return location

    def parse_job_link(self, element):
        try:
            link = element.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')
        except:
            link = ''
        return link

    def is_relevant(self, job_description):
        for keyword in self.keywords:
            if keyword in job_description:
                return keyword
        return ""

    # Linkedin has 25 postings per page
    def extract_jobs(self):
        """
        Returns all relevant jobs that fit the given parameters
        :return: xlsx file of jobs that fit the criteria
        """

        url = self.generate_url()

        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        jobs_list, page_count = self.parse_jobs_list_and_page_count(driver)

        print("Linkedin - Parsing jobs...")

        for job in jobs_list:
            job.click()

            try:
                button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "show-more-less-html__button--more")))
                button.click()

                time.sleep(0.5)
                job_description = driver.find_element(By.CLASS_NAME, "show-more-less-html").text
                keyword = self.is_relevant(job_description.lower())
                if keyword:
                    self.add_job(job, keyword)

            except:
                print("Timeout: " + self.parse_job_title(job) + " - Job description didn't load")
                self.add_job(job, "TIMEOUT")

        driver.quit()

        if len(self.titles) == 0:
            print("Linkedin - No jobs with the selected keywords were found.")
        else:
            self.create_table()

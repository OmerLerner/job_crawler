import math
import time

from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
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
        """
        Scrolls down until 'Show more' button. Continue loading jobs until there are
        none left to load or the website times out.
        After all of the jobs are loaded, select the column that contains all of the
        job postings, split each element into a job_element and returns the list.
        :param driver: Chrome WebDriver that Selenium uses
        :return: A list of all of the job elements
        """
        count = driver.find_element(By.CSS_SELECTOR, "h1>span").get_attribute('innerText')
        if len(count) > 5:
            count = 1000
            page_count = count
        else:
            count = int(count)
            page_count = math.ceil(count / self.JOBS_PER_PAGE)

        timeout_count = 0

        #Sometimes the "show more" button doesn't work right away, added more margin for error by adding 5 iterations
        for i in range(page_count+5):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            try:
                infinite_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((
                    By.CLASS_NAME, "infinite-scroller__show-more-button"
                )))
                if infinite_button:
                    infinite_button.click()
                    infinite_button.click()
                    time.sleep(1)
            except TimeoutException:
                timeout_count += 1
                if timeout_count > 15 or i * self.JOBS_PER_PAGE > 999:
                    break
                driver.execute_script("window.scrollTo(0,0)")
            except ElementClickInterceptedException:
                break

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

    def handle_timeout_link(self,timeout_job,driver):
        """
        Second check for jobs that timed out during the first iteration. Load each page
        individually and try to parse the job information. If unsuccessful, adds the job
        anyways with the keyword TIMEOUT

        :param timeout_job: List- index 0: job element, index 1: job url
        :param driver: chromedriver
        :return: void
        """
        driver.get(timeout_job[0])
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "show-more-less-html__button--more")))
            button.click()
            time.sleep(0.5)
            job_description = driver.find_element(By.CLASS_NAME, "show-more-less-html").text
            keyword = self.is_relevant(job_description.lower())
            if keyword:
                self.add_job(timeout_job[1], keyword)
        except:
            print("Timeout: " + self.parse_job_title(timeout_job[0]) + " - Job description didn't load")
            self.add_job(timeout_job[0], "TIMEOUT")
            return

    # Linkedin has 25 postings per page
    def extract_jobs(self):
        """
        Iterate through all of the job listings, filtering the ones who have
        the relevant keywords in their job description.

        :return: xlsx file of all relevant jobs (and ones that have timed out)
        """

        url = self.generate_url()

        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        jobs_list, page_count = self.parse_jobs_list_and_page_count(driver)

        timeout_jobs = []
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
                timeout_jobs.append([self.parse_job_link(job),job])


        for timeout_job in timeout_jobs:
            self.handle_timeout_link(timeout_job, driver)
        driver.quit()

        if len(self.titles) == 0:
            print("Linkedin - No jobs with the selected keywords were found.")
        else:
            self.create_table()

import math
import urllib
import time
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# import os

JOBS_PER_PAGE = 25

extracted_data = []
titles = []
companies = []
links = []
relevant_keyword = []


def parse_page_count(element, days_range):
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


def generate_range(days):
    if days == 1:
        return "f_TPR=r86400&"
    elif days <= 7:
        return "f_TPR=r604800&"
    elif days <= 31:
        return "f_TPR=r2592000&"
    return ""


def generate_job_title_string(job_title):
    keywords = job_title.split()
    if len(keywords) < 2:
        return job_title
    formatted_title = ""
    for i in range(len(keywords) - 1):
        formatted_title += keywords[i] + "%20"
    return formatted_title + keywords[-1]


def add_job(job, keyword):
    """

    :param job: Job element that is being parsed
    :param keyword: String - Keyword that is found in description, otherwise "Timeout"
    :return: void - appends each value to it's relevant column
    """
    titles.append(parse_job_title(job))
    companies.append(parse_job_company(job))
    links.append(parse_job_link(job))
    relevant_keyword.append(keyword)

def create_table():
    extracted_data.append(titles)
    extracted_data.append(companies)
    extracted_data.append(links)
    extracted_data.append(relevant_keyword)


# https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords=student&location=Israel
# https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Israel
# https://www.linkedin.com/jobs/search/?keywords=data%20scientist&location=Israel&start=25


def generate_url(job_title, location, days_range, page_number):
    """
    Sends a get request, parses page and returns all of the job postings on current page

    :param job_title: String - name of job to search
    :param location: String - location of job
    :param days_range: Int - search jobs posted in last x days
    :param page_number: Int - current page number to load
    :return: Page containing all jobs
    """
    date_posted_range = generate_range(days_range)
    url = ('https://www.linkedin.com/jobs/search/?'
           + date_posted_range +
           'keywords='
           + generate_job_title_string(job_title) +
           '&location=' + location)

    if page_number > 1:
        url += "&start=" + str(25 * (page_number - 1))

    return url


def parse_jobs_list_and_page_count(driver):
    count = int(driver.find_element(By.CSS_SELECTOR, "h1>span").get_attribute('innerText'))
    page_count = math.ceil(count / JOBS_PER_PAGE)

    for i in range(page_count):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
    driver.execute_script("window.scrollTo(0,0)")

    jobs_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = jobs_list.find_elements(By.TAG_NAME, 'li')

    return jobs, page_count


def parse_job_title(element):
    try:
        title = element.find_element(By.CLASS_NAME, 'base-search-card__title').text
    except:
        title = ""
    return title


def parse_job_company(element):
    try:
        company = element.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
    except:
        company = ""
    return company


def parse_job_link(element):
    try:
        link = element.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')
    except:
        link = ''
    return link


def is_relevant(job_description, keywords):
    for keyword in keywords:
        if keyword in job_description:
            return keyword
    return ""


# Linkedin has 25 postings per page
def extract_jobs(job_title, location, days, keywords):
    """
    Returns all relevant jobs that fit the given parameters
    :param job_title: Name of job to search
    :param location: Location of job
    :param days: Posted in last x days
    :param keywords: Filter jobs that have these keywords in the title/description
    :return: csv file of jobs that fit the criteria
    """

    page_number = 1

    url = generate_url(job_title, location, days, page_number)

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    jobs_list, page_count = parse_jobs_list_and_page_count(driver)

    columns = ['Job Title', 'Company', 'Job Link',  'Relevant Keyword']

    print("Linkedin - Parsing jobs...")

    for job in jobs_list:
        job.click()

        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "show-more-less-html__button--more")))
            button.click()

            time.sleep(0.5)
            job_description = driver.find_element(By.CLASS_NAME, "show-more-less-html").text
            keyword = is_relevant(job_description.lower(), keywords)
            if keyword:
                add_job(job, keyword)


        except:
            print("Timeout - Job description didn't load")
            add_job(job, "TIMEOUT")

    driver.quit()

    if len(titles) == 0:
        print("Linkedin - No jobs with the selected keywords were found.")
    else:
        create_table()
        jobs_list = {}

        print("Linkedin - Done parsing, formatting data to CSV...")
        for i in range(len(columns)):
            jobs_list[columns[i]] = extracted_data[i]

        jobs = pd.DataFrame(jobs_list)
        jobs.to_csv("results-linkedin.csv")

        print("Linkedin - Done! Results saved into linkedin.csv")

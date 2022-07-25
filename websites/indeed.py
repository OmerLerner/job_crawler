import math
import urllib

import requests
from bs4 import BeautifulSoup
# import selenium
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

JOBS_PER_PAGE = 15

extracted_data = []

titles = []
companies = []
links = []
relevant_keyword = []


def parse_page_count(element):
    pages_element = element.text.split()
    return math.ceil(int(pages_element[3]) / JOBS_PER_PAGE)


# https://il.indeed.com /jobs?q=student&l=israel
def load_jobs(job_title, location, days_range, page_number):
    """
    Sends a get request, parses page and returns all of the job postings on current page

    :param job_title: String - name of job to search
    :param location: String - location of job
    :param days_range: Int - search jobs posted in last x days
    :param page_number: Int - current page number to load
    :return: Page containing all jobs
    """
    url = ('https://il.indeed.com/jobs?q='
           + job_title +
           '&l=' + location +
           '&fromage=' + str(days_range) +
           '&sort=date'
           '&start=' + str(page_number))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    pages_element = soup.find(id='searchCountPages')
    return job_soup, parse_page_count(pages_element)


def parse_job_title(element):
    try:
        title_element = element.find('h2', class_='jobTitle')
        title = title_element.text.strip()
    except:
        title = ""
    return title


def parse_job_company(element):
    try:
        company_element = element.find('span', class_='companyName')
        company = company_element.text.strip()
    except:
        company = ""
    return company


def parse_job_link(element):
    try:
        link_element = element.find('a')['href']
        link = 'https://il.indeed.com' + link_element
    except:
        link = ''
    return link


def is_relevant(job_url, keywords):
    page = requests.get(job_url)
    soup = BeautifulSoup(page.content, "html.parser")
    # job_description = soup.find(id="jobDescriptionText")

    key = ""
    for keyword in keywords:
        if keyword in soup.text.lower():
            return keyword

    return key


def add_job(job, keyword, job_link):
    """

    :param job: Job element that is being parsed
    :param keyword: String - Keyword that is found in description, otherwise "Timeout"
    :return: void - appends each value to it's relevant column
    """
    titles.append(parse_job_title(job))
    companies.append(parse_job_company(job))
    links.append(job_link)
    relevant_keyword.append(keyword)


def create_table():
    extracted_data.append(titles)
    extracted_data.append(companies)
    extracted_data.append(links)
    extracted_data.append(relevant_keyword)


# Indeed has 15 posting per page
def extract_jobs(job_title, location, days, keywords):
    """
    Returns all relevant jobs that fit the given parameters
    :param job_title: Name of job to search
    :param location: Location of job
    :param days: Posted in last x days
    :param keywords: Filter jobs that have these keywords in the title/description
    :return: csv file of jobs that fit the criteria
    """

    page_number = 0

    job_soup, page_count = load_jobs(job_title, location, days, page_number)
    jobs_list = job_soup.find_all('div', class_='cardOutline')

    columns = ['Job Title', 'Company', 'Job Link', 'Relevant Keyword']

    print("Indeed - Parsing page 1 out of " + str(page_count))
    for job in jobs_list:
        job_link = parse_job_link(job)
        keyword = is_relevant(job_link, keywords)
        if keyword:
            add_job(job, job_link, keyword)

    for i in range(1, page_count):
        print("Indeed - Parsing page " + str(i + 1) + " out of " + str(page_count))
        page_number += 10
        job_soup, page_count = load_jobs(job_title, location, days, page_number)
        jobs_list = job_soup.find_all('div', class_='cardOutline')
        for job in jobs_list:
            job_link = parse_job_link(job)
            keyword = is_relevant(job_link, keywords)
            if keyword:
                add_job(job, job_link, keyword)

    if len(titles) == 0:
        print("Indeed - No jobs with the selected keywords were found.")
    else:

        create_table()
        jobs_list = {}

        print("Indeed - Done parsing, formatting data to CSV...")
        for i in range(len(columns)):
            jobs_list[columns[i]] = extracted_data[i]

        jobs = pd.DataFrame(jobs_list)
        jobs.to_csv("results-indeed.csv")
        print("Indeed - Done! Results saved into results_indeed.csv")

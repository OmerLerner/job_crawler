import math
import urllib

import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

JOBS_PER_PAGE = 15


def parse_page_count(element):
    pages_element = element.text.split()
    return int(pages_element[3])


# https://il.indeed.com /jobs?q=student&l=israel
def load_jobs(job_title, location, days_range, page_number):
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



# Indeed has 15 posting per page
def extract_jobs(job_title, location, days, keywords):
    """ Input: (Title of wanted job, location of wanted job (Country or city), posted in the last x days,
     keywords to search for in job description = ['Python', 'Computer Science', etc] """

    page_number = 0

    job_soup, job_count = load_jobs(job_title, location, days, page_number)
    page_count = math.ceil(job_count / JOBS_PER_PAGE)
    job_elements = job_soup.find_all('div', class_='cardOutline')

    columns = []
    extracted_data = []

    titles = []
    companies = []
    links = []

    columns.append('titles')
    columns.append('companies')
    columns.append('links')

    for job_element in job_elements:
        titles.append(parse_job_title(job_element))
        companies.append(parse_job_company(job_element))
        links.append(parse_job_link(job_element))
        # extracted_data.append(titles)



    for i in range(1, page_count):
        page_number += 10
        job_soup, job_count = load_jobs(job_title,location,days,page_number)
        job_elements = job_soup.find_all('div',class_='cardOutline')
        for job_element in job_elements:
            titles.append(parse_job_title(job_element))
            companies.append(parse_job_company(job_element))
            links.append(parse_job_link(job_element))

    extracted_data.append(titles)
    extracted_data.append(companies)
    extracted_data.append(links)

    jobs_list = {}
    for i in range(len(columns)):
        jobs_list[columns[i]] = extracted_data[i]

    num_of_listings = len(extracted_data[0])

    jobs = pd.DataFrame(jobs_list)
    jobs.to_csv("results.csv")

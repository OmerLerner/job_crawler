import urllib
import requests
from bs4 import BeautifulSoup
# import selenium
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

from websites import indeed, linkedin
from websites.indeed import Indeed_parser
from websites.linkedin import Linkedin_parser


def main():
    job_title = "Intern"
    location = "Israel"
    keywords = ['computer science']
    # linkedin_parser = Linkedin_parser(job_title,location,1,keywords)
    indeed_parser = Indeed_parser(job_title,location,3,keywords)

    # linkedin_parser.extract_jobs()
    indeed_parser.extract_jobs()

    print("Job search complete!")


if __name__ == '__main__':
    main()

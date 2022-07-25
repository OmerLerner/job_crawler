import urllib
import requests
from bs4 import BeautifulSoup
# import selenium
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

from websites import indeed, linkedin


def main():
    keywords = ['python','java','computer science','javascript','software engineer']
    indeed.extract_jobs("Student", "Israel", 1, keywords)
    linkedin.extract_jobs("Student", "Israel", 1, keywords)
    print("Job search complete!")


if __name__ == '__main__':
    main()

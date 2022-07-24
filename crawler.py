import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

from websites import indeed


def main():
    keywords = ["Python","Java", "Javascript", "OOP", "C", "C++", "Computer Science",
                "Software Engineer"]
    indeed.extract_jobs("Student", "Israel", 14, keywords)


if __name__ == '__main__':
    main()

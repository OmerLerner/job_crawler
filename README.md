# Ultimate Job Crawler

Want to automate your job search? Look no further! My job crawler is simple to use, just download the script, modify a few variables, and you're good to go!


## How to use:

You can use crawler.exe and follow the instructions. Make sure chromedriver.exe and parameters.txt (After it's created) are in the same folder before running!

In addition, you can run the code yourself using the following instructions:

0.) Requirements: Python3, BeautifulSoup, Selenium, Pandas

1.) Enter crawler.py

2.) 

    a.) In crawler.py, change job_title, location, days (job posted in last x days) and keywords.

    b.) You can also write these inputs in the cmd


3.) In "keywords", write all the keywords that are relevant to your position. The crawler will filter out jobs that don't have these criteria in the job description.

Example: keywords = ['Python', 'Remote', 'AWS']

4.) Make sure you have the required dependencies, and run the script! When prompted, inputting 0 will use the data in crawler.py, 1 will allow you to write it in the cmd.

## Features & Notes

* The xlsx sheet will have 5 columns: Job title, job location, company name, relevant keyword (the first one that's found) and the url to the job listing

* Selenium will run Chrome in the background. Don't be alarmed, this is completely normal!

* Due to the 429 error (too many requests), LinkedIn sometimes doesn't load the job description. In order to combat this, I have implemented the following solution:
  * During the first iteration of all jobs, I use Selenium's wait methods and sleep() to simulate pauses in between requests. If there is a timeout:
    * The job will be appended to the "timeout_jobs", and we'll load it later
    * Waiting too little will result the next "get" to receive this error as well.
  * After we iterate through all the jobs, approximately 10-20% should be in the time_out list. We iterate through them again, but with higher wait times.
  * If this fails too (429 errors, not logged on to LinkedIn), it will be added to the list, with the "TIMEOUT" keyword.

This solution parses 99% of the jobs correctly, while 1% will be saved with "TIME OUT" as the keyword, without sacrificing runtime of the script.

## To-do

* Add additional websites (open to requests)

* **DONE** Created exe file to run the script

* **DONE** Linkedin - In pages with over 100 jobs, after scrolling down need to click on "More jobs" button if one exists

## Contact Me

If you have any questions or opportunities to send my way, I'm available at omerler@post.bgu.ac.il

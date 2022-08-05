# Ultimate Job Crawler #

Want to automate your job search? Look no further! My job crawler is simple to use, run the exe or the script, modify a few values, and you're good to go!

Currently supports: Linkedin, Indeed


## How to use: ##

### You have two options: Run the exe file, or run the script directly from your desired cmd ###

#### Option 1: Run by exe ####

Extract crawler.rar and run crawler.exe.  Make sure chromedriver.exe is in the same folder as crawler.exe

0.) On the first time you run it, write 1 and follow the instructions.

1.) You will be required to write the job name, job location, days (job posted in last x days) and keywords to search for.
    
    Example input:
    Job name = Student
    Job location = New York
    Days = 7
    Keywords = Python,Computer Science,Machine Learning

2.) The script will then run, and save the xlsx files in the same directory as crawler.exe

3.) The next time you run the exe, you can write 0 to use the same values, or 1 to write new values.
 

####Option 2: Run from CMD ####

In addition, you can run the code yourself using the following instructions:

0.) Requirements: Python3, BeautifulSoup, Selenium, Pandas

1.) Run crawler.py

2.) 

    a.) In crawler.py, change job_title, location, days (job posted in last x days) and keywords.

    b.) You can also write these inputs in the cmd by choosing option 1 when the script runs. These inputs will be saved into a file


3.) In "keywords", write all the keywords that are relevant to your position. The crawler will filter out jobs that don't have these criteria in the job description.

Example: keywords = ['Python', 'Remote', 'AWS']

4.) Make sure you have the required dependencies, and run the script! When prompted:

    0 - Use the data in parameters.txt
    1 - Input new data in the CMD
    2 - Use data stored in the variables in crawler.py

####Command line arguments: ####
##### -f : Runs the script directly, using the parameters saved in parameters.txt #####
##### -l : Parses jobs ONLY from Linkedin #####
##### -i : Parses jobs ONLY from Indeed #####
If you use both -l and -i, it will parse from both websites.

## Features & Notes ##

* The xlsx sheet will have 5 columns: Job title, job location, company name, relevant keyword (the first one that's found) and the url to the job listing

* Selenium will run Chrome in the background. Don't be alarmed, this is completely normal!

* Due to the 429 error (too many requests), LinkedIn sometimes doesn't load the job description. In order to combat this, I have implemented the following solution:
  * During the first iteration of all jobs, I use Selenium's wait methods and sleep() to simulate pauses in between requests. If there is a timeout:
    * The job will be appended to the "timeout_jobs", and we'll load it later
    * Waiting too little will result the next "get" to receive this error as well.
  * After we iterate through all the jobs, approximately 10-20% should be in the time_out list. We iterate through them again, but with higher wait times.
  * If this fails too (429 errors, not logged on to LinkedIn), it will be added to the list, with the "TIMEOUT" keyword.

This solution parses 99% of the jobs correctly, while 1% will be saved with "TIME OUT" as the keyword, without sacrificing runtime of the script.

## To-do ##

* Add additional websites (open to requests)

* **DONE** Created exe file to run the script

* **DONE** Linkedin - In pages with over 100 jobs, after scrolling down need to click on "More jobs" button if one exists

## Contact Me ##

If you have any questions or opportunities to send my way, I'm available at omerler@post.bgu.ac.il

# Ultimate Job Crawler

Want to automate your job search? Look no further! My job crawler is simple to use, just download the script, modify a few variables and you're good to go!


## How to use:

1.) Enter crawler.py

2.) Change job_title and location

3.) In "keywords", write all of the keywords that are relevant to your position. The crawler will filter out jobs that don't have these criteria in the job description.

Example: keywords = ['Python', 'Remote', 'AWS']

4.) Make sure you have the required dependencies, and run the script!

## Features (Not bugs)

* The xlsx sheet will have 5 columns: Job title, job location, company name, relevant keyword (the first one that's found) and the url to the job listing

* Selenium will run Chrome in the background. Don't be alarmed, this is completely normal!

* Linkedin sometimes doesn't load the job description. If enough time has passed, it will save the listing to the xlsx, and define the keyword as TIMEOUT.

## To-do

* Add additional websites (open to requests)

* Create a notebook to make the script easier to run

## Contact Me

If you have any questions or opprotunities to send my way, I'm available at omerler@post.bgu.ac.il

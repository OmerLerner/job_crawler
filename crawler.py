
from websites.indeed import indeed_Parser
from websites.linkedin import linkedin_Parser


def main():
    job_title = "Student"
    location = "Israel"
    days = 1
    keywords = ['computer science', 'python', 'javascript', 'c++', 'java']

    if len(job_title) > 0 and len(location)>0:
        linkedin_parser = linkedin_Parser(job_title,location,days,keywords)
        indeed_parser = indeed_Parser(job_title,location,days,keywords)

        linkedin_parser.extract_jobs()
        indeed_parser.extract_jobs()

        print("Job search complete!")


if __name__ == '__main__':
    main()

from modules import file_handler
from os.path import exists

from websites.indeed import indeed_Parser
from websites.linkedin import linkedin_Parser


def check_validity(job_title, location, days, keywords):
    if len(job_title) == 0 or len(location) == 0 or days == 0 or len(keywords) == 0:
        return False
    return True


def main():
    job_title = "student"
    location = "israel"
    days = 1
    keywords = ['computer science']

    values = []

    file_exists = exists('parameters.txt')

    if file_exists:
        choice = input("Write 0 to use values currently in parameters.txt, or 1 to input custom values (and save them "
                       "in parameters.txt), or 2 to use values saved in crawler.py:")
    else:
        choice = input("Write 1 to input values, or 2 to use values saved in crawler.py:")

    if (not file_exists) and choice == '0':
        print("Can't load values from a file that doesn't exist. Try again and use 1 as the input value.")
        exit(-1)
    else:
        values = file_handler.handle_input(choice)

    if values and len(values) == 4:
        job_title = values[0]
        location = values[1]
        days = values[2]
        keywords = values[3]
    if not check_validity(job_title, location, days, keywords):
        print("One of the parameters: job_title, location, days, keywords is invalid.")
        exit(-1)

    print("All values are valid! Starting to find jobs.")
    linkedin_parser = linkedin_Parser(job_title, location, days, keywords)
    indeed_parser = indeed_Parser(job_title, location, days, keywords)

    linkedin_parser.extract_jobs()
    indeed_parser.extract_jobs()

    print("Job search complete!")


if __name__ == '__main__':
    main()

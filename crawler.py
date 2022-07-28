from websites.indeed import indeed_Parser
from websites.linkedin import linkedin_Parser


def main():
    job_title = "Student"
    location = "Israel"
    days = 1
    keywords = ['computer science', 'python', 'javascript', 'c++', 'java', 'software engineer']

    choice = input("Write 0 to use values currently saved in crawler.py, or 1 to input custom values:")
    if choice == "1":
        job_title = input("Write the job title to search for: ")
        location = input("Write the city/country to search for jobs: ")
        days = input("Write a number - Check jobs posted in last X days: ")
        if days.isnumeric():
            days = int(days)
        else:
            count = 1
            while not days.isnumeric():
                if count == 3:
                    print("Bye bye.")
                    exit()
                elif count == 2:
                    days = input("Last chance, write a number this time. I believe in you: ")
                    count += 1
                else:
                    days = input(
                        "Alright, you had your fun. Write a number to scan the jobs posted in the last X days:")
                    count += 1
        print("\n")
        print("Write down all of the keywords to scan for in the job description, and seperate each one by a comma.")
        print("For example: Python,Full-Stack,Backend Engineer")
        keywords_string = input("Write the keywords here: ")
        keywords = keywords_string.split(',')

    if len(job_title) > 0 and len(location) > 0:
        linkedin_parser = linkedin_Parser(job_title, location, days, keywords)
        indeed_parser = indeed_Parser(job_title, location, days, keywords)

        linkedin_parser.extract_jobs()
        indeed_parser.extract_jobs()

        print("Job search complete!")


if __name__ == '__main__':
    main()

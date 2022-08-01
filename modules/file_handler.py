def read_file(file):
    lines = file.readlines()
    return [
        lines[0][10:].strip(),
        lines[1][9:].strip(),
        lines[2][6:].strip(),
        lines[3][9:].split(',')
    ]


def write_file(file, temp_title, temp_location, temp_days, keywords_string):
    file.write("Job title:" + temp_title + '\n')
    file.write("Location:" + temp_location + '\n')
    file.write("Range:" + str(temp_days) + '\n')
    file.write("Keywords:" + keywords_string)


def handle_input(choice):
    if choice == '0':
        try:
            file = open('parameters.txt', 'r')
            values = read_file(file)
            print(values)
            file.close()
            return values
        except FileNotFoundError:
            print("File hasn't been created. Run the program again and choose choice 1.")
            exit(-1)
    elif choice == "1":
        temp_title = input("Write the job title to search for: ")
        temp_location = input("Write the city/country to search for jobs: ")
        temp_days = input("Write a number - Check jobs posted in last X days: ")
        if temp_days.isnumeric():
            temp_days = int(temp_days)
        else:
            count = 1
            while not temp_days.isnumeric():
                if count == 3:
                    print("Bye bye.")
                    exit()
                elif count == 2:
                    temp_days = input("Last chance, write a number this time. I believe in you: ")
                    count += 1
                else:
                    temp_days = input(
                        "Alright, you had your fun. Write a number to scan the jobs posted in the last X days:")
                    count += 1
        print(
            "Write down all of the keywords to scan for in the job description, and seperate each one by a comma.")
        print("For example: Python,Full-Stack,Backend Engineer")
        keywords_string = input("Write the keywords here: ").lower()
        temp_keywords = keywords_string.split(',')

        file = open('parameters.txt', 'w')
        write_file(file, temp_title, temp_location, temp_days, keywords_string)
        file.close()
        return [temp_title, temp_location, temp_days, temp_keywords]
    elif choice == '2':
        return
    else:
        print("Invalid input")
        exit(-1)

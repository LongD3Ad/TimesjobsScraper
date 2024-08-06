#TODO In this program we  use the with open function to save and write the file as a txt document whenever we scrape data

import time
from bs4 import BeautifulSoup
import requests

# Taking in the user input to see what skills they are not familiar with
print(">>>>> Mention the skills you are not familiar with <<<<<")
unfamiliar_skills = input('>').lower().split()  # Convert to lowercase for case-insensitive comparison

print(f'FILTERING OUT JOBS THAT REQUIRE: {", ".join(unfamiliar_skills)}')

def finding_jobs(page):
    # Adjust the URL to include the page number so here we look into the url pattern whenever it changes to a new page and add a sequence and a page
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=&sequence={page}&startPage={page}'

    # Here we are calling a response
    response = requests.get(url)

    # Parsing that response as a text
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")

    if not jobs:
        return False  # Stop condition if no jobs are found

    # Use the for loop to go through the current page and fetch data
    for index, job in enumerate (jobs): #we can use the enumerate to make the with open function easy to save the txt files according to the index numbers so 0.txt 1.txt...etc etc
        company_name = job.find('h3', class_='joblist-comp-name').text.strip()
        job_desc = job.find('label', string='Job Description:')
        found = job_desc.next_sibling.strip() if job_desc else 'No description available'
        skill_needed = job.find('span', class_='srp-skills').text.replace(" ", "").lower()  # Remove spaces and convert to lowercase
        date = job.find('span', class_='sim-posted').text.strip()
        more_info = job.header.h2.a['href']  # Dictionary is used to remove the a and href tag from print
        
        # Split the required skills into a list
        skills_list = skill_needed.split(',')

        # Check if any of the unfamiliar skills are in the job's required skills
        if not any(skill in skills_list for skill in unfamiliar_skills):
            #using the with open function here to create a text file saved according to index values
            with open(f'data/{index}.txt', 'w') as f:
            # Join the skills for neat output
                neat_output = ', '.join(skills_list)
                #using the write and \n operation to save the extracted data neatly
                f.write(f"Company Name: {company_name} \n")
                f.write(f"Job Description: {found.strip()} \n")
                f.write(f"Skills Required: {neat_output.strip()} \n")
                f.write(f"Job Posted: {date} \n")
                f.write(f"More Info: {more_info} \n")
            print(f"File Saved : {index}")
                
    return True

if __name__ == '__main__':
    page = 1
    while True:
        if not finding_jobs(page):
            break  # Stop if no more jobs are found
        page += 1  # Move to the next page
        time_wait = 10 
        print(f'Waiting {time_wait} minutes before fetching page {page}...')
        time.sleep(time_wait*60)

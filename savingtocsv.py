#NOTE here after practing and checking out how to save data into a csv file we are gonna slightly modify the code and try and save the scraped data into csv format

import time
from bs4 import BeautifulSoup
import requests
import os
import csv
# Taking in the user input to see what skills they are not familiar with
print(">>>>> Mention the skills you are not familiar with <<<<<")
unfamiliar_skills = input('>').lower().split()  # Convert to lowercase for case-insensitive comparison

print(f'FILTERING OUT JOBS THAT REQUIRE: {", ".join(unfamiliar_skills)}')
    
def save_job_data_csv(index, page_number, company_name, found, skills_list, date, more_info):
    try:
        # Make sure the directory exists
        os.makedirs('data', exist_ok=True)

        # Create a CSV file
        filename = 'data/jobs1_data.csv'
        file_exists = os.path.isfile(filename)

        # Prepare the neat output
        neat_output = ', '.join(skills_list)

        # Write the data to the CSV file
        with open(filename, 'a', newline='') as csvfile:
            field_names = ['Index', 'Page Number', 'Company Name', 'Job Description', 'Skills Required', 'Job Posted', 'More Info']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)

            if not file_exists:
                writer.writeheader()  # Write header only if file doesn't exist

            writer.writerow({
                'Index': index,
                'Page Number': page_number,
                'Company Name': company_name,
                'Job Description': found.strip(),
                'Skills Required': neat_output.strip(),
                'Job Posted': date,
                'More Info': more_info
            })

        print(f"File Saved Successfully: {filename}")

    except Exception as e:
        print(f"Failed to save file {filename}: {e}")


def finding_jobs(page):
    # Adjust the URL to include the page number
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=&sequence={page}&startPage={page}'

    # Call a response
    response = requests.get(url)

    # Parse that response as text
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")

    if not jobs:
        return False  # Stop condition if no jobs are found

    # Loop through the current page and fetch data
    for index, job in enumerate(jobs): 
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
            # Save the job data using the improved function
            save_job_data_csv(index, page, company_name, found, skills_list, date, more_info)
                
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

import re
import requests
import sys

from bs4 import BeautifulSoup

def scrape_gradconnection(url):
    domain_name = re.sub(r'^(.+\.com).+$', r'\1', url)

    page = requests.get(url)

    #print(page.text)   # Prints Entire Webpage (Inspect Element)
    soup = BeautifulSoup(page.content, 'html.parser')

    job_elements = soup.find_all("div", class_='campaign-box')

    app_name_list = []
    company_list = []
    app_link_list = []
    deadline_list = []

    for job_element in job_elements:
        app_name = str(job_element.find('h3'))[4: -5]

        company = str(job_element.find('p', class_='box-header-para'))[27: -4]

        app_link = str(job_element.find('a', class_='box-header-title'))
        app_link = domain_name + re.sub(r'^.+href=\"(.+?)\".+$', r'\1', app_link)

        deadline = str(job_element.find('span', class_='closing-in closing-in-button'))[54: -7].capitalize()

        app_name_list.append(app_name)
        company_list.append(company)
        app_link_list.append(app_link)
        deadline_list.append(deadline)

        print(app_name)
        print(company)
        print(app_link)
        print(deadline, end="\n"*2)
    return(app_name_list,company_list,app_link_list,deadline_list)

def print_usage():
    print('usage:')
    print('python3 main.py')
    print('python3 main.py <field> <job_type>')
    print('python3 main.py <field> <job_type> <ordering>')
    print('<field>: {}'.format(', '.join(mapping['gradconnection']['field'].keys())))
    print('<job_type>: {}'.format(', '.join(mapping['gradconnection']['job_type'].keys())))
    print('<ordering>: {}'.format(', '.join(mapping['gradconnection']['ordering'].keys())))

    exit()

mapping = {
    'gradconnection': {
        'domain': 'https://au.gradconnection.com/',
        'field': {
            'business': 'business-and-commerce',
            'civil': 'engineering-civil-structural',
            'electrical': 'engineering-electrical',
            'mechanical': 'engineering-mechanical',
            'software': 'engineering-software',
            'structual': 'engineering-civil-structural',
        },
        'func': scrape_gradconnection,
        'ordering': {
            'closing': 'earliest_closing_date',
            'newest': '-recent_job_created'
        },
        'job_type': {
            'grad': 'graduate-jobs',
            'intern': 'internships',
        }
    },
}


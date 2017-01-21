import pickle
import requests
from bs4 import BeautifulSoup as bsoup
import re
from os import listdir
import json

html_parser = "lxml"

#  Initialize a requests session
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'})

def parse_team_member(member):
    """Given the contents of a team member list item, returns the team member's name and contribution
    """
    member_name = member.find('div', {'class': 'row'}).find('div', {'class': 'small-10 large-8 columns'}).find('a').text
    member_contribution = member.find('div', {'class': 'bubble'})
    member_contribution = "" if member_contribution is None else member_contribution.find('p').text
    return (member_name, member_contribution)

def list_projects(hackathon_root):
    """Given a hackathon hostname on devpost, retrieves a list of projects, and returns the URL for each of them
    """
    # Static variables
    projects_per_page = 24
    # Initializes the current page
    cur_page = 1
    # Stores project urls
    projects = []
    while True:
        # Retrieve the current page of submissions
        submission_page = session.get('{}/submissions?page={}'.format(hackathon_root, cur_page)).text
        submission_soup = bsoup(submission_page, html_parser)
        project_rows = submission_soup.find('div',id='submission-gallery').find_all('div')
        start_num, end_num, total = tuple(map(int, re.match('(\d+) – (\d+) of (\d+)', project_rows[-1].p.text).groups()))
        project_rows = project_rows[1:-1]
        for row in project_rows:
            for col in row.find_all('div')[:-1]:
                hackathon_link = col.a
                if hackathon_link is None:
                    continue
                projects.append(hackathon_link['href'])
        if end_num == total:
            break
        else:
            cur_page += 1
    return projects

def scrape_project(project_url):
    """Given a devpost project URL, returns ths
    title: The project's title
    project_details: The project's writeup
    team_details: Each team member and their contribution
    """
    # Soupify the project page
    project_page = session.get(project_url).text
    project_soup = bsoup(project_page, html_parser)
    # Retrieve the project title
    project_title = project_soup.find('h1',id='app-title').text
    # TODO: Retrieve project image or randomly generate images
    # Retrieve the project write-up
    project_details = project_soup.find('div',id='app-details-left').text
    # Retrieve team contributions
    team_details = [parse_team_member(member) for member in project_soup.find_all('li', {'class': 'software-team-member'})]
    return {'title': project_title, 'project_details': project_details, 'team_details': team_details}

def search_hackathon(name):
    search_page = session.get('https://devpost.com/hackathons?utf8=✓&search={}&challenge_type=all&sort_by=Recently+Added'.format(name)).text
    if 'find any challenges' in search_page:
        #TODO: strip qualifiers
        print('Hackathon {} doesn\'t exist'.format(name))
        return set()
    else:
        print('Hackathons found under {}'.format(name))
    search_soup = bsoup(search_page, html_parser)
    hackathon_urls = set()
    for hackathon in search_soup.find('div', {'class':'results'}).div.find_all('div', {'class': 'row'}):
        link = hackathon.div.article
        if link is None:
            continue
        hackathon_urls.add(re.search('https://.*\.devpost\.com', link.a['href']).group(0))
    return hackathon_urls

hackathon_list = set()
for year in listdir('./hackathon_list'):
    for month in listdir('./hackathon_list/'+year):
        for hackathon in list(json.load(open('./hackathon_list/{}/{}'.format(year, month), 'r')).values())[0]:
            hackathon_list.add(hackathon['title'])

hackathon_url_list = set()

"""
#Retrieves hackathon list
for index, hackathon in enumerate(hackathon_list):
    print('{}%',(index/len(hackathon_list))*100)
    try:
        hackathon_url_list.update(search_hackathon(hackathon))
    except:
        print('failed to retrieve hackathons for {}'.format(hackathon))
with open('hackathon_urls','w') as hackathon_url_list_file:
    for hackathon_url in hackathon_url_list:
        hackathon_url_list_file.write('{}\n'.format(hackathon_url))
"""



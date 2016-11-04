import requests
from bs4 import BeautifulSoup
import re


def create_flowchart(major):
    # get the soup object
    url = 'http://catalog.illinois.edu/courses-of-instruction/{}'.format(major)
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # dictionary of courses, with the values being a list of that
    # courses pre-reqs
    courses = {}

    for row in soup.find_all('div', {'class': 'courseblock'}):

        # gets the title of the course in the form: [class #, class name, credit hours]
        # ex: ['CS 100','Freshman Orientation','credit: 1 Hour.']
        course_title = [str(i.strip().replace(u'\xa0', u' ')) for i in
                        row.find('p', {'class': 'courseblocktitle'}).find('strong').text.split(u'\u2002')]

        # add each course to the dictionary, keyed by the course number
        courses[course_title[0]] = []

        course_description = row.find('p', {'class': 'courseblockdesc'})

        if 'Prerequisite: ' in course_description.text:
            # gets a string of the pre-reqs (the description in english)
            pre_requisites = course_description.text.split('Prerequisite: ')[1]

            # gets each course referenced in the course description, and appends it to the dictionary
            # if it is in the pre-req section
            for pre_req in course_description.find_all('a', {'class:', 'bubblelink code'}):
                for pre_req_block in pre_requisites.split('; '):
                    # if " or " in pre_req_block.lower() or "one of " in pre_req_block.lower():
                    print pre_req_block
                if pre_req.text in pre_requisites:
                    courses[course_title[0]].append(str(pre_req.text.replace(u'\xa0', u' ')))

            # TODO: account for 'or' pre-reqs (and 'One of')
            # TODO: account for concurrent
    print courses


if __name__ == '__main__':
    create_flowchart('cs')

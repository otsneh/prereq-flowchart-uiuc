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

        if 'Prerequisite:' in course_description.text:
            # gets a string of the pre-reqs (the description in english)
            pre_requisites = BeautifulSoup(course_description.prettify().split('Prerequisite:')[1], 'html.parser')

            # splits up the pre-reqs into groups that include "or" or "one of"
            # e.g., multiple courses that all satisfy a single pre-req
            for pre_req_block in pre_requisites.prettify().split('; '):
                block_soup = BeautifulSoup(pre_req_block, 'html.parser')

                # list of pre-reqs that all satisfy the same requirement
                block_pre_reqs = []

                # gets each course referenced in each "or" block of the course description,
                # and appends it to a list of pre-reqs in that block
                for pre_req in block_soup.find_all('a', {'class:', 'bubblelink code'}):
                    block_pre_reqs.append(pre_req.text.replace(u'\xa0', u' ').strip())

                # appends that list to the dictionary
                courses[course_title[0]].append(block_pre_reqs)

            # TODO: account for concurrent
    print courses


if __name__ == '__main__':
    create_flowchart('cs')

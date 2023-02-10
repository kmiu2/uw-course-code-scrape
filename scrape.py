import requests
from bs4 import BeautifulSoup
import json

data = []

url = "https://ucalendar.uwaterloo.ca/2223/COURSE/course-NE.html"

# Create object page
page = requests.get(url)

# Parse HTML and save to BeautifulSoup object
soup = BeautifulSoup(page.text, "lxml")

# Get all divTable classes
divTable = soup.find_all("div", class_="divTable")

# NE Terms
terms = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]

# Iterate through each divTable
for table in divTable:
    divTableCell = table.find_all("div", class_="divTableCell")

    # Store course code, name, and description
    course_code = divTableCell[0].text
    course_name = divTableCell[2].text
    course_desc = divTableCell[3].text

    # Some courses have an extra sub note, need to add to description
    if len(divTableCell) > 6:
        course_desc += " " + divTableCell[4].text

    # Only take the course code
    temp = course_code.split(" ")
    course_code = temp[0] + " " + temp[1]

    # Remove extra spaces
    course_desc = course_desc.replace("  ", " ")

    # Determine term based on offering
    term = ""
    if course_code.startswith("NE 1"):
        if ": F" in course_desc:
            term = "1A"
        elif "W]" in course_desc:
            term = "1B"
    elif course_code.startswith("NE 2"):
        if ": F" in course_desc:
            term = "2A"
        elif ": S" in course_desc:
            term = "2B"
    elif course_code.startswith("NE 3"):
        if ": S" in course_desc:
            term = "3A"
        elif ": F" in course_desc:
            term = "3B"
    elif course_code.startswith("NE 4"):
        if ": F" in course_desc:
            term = "4A"
        elif ": W" in course_desc:
            term = "4B"

    # Determine x and y coordinates based on term
    x = 0
    y = 0
    x_diff = 200
    y_diff = 100

    # Loop through terms to find the index of the term
    for i in range(len(terms)):
        if term == terms[i]:
            x = x_diff * i

    # Add y_diff for the number of courses already added for that term
    for i in range(len(data)):
        if data[i]["term"] == term:
            y += y_diff

    # data += [[course_code, course_name, course_desc, term, x, y]]
    data.append(
        {
            "course_code": course_code,
            "course_name": course_name,
            "course_desc": course_desc,
            "term": term,
            "x": x,
            "y": y,
        }
    )

# Save to JSON file
with open("data.json", "w") as outfile:
    json.dump(data, outfile)

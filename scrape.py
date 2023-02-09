import requests
from bs4 import BeautifulSoup
import csv

data = []

url = "https://ucalendar.uwaterloo.ca/2223/COURSE/course-NE.html"

# Create object page
page = requests.get(url)

# Parse HTML and save to BeautifulSoup object
soup = BeautifulSoup(page.text, "lxml")

# Get all divTable classes
divTable = soup.find_all("div", class_="divTable")

# Iterate through each divTable
for table in divTable:
    divTableCell = table.find_all("div", class_="divTableCell")

    # Store course code, name, and description
    course_code = divTableCell[0].text
    course_name = divTableCell[2].text
    course_desc = divTableCell[3].text

    # Only take the course code
    temp = course_code.split(" ")
    course_code = temp[0] + " " + temp[1]

    data += [[course_code, course_name, course_desc]]

# Save to CSV
with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)

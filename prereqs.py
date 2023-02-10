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

# Iterate through each divTable
for table in divTable:
    divTableCell = table.find_all("div", class_="divTableCell")

    # Store course code and prerequisites
    course_code = divTableCell[0].text
    temp = course_code.split(" ")
    course_code = temp[0] + " " + temp[1]
    course_prereqs = divTableCell[-1].text

    # Remove brackets
    course_prereqs = course_prereqs.replace("(", "")
    course_prereqs = course_prereqs.replace(")", "")

    # Remove everything after ;
    if ";" in course_prereqs:
        course_prereqs = course_prereqs.split(";")[0]

    # Remove extra spaces
    course_prereqs = course_prereqs.replace("  ", " ")

    # Find the prereq
    if "Prereq: NE" in course_prereqs:
        course_prereqs = course_prereqs.split("Prereq: ")[1]

        # If there is a comma, add in NE prefix
        if "," in course_prereqs:
            course_prereqs = course_prereqs.replace(",", ", NE")

        # Idk why 381 has " - " this page is weird
        if " - " in course_prereqs:
            course_prereqs = course_prereqs.split(" - ")[0]
    else:
        course_prereqs = ""

    data.append({"course_code": course_code, "prereqs": course_prereqs})

# Format for Course Map.
# Current Format:
# { "course_code": "NE 102B", "prereqs": "" },
# { "course_code": "NE 461", "prereqs": "NE 352, NE 353" },

# Desired Format:
# {id: "NE 352 - NE 451", source: "NE 352", target: "NE 451"},

formatted_data = []
for course in data:
    if course["prereqs"] != "":
        prereqs = course["prereqs"].split(", ")
        for prereq in prereqs:
            formatted_data.append(
                {
                    "id": prereq + " - " + course["course_code"],
                    "source": prereq,
                    "target": course["course_code"],
                }
            )

# Write to JSON file
with open("prereqs.json", "w") as outfile:
    json.dump(formatted_data, outfile)

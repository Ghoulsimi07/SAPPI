# SAPPI
HackFax x PatriotHacks 2026

TechStack: Python, Flask, MongoDB (for local hosting)

MongoDB_Data: 
- Collections for the SAPPI DB
- You can import the JSON into the collections

Output: Sample Chat Export for SAPPI

parsingCode: A folder containing logic to scrape GMU course data for ALL (yes all) majors
We then break apart the pre-requisites (required only) for EACH course and store all possible paths in the txt file
Ex: Let's say CS262 has prereq as follows (CS 110C, 110XS, or 251C) and MATH 113C. 
We construct the following paths:
- CS110 C and MATH 113C
- CS110 XS and MATH 113C
- CS 251C and MATH 113C

src: Flask web-app that you can run locally
- static = css and images
- templates - html files
- 1 javascript function to switch between buttons
- main.py = Flask web application + dynamically get DB info from MongoDB

HOW TO RUN: After importing the MongoDB collections, run main.py

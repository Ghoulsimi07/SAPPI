import requests
from bs4 import BeautifulSoup
import breakPreReq as parsingRequisite

MainURL = 'https://catalog.gmu.edu/courses/'
exceptionTable = {'Design':'design','Honors College':'science/math','MS Business Analytics':'ms-business-analytics-msba','Operations &​ Supply Chain Management':'operations--supply-chain-management'}

def grabHTMLContent(url):
    response = requests.get(url)
    html_content = None
    if response.status_code == 200:
        html_content = response.text
    else:
        raise ValueError('missing page')
    return html_content

def grabMajorDictionary(url):
    html_content = grabHTMLContent(url)

    majorDict = {}

    soup = BeautifulSoup(html_content, 'html.parser')
    courseblocks = soup.find_all(class_='courseblock')

    for courseblock in courseblocks:

        courseblocktext = courseblock.get_text()
        title = courseblocktext.split('\n')[1]
        desc = courseblocktext.split('\n')[2]
        recCleansed = ''

        if 'Required Prerequisites:' in desc:
            recCleansed = courseblocktext.split('Required Prerequisites:')[1].split('.')[0]
            majorDict[title] = recCleansed
        else:
            majorDict[title] = None

    return majorDict

def parseAllLinks(mainURL):
    html_content = grabHTMLContent(mainURL)
    soup = BeautifulSoup(html_content, 'html.parser')
    majorList = soup.select("a[href*=course]")
    
    majorDict = {}
    for major in majorList:
        courseTitle = major.get_text()

        if '(' in courseTitle:
            majorName = courseTitle.split('(')[0].strip()
            abbreviation = courseTitle.split('(')[1].split(')')[0]
            if majorName not in exceptionTable:
                majorDict[majorName] = 'https://catalog.gmu.edu/courses/'+abbreviation.lower()+'/'
            else:
                majorDict[majorName] = 'https://catalog.gmu.edu/courses/'+ exceptionTable[majorName].lower()+'/'

    return majorDict 

def constructAllCourses():
    majorDictionary = parseAllLinks(MainURL)

    UniversityCatalog = {}
    for major in majorDictionary:
        try:
            majorSpecificCourseCatalogDictionary = grabMajorDictionary(majorDictionary[major])
            UniversityCatalog[major] = majorSpecificCourseCatalogDictionary
        except Exception as e:
            dummy = 1
    return UniversityCatalog

def printFinalConstruction():
    finalConstruction = constructAllCourses()
    for major in finalConstruction:
            with open('./TextFiles/'+major+'.txt', 'w', encoding='utf-8') as f:
                for course in finalConstruction[major]:
                    courseStripped = course.replace('\xa0',"")

                    if finalConstruction[major][course] is not None:
                        requisite = finalConstruction[major][course].replace("\xa0"," ").strip()
                        newRequisite = parsingRequisite.parseResult(requisite)
                        for eachRequisite in newRequisite:
                            if 'or' in eachRequisite:
                                eachRequisite.remove('or')
                            if eachRequisite is not None and len(eachRequisite) > 0:
                                f.write(f"{major},{courseStripped},{eachRequisite}\n")
                    else:
                        f.write(f"{major},{courseStripped},{None}\n")
                f.close()

printFinalConstruction()
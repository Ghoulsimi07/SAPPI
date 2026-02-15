from flask import Flask, render_template, request, redirect, url_for
import pymongo
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SAPPI"]

studentDB = mydb["Student"]
currentStudent = studentDB.find()
for student in currentStudent:
    student = student 

global name 
name = student['name']

global current_semester
global next_semester
global second_semester
global third_semester

current_semester = '2025-08'
next_semester = '2026-02'
second_semester = '2026-06'
third_semester = '2026-08'


def grabStudent():
    global name
    studentDB = mydb["Student"]
    currentStudent = studentDB.find({"name":name})
    for student in currentStudent:
        return student 

def grabRequirements():
    student = grabStudent()
    major = student['major']
    name = student['name']
    
    requirementDB = mydb["Requirements"]
    courseDB = mydb['Courses']
    courses = courseDB.find()
    courseDict = {}
    for course in courses:
        courseDict[course['Course']] = course

    courseTakenDB = mydb['Student-Courses-Taken']
    coursesTaken = courseTakenDB.find({'Student':name})
    courseTaken = []
    for course in coursesTaken:
        courseTaken.append(course['CourseTaken'])

    coreClass1 = [x for x in requirementDB.find({"Major":major,'Type':'Core'})]
    seniorClass1 = [x for x in requirementDB.find({"Major":major,'Type':'Senior'})]
    electiveClass1 = [x for x in requirementDB.find({"Major":major,'Type':'Elective'})]
    
    for classLabel in [coreClass1,seniorClass1,electiveClass1]:
        for x in classLabel:
            specificCourse = courseDict[x['Course']] 
            x['description'] = specificCourse['Description']
            x['pre_req'] = specificCourse['Pre_Req']
            x['credits'] = specificCourse['Credits']

    coreClass = []
    for x in coreClass1:
        if x['Course'] not in courseTaken:
            coreClass.append(x)
        
    electiveClass = []
    for x in electiveClass1:
        if x['Course'] not in courseTaken:
            electiveClass.append(x)

    seniorClass = []
    for x in seniorClass1:
        if x['Course'] not in courseTaken:
            seniorClass.append(x)
    return coreClass, electiveClass, seniorClass

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    global name
    studentDB = mydb["Student"]
    currentStudent = studentDB.find({"name":name})

    for student in currentStudent:
        student = student 

    if request.method == "POST":
        nameForm = request.form.get("name")
        majorForm = request.form.get("major")
        graduationForm = request.form.get("graduation")

        studentDB.update_one({"name":name}, {'$set':{'name':nameForm,"major":majorForm,"expected_graduation":graduationForm}},upsert=False)
        
        name = nameForm

        currentStudent = studentDB.find({"name":name})
        for student in currentStudent:
            student = student 
        return render_template("update.html",student=student)
    
    return render_template("update.html",student=student)

@app.route("/requirements")
def requirements():
    coreClass, seniorClass, electiveClass = grabRequirements()

    coreCount = len(coreClass)
    seniorCount = len(seniorClass)
    electiveCount = len(electiveClass)
    CreditCount = coreCount + seniorCount + electiveCount
    return render_template("requirements.html",CoreCount=coreCount,SeniorCount=seniorCount,ElectiveCount=electiveCount,coreClass=coreClass,seniorClass=seniorClass,electiveClass=electiveClass,CreditCount=CreditCount)

@app.route("/optimal-path")
def optimal_path():
    global current_semester
    current_semester = current_semester

    student = grabStudent()
    major = student['major']
    name = student['name']

    courseTakenDB = mydb['Student-Courses-Taken']
    coursesTaken = courseTakenDB.find({'Student':name,"Semester":current_semester})

    courseTakenList = []
    for course in coursesTaken:
        courseTakenList.append(course['CourseTaken'])

    courseDB = mydb['Courses']
    courses = courseDB.find()
    courseList = []
    for course in courses:
        if course['Course'] in courseTakenList:
            courseList.append(course)    
    
    AllcoursesTaken = courseTakenDB.find({'Student':name})
    AllcourseTakenList = []
    for course in AllcoursesTaken:
        AllcourseTakenList.append(course['CourseTaken'])

    #print()
    #print(AllcourseTakenList)

    global next_semester
    global third_semester
    global second_semester

    coreClass, seniorClass, electiveClass = grabRequirements()
    coreClass.extend(seniorClass)
    coreClass.extend(electiveClass)
    #print(coreClass)

    classesProgress = []
    for remainingClass in coreClass:
        if remainingClass['pre_req'] is None:
            remainingClass['semester'] = next_semester
            classesProgress.append(remainingClass)
        elif 'and' in remainingClass['pre_req']:
            andList = remainingClass['pre_req'].split(' and ')
            countNot = 0
            notSatisfied = False 
            for item2 in andList:
                if item2.strip() not in AllcourseTakenList:
                    countNot += 1
                    notSatisfied = True
            if notSatisfied:
                if countNot >= 2:
                    remainingClass['semester'] = third_semester
                elif countNot == 1:
                    remainingClass['semester'] = second_semester
            else:
                remainingClass['semester'] = next_semester
            classesProgress.append(remainingClass)
        elif 'or' in remainingClass['pre_req']:
            orList = remainingClass['pre_req'].split(' or ')
            satisfied = False
            for item2 in orList:
                if item2.strip() not in AllcourseTakenList:
                    satisfied = True
            if not satisfied:
                remainingClass['semester'] = second_semester
            else:
                remainingClass['semester'] = next_semester
            classesProgress.append(remainingClass)

    classesProgress = sorted(classesProgress, key=lambda d: d['semester'])
    return render_template("optimal_path.html",classes=classesProgress,classesProgress=courseList,current_semester=current_semester)

@app.route("/patriotai")
def patriotai():
    return render_template("patriotai.html")

if __name__ == "__main__":
    app.run(debug=True)
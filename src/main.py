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


def grabStudent():
    global name
    studentDB = mydb["Student"]
    currentStudent = studentDB.find({"name":name})
    for student in currentStudent:
        return student 

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

    coreCount = len(coreClass)
    seniorCount = len(seniorClass)
    electiveCount = len(electiveClass)
    CreditCount = coreCount + seniorCount + electiveCount
    print(CreditCount)
    return render_template("requirements.html",CoreCount=coreCount,SeniorCount=seniorCount,ElectiveCount=electiveCount,coreClass=coreClass,seniorClass=seniorClass,electiveClass=electiveClass,CreditCount=CreditCount)

@app.route("/optimal-path")
def optimal_path():
    classesProgress=[{"course":"PHYS216","description":"Electrical Systems and Circuits for Engineers","pre_req":"MATH113C AND PHYS214C","semester":"Fall 2026","credits":3}]
    classes=[{"course":"PHYS216","description":"Electrical Systems and Circuits for Engineers","pre_req":"MATH113C AND PHYS214C","semester":"Fall 2026","credits":3}]
    return render_template("optimal_path.html",classes=classes,classesProgress=classesProgress)

@app.route("/patriotai")
def patriotai():
    return render_template("patriotai.html")

if __name__ == "__main__":
    app.run(debug=True)
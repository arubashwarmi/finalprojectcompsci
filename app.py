import sqlite3

#Importing the SQL module into the python environment so that we can work with it

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#The above decorator (and the similarly formatted below decorators) enable PyCharm to run a function whenever a given url
#which is denoted by the argument of "app.route" is reached. In these cases, each subsequent URL goes to another webpage that's being
#developed here in pycharm.

#The below code goes to the "about us" page if the web address is 127.0.0.1.../about

@app.route('/about')
def about():
    return render_template('aboutus.html')

#This code goes to the "login" page if the address is .../login.

@app.route('/login')
def login():
    return render_template('loginpage.html')

#This part is a bit trickier. Here, we execute SQL queries USING python WTIH html.

#If we go to /myteachers
@app.route('/myteachers')
def load_tables_teachers():
    con = sqlite3.connect("compsciproject.db")
#When we go to myteachers, we have Python connect to our SQL database with all of the data.
    sql = "SELECT * FROM teachers" #select everything in the teacher able
    cursor = con.execute(sql)
    rows = cursor.fetchall() #execute the SQL query using python

    return render_template('myteachers.html', items=rows) #sending this tablular data to a table in HTML

#If we go to teacher_classes/1, for example:
@app.route('/teacher_classes/<teacherID>') #this <> notation ensures that the teacherID is dynamic
def teacher_classes(teacherID):
    con = sqlite3.connect("compsciproject.db") #connects to the database
    sql_query_teacher_ids = f"SELECT c.classname, c.classID FROM classes c, teachers t, teacher_classes tc WHERE c.classID = tc.classID AND t.teacherID = tc.teacherID AND t.teacherID = {teacherID};"
    #using primary keys (teacher and class IDs) to select the classes of the teacher whose ID corresponds to the argument (using an F string for the last part)
    cursor = con.execute(sql_query_teacher_ids)
    rows = cursor.fetchall()

    return render_template('teacher_classes.html', items=rows) #same style as before

@app.route('/class_students/<classID>')
def student_classes(classID):
    con = sqlite3.connect("compsciproject.db") #connects to the database
    sql_query_student_classes = f" SELECT cs.studentID, s.firstname, s.lastname, cs.classID FROM students s, classes c, class_students cs WHERE s.studentID = cs.studentID AND cs.classID = c.classID AND cs.classID = {classID};"
    #using primary keys (teacher and class IDs) to select the classes of the teacher whose ID corresponds to the argument (using an F string for the last part)
    cursor = con.execute(sql_query_student_classes)
    rows = cursor.fetchall()

    return render_template('students.html', items=rows)  # same style as before

@app.route('/students/<studentid>')
def student_learning_outcomes(studentid):
    con = sqlite3.connect("compsciproject.db") #connects to the database
    sql_query_student_info = f" SELECT lo.studentID, lo.assignmentID, lo.LOID, lo.score, lo.classID FROM students s, classes c, class_students cs, LO_grades lo WHERE s.studentID = cs.studentID AND s.studentID = lo.studentID AND cs.classID = lo.classID AND lo.studentID = {studentid};"
    #using primary keys (teacher and class IDs) to select the classes of the teacher whose ID corresponds to the argument (using an F string for the last part)
    cursor = con.execute(sql_query_student_info)
    rows = cursor.fetchall()

    return render_template('lo_students.html', items=rows)  # same style as before

if __name__ == '__main__':
    app.run()


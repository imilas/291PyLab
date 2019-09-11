import sqlite3
import time
import hashlib

connection = None
cursor = None


def setupDatabase(path="unspecified.db"):
    print("created database at path:",path)        
    connect(path)
    define_tables()
    insert_data()    
    enroll_assign_grades()
    connection.close()
    
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return connection,cursor

def define_tables():
    global connection, cursor
    cursor.execute('''DROP TABLE IF EXISTS course''')
    cursor.execute('''DROP TABLE IF EXISTS student''')
    cursor.execute('''DROP TABLE IF EXISTS enroll''')
    course_query=   '''
                        CREATE TABLE course (
                                    course_id INTEGER,
                                    title TEXT,
                                    seats_available INTEGER,
                                    PRIMARY KEY (course_id)
                                    );
                    '''

    student_query=  '''
                        CREATE TABLE student (
                                    student_id INTEGER,
                                    name TEXT,
                                    PRIMARY KEY (student_id)
                                    );
                    '''

    enroll_query= '''
                    CREATE TABLE enroll (
                                student_id INTEGER,
                                course_id INTEGER,
                                enroll_date DATE,
                                grade TEXT,
                                PRIMARY KEY (student_id, course_id),
                                FOREIGN KEY(student_id) REFERENCES student(student_id),
                                FOREIGN KEY(course_id) REFERENCES course(course_id)
                                );
                '''

    cursor.execute(course_query)
    cursor.execute(student_query)
    cursor.execute(enroll_query)
    connection.commit()

    return

def insert_data():
    global connection, cursor

    insert_courses = '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                     '''

    insert_students =  '''
                        INSERT INTO student(student_id, name) VALUES
                                (1509106, 'Saeed'),
                                (1409106, 'Alex'),
                                (1609106, 'Mike');
                       '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return

def enroll_assign_grades():
    global connection, cursor

    cursor.execute('SELECT * FROM course;')
    all_courses = cursor.fetchall()

    cursor.execute('SELECT * FROM student;')
    all_students = cursor.fetchall()

    Grades = ['A', 'A', 'C', 'B', 'C', 'B', 'F', 'C', 'A']
    i=0

    for every_course in all_courses:
        for every_student in all_students:
            enroll(every_student[0], every_course[0])

            data = (Grades[i], every_student[0], every_course[0])
            cursor.execute('UPDATE enroll SET grade=? where student_id=? and course_id=?;', data)
            i += 1

    return

def enroll(student_id, course_id):
    global connection, cursor

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    crs_id = (course_id,)
    cursor.execute('SELECT seats_available FROM course WHERE course_id=?;', crs_id)
    seats_available = cursor.fetchone()

    if seats_available[0] > 0:
        data = (student_id, course_id, current_date)
        cursor.execute('INSERT INTO enroll (student_id, course_id, enroll_date) VALUES (?,?,?);', data) 
        cursor.execute('UPDATE course SET seats_available = seats_available - 1 where course_id=?;', crs_id)
    
    connection.commit()
    return
import mysql.connector

mydbase = mysql.connector.connect(
    host = 'localhost',
    database = 'system',
    user = 'root',
    password = ''
)

mycursor = mydbase.cursor(dictionary=True)

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS student(
        ID INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        stu_id VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        mobile INT,
        PRIMARY KEY(ID)
    )"""
)

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS fee(
        amount INT NOT NULL,
        type VARCHAR(255)
    )"""
)

mycursor.execute(
    """ALTER TABLE fee ADD COLUMN IF NOT EXISTS(
        student_id INT references student(ID)
    )
    """
)
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS course(
        course_name VARCHAR(255) NOT NULL,
        course_type VARCHAR(255) NOT NULL,
        course_id INT references student(ID)
    )"""
)
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS exams(
        exam_code VARCHAR(255) NOT NULL,
        exam_type VARCHAR(255) NOT NULL,
        exam_score INT NOT NULL,
        exam_id INT references student(ID)
    )"""
)
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS profile(
        picture VARCHAR(255),
        profile_id INT references student(ID)
    )"""
)
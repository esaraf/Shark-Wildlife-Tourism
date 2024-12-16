import mysql.connector

from secrets_1 import USER, PASSWORD


# Establish connection to the MySQL server 
connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD
)

# Create a cursor object 
cursor = connection.cursor()

# Create SWT Database 
cursor.execute("CREATE DATABASE IF NOT EXISTS SWT;")
print("Database SWT created successfully.")

# Use the newly created database
cursor.execute("USE SWT;")

# Create Participant table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Participant (
               ParticipantUUID CHAR(36) PRIMARY KEY, 
               ParticipantID INT, 
               GroupName VARCHAR(255),
               FirstName VARCHAR(255),
               LastName VARCHAR(255),
               EmailAddress VARCHAR(255),
               AgreedT3 TINYINT(1)
               );
               ''')

# Create Survey table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Survey (
               SurveyUUID CHAR(36) PRIMARY KEY,
               SurveyID CHAR(255),
               SurveyName VARCHAR(255),
               ParticipantUUID CHAR(36), 
               Date DATE,
               Trial INT, 
               IsOpen BOOLEAN,
               FOREIGN KEY (ParticipantUUID) REFERENCES Participant(ParticipantUUID)
               );
               ''')

# Create Question table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Question (
            QuestionUUID CHAR(36) NOT NULL PRIMARY KEY,  -- UUID as the primary key
            QuestionID VARCHAR(255) NOT NULL,           -- Human-readable ID
            SurveyID VARCHAR(255),                      -- Link to Survey
            ThemeID INT,
            QuestionType VARCHAR(255),
            Question TEXT
            );
            ''')

# Create Response table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Response (
               ResponseUUID CHAR(36) PRIMARY KEY,
               SurveyID VARCHAR(255),
               ParticipantUUID CHAR(36),
               QuestionUUID VARCHAR(255),
               Response TEXT,
               FOREIGN KEY (ParticipantUUID) REFERENCES Participant(ParticipantUUID),
               FOREIGN KEY (QuestionUUID) REFERENCES Question(QuestionUUID)
               );
               ''')



# Query to get a list of tables 
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

# Message to User 
print("Tables created successfully:")
for table in tables:
    print(f"- {table[0]}")

# Commit the changes and close the connection 
connection.commit()
cursor.close()
connection.close()
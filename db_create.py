import mysql.connector

from secrets_1 import USER, PASSWORD


# Establish connection to the MySQL server 
connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)

# Create a cursor object 
cursor = connection.cursor()

# Create Participant table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Participant (
               ParticipantID CHAR(36) PRIMARY KEY, 
               Sona_SurveyID INT, 
               GroupName VARCHAR(255),
               FirstName VARCHAR(255),
               LastName VARCHAR(255),
               EmailAddress VARCHAR(255)
               );
               ''')

# Create Survey table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Survey (
               SurveyID VARCHAR(255) PRIMARY KEY,
               SurveyName VARCHAR(255),
               ParticipantID CHAR(36), 
               StartDate DATE,
               EndDate DATE,
               Trial INT, 
               IsOpen BOOLEAN,
               FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID)
               );
               ''')

# Create Question table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Question (
               QuestionID VARCHAR(255) PRIMARY KEY,
               SurveyID VARCHAR(255),
               ThemeID INT,
               QuestionType VARCHAR(255),
               Question TEXT, 
               IsMandatory BOOLEAN,
               FOREIGN KEY (SurveyID) REFERENCES Survey(SurveyID)
               );
               ''')

# Create Response table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Response (
               ResponseID VARCHAR(255) PRIMARY KEY,
               ParticipantID CHAR(36),
               QuestionID VARCHAR(255),
               ResponseScale FLOAT,
               ResponseOPE TEXT,
               ResponseLikertID INT,
               ResponseMCID INT,
               FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID),
               FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID)
               );
               ''')


# Ensure that you have created necessary FK constraints to enforce referential integrity.
cursor.execute('''ALTER TABLE Response
ADD CONSTRAINT fk_participant
FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID),
ADD CONSTRAINT fk_question
FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID);
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
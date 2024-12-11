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
               AssignedInFieldID INT, 
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
               SurveyID CHAR(36) PRIMARY KEY,
               SurveyTypeID VARCHAR(255),
               SurveyName VARCHAR(255),
               ParticipantID CHAR(36), 
               Date DATE,
               Trial INT, 
               IsOpen BOOLEAN,
               FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID)
               );
               ''')

# Create Question table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Question (
            QuestionUUID CHAR(36) NOT NULL PRIMARY KEY,  -- UUID as the primary key
            QuestionID VARCHAR(255) NOT NULL,           -- Human-readable ID
            SurveyID VARCHAR(255),                      -- Foreign key to Survey
            ThemeID INT,
            QuestionType VARCHAR(255),
            Question TEXT,
            FOREIGN KEY (SurveyID) REFERENCES Survey(SurveyID)
            );
            ''')

# Create Response table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Response (
               ResponseID CHAR(36) PRIMARY KEY,
               ParticipantID CHAR(36),
               SurveyTypeID VARCHAR(255),
               QuestionUUID VARCHAR(255),
               ResponseValue TEXT,
               FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID),
               FOREIGN KEY (QuestionUUID) REFERENCES Question(QuestionUUID)
               );
               ''')


# Ensure that you have created necessary FK constraints to enforce referential integrity.
cursor.execute('''ALTER TABLE Response
ADD CONSTRAINT fk_participant
FOREIGN KEY (ParticipantID) REFERENCES Participant(ParticipantID),
ADD CONSTRAINT fk_question
FOREIGN KEY (QuestionUUID) REFERENCES Question(QuestionUUID);
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
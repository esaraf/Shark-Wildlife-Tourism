from typing import Any
import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract
import pytest
from test_data import get_participant_test_data

@pytest.fixture(scope="function")
def db_connection():
    # Setup database connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Molamola608!"
    )
    cursor = connection.cursor()

    # Create test database and use it
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_swt;")
    cursor.execute("USE test_swt;")

    # Create test_Participant table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_Participant (
            ParticipantUUID CHAR(36) PRIMARY KEY,
            ParticipantID INT,
            GroupName VARCHAR(255),
            FirstName VARCHAR(255),
            LastName VARCHAR(255),
            EmailAddress VARCHAR(255),
            AgreedT3 TINYINT(1)
        );
    ''')

    # Create test_Question table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_Question (
            QuestionUUID CHAR(36) NOT NULL PRIMARY KEY,  
            QuestionID VARCHAR(255) NOT NULL,           
            SurveyID VARCHAR(255),                      
            ThemeID INT,
            QuestionType VARCHAR(255),
            Question TEXT
                );
                   ''')

    connection.commit()
    yield cursor  # Provide the cursor to the test

    # Teardown: Clean up database after each test
    cursor.execute("DELETE FROM test_Participant;")
    connection.commit()
    cursor.close()
    connection.close()

def test_inserting_participants(db_connection: MySQLCursorAbstract | Any):
    # Get test data
    data = get_participant_test_data()

    for _, row in data.iterrows():
        db_connection.execute('''
            INSERT INTO test_Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
            VALUES  (%s, %s, %s, %s, %s, %s, %s);
        ''', (
            row['ParticipantUUID'],  
            row['ParticipantID'],   
            row['GroupName'],       
            row['FirstName'],       
            row['LastName'],       
            row['EmailAddress'],    
            row['AgreedT3']         
        ))

    # Expected: Data from participant_test_data
    expected = [(
        row['ParticipantUUID'],
        row['ParticipantID'],
        row['GroupName'],
        row['FirstName'],
        row['LastName'],
        row['EmailAddress'],
        row['AgreedT3']
    ) for _, row in data.iterrows()]

    # Query inserted data
    db_connection.execute('SELECT * FROM test_Participant;')
    actual = db_connection.fetchall()

    assert actual == expected, f"Expected {expected}, but got {actual}"


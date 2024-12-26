from typing import Any
import mysql.connector
from mysql.connector.abstracts import MySQLCursorAbstract
import pytest
from test_data import get_participant_test_data, get_survey_test_data

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

    # Creat test_Survey table
    # child deleted before parent row
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_Survey (
           SurveyUUID CHAR(36) PRIMARY KEY,
           SurveyID CHAR(255),
           SurveyName VARCHAR(255),
           ParticipantUUID CHAR(36),
           Date DATE,
           Trial INT,
           IsOpen BOOLEAN,
           FOREIGN KEY (ParticipantUUID) REFERENCES test_Participant(ParticipantUUID) ON DELETE CASCADE
        );
    ''')

    connection.commit()
    yield cursor  # Provide the cursor to the test

    # Teardown: Clean up database after each test
    cursor.execute("DELETE FROM test_Participant;")
    cursor.execute("DELETE FROM test_Question;")
    cursor.execute("DELETE FROM test_Survey;")
    connection.commit()
    cursor.close()
    connection.close()

def test_duplicates_ignored(db_connection: MySQLCursorAbstract | Any):
    """Test to ensure duplicate entries are ignored or prevented."""

    # Sample test data for participants
    participant_data = [
        {
            'ParticipantUUID': 'uuid1',
            'ParticipantID': 1,
            'GroupName': 'Shark',
            'FirstName': 'Alice',
            'LastName': 'Smith',
            'EmailAddress': 'alice@example.com',
            'AgreedT3': 1
        },
        {
            'ParticipantUUID': 'uuid1',  # Duplicate UUID
            'ParticipantID': 1,         # Duplicate ID
            'GroupName': 'Shark',
            'FirstName': 'Alice',
            'LastName': 'Smith',
            'EmailAddress': 'alice@example.com',
            'AgreedT3': 1
        }
    ]

    # Insert first entry
    db_connection.execute('''
        INSERT IGNORE INTO test_Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    ''', (
        participant_data[0]['ParticipantUUID'],
        participant_data[0]['ParticipantID'],
        participant_data[0]['GroupName'],
        participant_data[0]['FirstName'],
        participant_data[0]['LastName'],
        participant_data[0]['EmailAddress'],
        participant_data[0]['AgreedT3']
    ))


    # Try inserting the duplicate entry
    try:
        db_connection.execute('''
            INSERT IGNORE INTO test_Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (
            participant_data[1]['ParticipantUUID'],
            participant_data[1]['ParticipantID'],
            participant_data[1]['GroupName'],
            participant_data[1]['FirstName'],
            participant_data[1]['LastName'],
            participant_data[1]['EmailAddress'],
            participant_data[1]['AgreedT3']
        ))

        inserted_duplicate = True
    except mysql.connector.IntegrityError:
        inserted_duplicate = False

    # Assert that duplicate entry was not inserted
    assert not inserted_duplicate, "Duplicate entry was inserted, but it should have been ignored."

    # Fetch all rows from the database
    db_connection.execute('SELECT * FROM test_Participant;')
    rows = db_connection.fetchall()

    # Assert that only the first entry exists
    assert len(rows) == 1, f"Expected 1 entry, but found {len(rows)}."
    assert rows[0] == (
        participant_data[0]['ParticipantUUID'],
        participant_data[0]['ParticipantID'],
        participant_data[0]['GroupName'],
        participant_data[0]['FirstName'],
        participant_data[0]['LastName'],
        participant_data[0]['EmailAddress'],
        participant_data[0]['AgreedT3']
    ), "Inserted data does not match expected data."


def test_inserting_participants(db_connection: MySQLCursorAbstract | Any):
    # Get test data
    data = get_participant_test_data()

    for _, row in data.iterrows():
        db_connection.execute('''
            INSERT IGNORE INTO test_Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
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

def test_survey_linked_to_participant(db_connection: MySQLCursorAbstract | Any):
    # get test data
    survey_data = get_survey_test_data()
    participant_data = get_participant_test_data()

    # Insert participant data into the database
    for _, participant_row in participant_data.iterrows():
        db_connection.execute('''
            INSERT IGNORE INTO test_Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (
            participant_row['ParticipantUUID'],  
            participant_row['ParticipantID'],   
            participant_row['GroupName'],       
            participant_row['FirstName'],       
            participant_row['LastName'],       
            participant_row['EmailAddress'],    
            participant_row['AgreedT3']         
        ))
    
        # Insert survey data into the database
    for _, survey_row in survey_data.iterrows():
        db_connection.execute('''
            INSERT IGNORE INTO test_Survey (SurveyUUID, SurveyID, SurveyName, ParticipantUUID, Date, Trial, IsOpen)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (
            survey_row['SurveyUUID'],  
            survey_row['SurveyID'],   
            survey_row['SurveyName'],       
            survey_row['ParticipantUUID'],  
            survey_row['Date'],             
            survey_row['Trial'],            
            survey_row['IsOpen']            
        ))

     # Verify survey is linked to a valid participant
    for _, survey_row in survey_data.iterrows():
        participant_uuid = survey_row['ParticipantUUID']
        survey_uuid = survey_row['SurveyUUID']

        # Query to confirm the link
        db_connection.execute('''
            SELECT ParticipantUUID FROM test_Survey WHERE SurveyUUID = %s;
        ''', (survey_uuid,))
        result = db_connection.fetchone()

        # Assert that the participant UUID matches the expected value
        assert result is not None, f"Survey {survey_uuid} not linked to any participant"
        assert result[0] == participant_uuid, f"Survey {survey_uuid} is not correctly linked to Participant {participant_uuid}"
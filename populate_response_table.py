import pandas as pd
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, QUESTION_CSV
from secrets_1 import SHARK_RESPONSE_T0, SHARK_RESPONSE_T1, SHARK_RESPONSE_T2, SHARK_RESPONSE_T3
from secrets_1 import DOCUMENTARY_RESPONSE_T0, DOCUMENTARY_RESPONSE_T1, DOCUMENTARY_RESPONSE_T2, DOCUMENTARY_RESPONSE_T3
from secrets_1 import CONTROL_T0, CONTROL_T2, CONTROL_T3

# TODO: Extrapolate response file paths 

#response_file_path = SHARK_RESPONSE_T0
#response_file_path = SHARK_RESPONSE_T1
#response_file_path = SHARK_RESPONSE_T2
#response_file_path = SHARK_RESPONSE_T3

response_file_path = DOCUMENTARY_RESPONSE_T0
#response_file_path = DOCUMENTARY_RESPONSE_T1
#response_file_path = DOCUMENTARY_RESPONSE_T2
#response_file_path = DOCUMENTARY_RESPONSE_T3

#response_file_path = CONTROL_RESPONSE_T0
#response_file_path = CONTROL_RESPONSE_T2
#response_file_path = CONTROL_RESPONSE_T3

response_df = pd.read_csv(response_file_path)

question_file_path = QUESTION_CSV
question_df = pd.read_csv(question_file_path)
valid_question_ids = set(question_df['QuestionID'])

# Pull the Demographic info from the response table and put it into the participant table...

connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)

cursor = connection.cursor()

def get_question_uuid(question_id, survey_id):
    ''' Fetch QuestionUUID based on questionID and SurveyID '''
    try:
        query = """
            SELECT QuestionUUID FROM Question
            WHERE QuestionID = %s AND SurveyID = %s
        """
        cursor.execute(query, (question_id, survey_id))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"Warning: No QuestionUUID found for SurveyID {survey_id} and QuestionID{question_id}")
    finally:
        cursor.fetchall()

# Function to fetch ParticipantUUID based on ParticipantID
def get_participant_uuid(participant_id):
    try:
        cursor.execute("SELECT ParticipantUUID FROM Participant WHERE ParticipantID = %s", (participant_id,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the ParticipantUUID
        else:
            print(f"Warning: No ParticipantUUID found for ParticipantID: {participant_id}")
            return None
    except mysql.connector.Error as err:
        print(f"Error fetching ParticipantUUID: {err}")
        return None
    finally:
        cursor.fetchall()

# Function to fetch SurveyUUID based on SurveyID and ParticipantUUID
def get_survey_uuid(survey_id, participant_uuid):
    try:

        query = """
            SELECT SurveyUUID FROM Survey
            WHERE SurveyID = %s AND ParticipantUUID = %s
        """
        cursor.execute(query, (survey_id, participant_uuid))
        result = cursor.fetchone()
        if result:
            return result[0]
        else: 
            print(f"Warning: No SurveyUUID found for SurveyID {survey_id}")
    
    except mysql.connector.Error as err:
        print(f"Error fetching ParticipantUUID: {err}")
        return None
    finally:
        cursor.fetchall()

for index, row in response_df.iterrows():
    # Get the survey and participant information from the row
    survey_id = row.get('SurveyID')
    participant_id = row.get('ParticipantID')
    
    # Validate required data is present
    if not survey_id or not participant_id:
        print(f"Skipping row {index}: Missing SurveyID or ParticipantID")
        continue

    # Fetch the ParticipantUUID using the ParticipantID
    participant_uuid = get_participant_uuid(participant_id)
    if not participant_uuid:
        print(f"Skipping row {index}: No ParticipantUUID found for ParticipantID {participant_id}")
        continue

    # Fetch the SurveyUUID using the SurveyID and ParticipantUUID
    survey_uuid = get_survey_uuid(survey_id, participant_uuid)
    if not survey_uuid:
        print(f"Skipping row {index}: No SurveyUUID found for SurveyID {survey_id} and ParticipantUUID {participant_uuid}")
        continue

    # Iterate over the responses for the current row
    for question_id, response in row.items():
        # Skip columns that are not valid question IDs
        if question_id not in valid_question_ids:
            continue

        # Fetch the QuestionUUID for the given QuestionID and SurveyID
        question_uuid = get_question_uuid(question_id, survey_id)
        if not question_uuid:
            print(f"Skipping response: No QuestionUUID found for QuestionID {question_id}, SurveyID {survey_id}")
            continue

        # Generate a unique ResponseUUID
        response_uuid = str(uuid.uuid4())

        # Insert the response into the database
        try:
            insert_query = """
                INSERT INTO Response (ResponseUUID, SurveyUUID, ParticipantUUID, QuestionUUID, Response)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (response_uuid, survey_uuid, participant_uuid, question_uuid, response))
            print(f"Inserted response for ParticipantID {participant_id}, QuestionID {question_id}")
        except mysql.connector.Error as err:
            print(f"Error inserting response for ParticipantID {participant_id}, QuestionID {question_id}: {err}")

print("Responses inserted successfully!")

connection.commit()
cursor.close()
connection.close()
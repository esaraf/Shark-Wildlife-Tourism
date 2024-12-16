import pandas as pd
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, SHARK_RESPONSE_T0, QUESTION_CSV
from utils import filter_non_question_fields

response_file_path = SHARK_RESPONSE_T0
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
    
    query = """
        SELECT QuestionUUID FROM Question
        WHERE QuestionID = %s AND SurveyID = %s
    """
    cursor.execute(query, (question_id, survey_id))
    result = cursor.fetchone()
    return result[0] if result else None

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


# Process Responses
for index, row in response_df.iterrows():
    survey_id = row['SurveyID']
    participant_id = row['ParticipantID']

    # Fetch ParticipantUUID using ParticipantID
    participant_uuid = get_participant_uuid(participant_id)
    if not participant_uuid:
        print(f"Skipping row {index} due to missing ParticipantUUID for ParticipantID: {participant_id}")
        continue  # Skip if no matching ParticipantUUID is found
    
    for question_id, response_value in row.items():
        # Skip if question_id is not in valid_question_ids
        if question_id not in valid_question_ids:
            continue
        
        # Fetch Question UUID 
        question_uuid = get_question_uuid(question_id, survey_id)
        if question_uuid:
            response_uuid = str(uuid.uuid4())
            
            try:
                insert_query = """
                    INSERT INTO Response (ResponseUUID, SurveyID, QuestionUUID, Response)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (response_uuid, survey_id, question_uuid, response_value))
                print(f"Inserted response for ParticipantID {participant_id}, QuestionID {question_id}")
                
            except mysql.connector.Error as err:
                print(f"Error inserting response: {err}")
        else:
            print(f"Warning: No QuestionUUID found for QuestionID: '{question_id}' and SurveyID: '{survey_id}'")


print("Responses inserted successfully!")

connection.commit()
cursor.close()
connection.close()
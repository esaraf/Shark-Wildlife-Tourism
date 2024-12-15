import pandas as pd
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, SHARK_RESPONSE_T0, QUESTION_CSV

response_file_path = SHARK_RESPONSE_T0
response_df = pd.read_csv(response_file_path)

connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)
cursor = connection.cursor()
# Populate Response Table
for index, row in response_df.iterrows():
    # Retrieve ParticipantID from Participant table: 
    participant_id = row['ParticipantID']

    # Query to fetch group information 
    cursor.execute('''
        SELECT GroupName FROM Participant WHERE ParticipantID = %s
        ''', (participant_id,))
    result = cursor.fetchone()
    
    if not result:
        print(f"Warning: No ParticipantID found for ParticipantID {participant_id}")
        continue  # Skip if no matching ParticipantID is found

    group_name = result[0]
    print(f"ParticipantID {participant_id} in group {group_name}")

    responseUUID = str(uuid.uuid4())

    # Fetch SurveyUUID
    survey_id = row['SurveyID']
    try: 

        cursor.execute('''
        SELECT SurveyUUID
        FROM Survey
        WHERE SurveyID = %s AND ParticipantID = %s 
        ''', (survey_id, participant_id,))
        survey_result = cursor.fetchone()

        survey_uuid = survey_result[0]
        print(f"SurveyUUID for SurveyID {survey_id} and ParticipantID {participant_id}: {survey_uuid}")

        if not survey_result:
            print(f"Warning: No SurveyUUID found for SurveyID {survey_id} and ParticipantID {participant_id}") 
            continue
    
    except mysql.connector.Error as err:
        print(f"Error fetching SurveyUUID: {err}")
        continue
    
    try: # Query to fetch questionID

    try:
        cursor.execute('''
            INSERT INTO Response (ResponseUUID, SurveyUUID, QuestionID, Response)
            VALUES (%s, %s, %s, %s)
            ''', (responseUUID, participant_id, question_id, str(response)))
                      

    except mysql.connector.Error as err:
        print(f"Error: {err}")


print("Responses inserted successfully!")

connection.commit()
cursor.close()
connection.close()
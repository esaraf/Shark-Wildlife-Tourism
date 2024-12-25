import pandas as pd
import mysql.connector
import uuid
from tqdm import tqdm # Terminal Progress Bar

from secrets_1 import USER, PASSWORD, SURVEY_CSV # TODO: Bring data out of secrets and into data_file
# from utils import filter_non_question_fields

survey_file_path = SURVEY_CSV
survey_df = pd.read_csv(survey_file_path)

# Connect to the database
connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)

cursor = connection.cursor(buffered=True) # Override lazy load of one row


for index, row in survey_df.iterrows():
    surveyUUID = str(uuid.uuid4()) # Generate a UUID for each survey
    survey_id = row['SurveyID']
    survey_name = row['SurveyName']
    participant_id = row['ParticipantID']
    date = row['Date']
    trial = row['Trial']
    is_open = row['IsOpen']

    # Insert data into the Survey table
    try:
        # Fetch ParticipantUUID based on ParticipantID
        fetch_participant_query = "SELECT ParticipantUUID FROM Participant WHERE ParticipantID = %s"
        cursor.execute(fetch_participant_query, (participant_id,))
        result = cursor.fetchone()

        if result:
            participant_uuid = result[0]
        else:
            print(f"ParticipantID {participant_id} not found in Participant table.")
            continue  # Skip this row and move to the next
        
        cursor.execute('''
            INSERT IGNORE INTO Survey (SurveyUUID, SurveyID, SurveyName, ParticipantUUID, Date, Trial, IsOpen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
                       ''', (surveyUUID, survey_id, survey_name, participant_uuid, date, trial, is_open))
        print(f"Inserted survey: {survey_name} with ID {surveyUUID}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Skipping row {index}")

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Survey table populated successfully.")

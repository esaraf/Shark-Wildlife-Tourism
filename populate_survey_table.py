import pandas as pd
import mysql.connector
import uuid

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

cursor = connection.cursor()

# Query to fetch ParticipantUUID based on ParticipantID
fetch_participant_query = "SELECT ParticipantUUID FROM Participant WHERE ParticipantUUID = %s"

# Insert data into the Survey table
insert_query = """
INSERT INTO Survey (
    SurveyUUID, Name, SurveyTypeID, ParticipantUUID, Date, Trial, IsOpen
) VALUES (%s, %s, %s, %s, %s, %s)
"""

# Loop through each row in the survey DataFrame
for _, row in survey_df.iterrows():
    # Fetch the ParticipantUUID
    cursor.execute(fetch_participant_query, (row['ParticipantUUID'],))
    result = cursor.fetchone()
    
    if result:
        participant_uuid = result[0]  # Extract the ParticipantUUID from the result
        
        # Insert the survey row
        cursor.execute(insert_query, (
            str(uuid.uuid4()),       # Generate a new SurveyUUID
            row['Name'],             # Name from the CSV
            row['SurveyTypeID'],     # SurveyTypeID from the CSV
            participant_uuid,        # Use the fetched ParticipantUUID
            row['Date'],             # StartDate from the CSV
            row['Trial'],            # Trial from the CSV
            row['IsOpen']            # IsOpen from the CSV
        ))
    else:
        print(f"Warning: ParticipantID {row['ParticipantID']} not found in Participant table.")

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Survey table populated successfully.")

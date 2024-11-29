import pandas as pd
import mysql.connector
import uuid

from question_mapping import combined_dict_mapping

from secrets_1 import USER, PASSWORD, SHARK_RESPONSE_T0
from utils import filter_non_question_fields

file_path = SHARK_RESPONSE_T0

df = pd.read_csv(file_path)

# Filter out non-question fields
filtered_headers = filter_non_question_fields(df.columns.tolist())

connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)
cursor = connection.cursor()

# Populate 
for index, row in df.iterrows():
    # Retrieve ParticipantID from Participant table: 
    cursor.execute('''
        SELECT ParticipantID FROM Participant WHERE EmailAddress = %s
        ''', (row['EmailAddress'],))
    
    result = cursor.fetchone()
    
    if not result:
        print(f"Error: No ParticipantID found for EmailAddress {row['EmailAddress']}")
        continue  # Skip if no matching ParticipantID is found

    participant_id = result[0]

    for question_text, response_value, in row.items():
        print(question_text)
        print(response_value)
        # Skip Non-response columns
        if question_text in ['EmailAddress', 'GroupName', 'FirstName', 'LastName']:
            continue

        # Map the question_text to question_id
        question_id = combined_dict_mapping.get(question_text)
        if not question_id:
            print(f"Warning: No QuestionID for {question_text}")
            continue 

        # Generate a uuid for responseID
        response_id = str(uuid.uuid4())

        # Insert Response into Response Table 
        cursor.execute('''
                INSERT INTO Response (ResponseID, ParticipantID, QuestionID, ResponseValue)
                VALUES (%s, %s, %s, %s)
                ''', (response_id, participant_id, question_id, str(response_value)))

connection.commit()
cursor.close()
connection.close()

print("Responses inserted successfully!")
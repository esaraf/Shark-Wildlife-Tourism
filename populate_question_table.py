import pandas as pd
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, QUESTION_CSV # TODO: Bring data out of secrets and into data_file

question_file_path = QUESTION_CSV

question_df = pd.read_csv(question_file_path)

connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)

cursor = connection.cursor()

# SQL query to insert data into the questions table
insert_query = """
INSERT INTO Question (QuestionUUID, QuestionID, SurveyTypeID, ThemeID, QuestionType, Question)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Track inserted QuestionIDs
inserted_question_ids = []

for _, row in question_df.iterrows():
    question_uuid = str(uuid.uuid4())  # Generate a UUID
    cursor.execute(insert_query, (
        question_uuid,  # Insert the UUID
        row['QuestionID'],
        row['SurveyTypeID'],
        row['ThemeID'],
        row['QuestionType'],
        row['Question']
    ))
    inserted_question_ids.append(row['QuestionID'])  # Track the inserted QuestionID


# Commit the transaction
connection.commit()

print(f"Inserted {len(inserted_question_ids)} rows into the questions table.")
print("Inserted QuestionIDs:")
print(", ".join(inserted_question_ids))

connection.commit()
cursor.close()
connection.close()
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

for index, row in question_df.iterrows():
    questionUUID = str(uuid.uuid4())
    question_id = row['QuestionID']
    survey_id = row['SurveyID']
    theme_id = row['ThemeID']
    question_type = row['QuestionType']
    question = row['Question']

    try:
        cursor.execute('''
            INSERT IGNORE INTO Question (QuestionUUID, QuestionID, SurveyName, ThemeID, QuestionType, Question)
            VALUES (%s, %s, %s, %s, %s, %s)
                       ''', (questionUUID, question_id, survey_id, theme_id, question_type,question))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Skipping row {index}")


# Commit the transaction
connection.commit()

print('Data insertion completed')

connection.commit()
cursor.close()
connection.close()
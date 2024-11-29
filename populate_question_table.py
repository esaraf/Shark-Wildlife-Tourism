import pandas as pd
import mysql.connector
import uuid

from question_mapping import combined_dict_mapping

from secrets_1 import USER, PASSWORD, SHARK_RESPONSE_T0
from utils import filter_non_question_fields

connection = mysql.connector.connect(
    host='localhost',
    user=USER,
    password=PASSWORD,
    database='SWT'
)
cursor = connection.cursor()

for question_text, question_id in combined_dict_mapping.items():
    cursor.execute('''
                    INSERT INTO Question (QuestionID, QuestionText)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE QuestionText = VALUES(QuestionText)
                   ''', (question_id, question_text)
                   )

connection.commit()
cursor.close()
connection.close()

print("Question table populated successfully!")
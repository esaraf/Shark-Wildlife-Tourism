import pandas as pd 
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, PARTICIPANT_TABLE

file_path = PARTICIPANT_TABLE
df = pd.read_csv(file_path)

# Establish connection to database 
connection = mysql.connector.connect(
    host = 'localhost',
    user=USER, 
    password=PASSWORD,
    database='SWT'
)

cursor = connection.cursor()

# Data insertion code below: 
# Iterate existing Dataframe and insert each row with a UUID 

for index, row in df.iterrows():
    participantID = str(uuid.uuid4()) # Generate a UUID for each participant
    assigned_in_field_id = row['AssignedInFieldID'] if pd.notna(row['AssignedInFieldID']) else None
    group_name = row['GroupName']
    first_name = row['FirstName'] if pd.notna(row['FirstName']) else None
    last_name = row['LastName'] if pd.notna(row['LastName']) else None
    email_address = row['EmailAddress']

    # Insert data into the Participant table 
    try: 
        cursor.execute('''
            INSERT INTO Participant (ParticipantID, AssignedInFieldID, GroupName, FirstName, LastName, EmailAddress)
            VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (participantID, assigned_in_field_id, group_name, first_name, last_name, email_address))
        print(f"Inserted participant: {first_name} {last_name} with ID {participantID}")
    except mysql.connector.Error as err: 
        print(f"Error: {err}")
        print(f"Skipping row {index}")

connection.commit()
        
cursor.close()
connection.close()

print("Data insertion completed.")
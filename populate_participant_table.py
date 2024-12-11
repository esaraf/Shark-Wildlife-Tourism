import pandas as pd 
import mysql.connector
import uuid

from secrets_1 import USER, PASSWORD, PARTICIPANT_CSV

participant_file_path = PARTICIPANT_CSV
df = pd.read_csv(participant_file_path)

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
    participantUUID = str(uuid.uuid4()) # Generate a UUID for each participant
    participant_id = row['ParticipantID'] if pd.notna(row['ParticipantID']) else None
    group_name= row['GroupName']
    first_name = row['FirstName'] if pd.notna(row['FirstName']) else None
    last_name = row['LastName'] if pd.notna(row['LastName']) else None
    email_address = row['EmailAddress']
    agree_to_T3 = row['AgreedT3']

    # Insert data into the Participant table 
    try: 
        cursor.execute('''
            INSERT INTO Participant (ParticipantUUID, ParticipantID, GroupName, FirstName, LastName, EmailAddress, AgreedT3)
            VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (participantUUID, participant_id, group_name, first_name, last_name, email_address, agree_to_T3))
        print(f"Inserted participant: {first_name} {last_name} with ID {participantUUID}")
    except mysql.connector.Error as err: 
        print(f"Error: {err}")
        print(f"Skipping row {index}")

connection.commit()
        
cursor.close()
connection.close()

print("Data insertion completed.")
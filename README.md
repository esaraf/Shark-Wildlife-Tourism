# Shark Wildlife Tourism

This repository contains tools and scripts for analyzing survey responses related to shark wildlife tourism, conservation behavior, and participant attitudes across multiple time points and survey groups. 

## Table of Contents 
1. Project Overview 
2. Features 
3. Setup and Installation 
4. Data Structure 
5. Scripts and Usage 
6. Tests and Validation 
7. Key Statistics and Insights 
8. Contributing 
9. License 

## Project Overview 

This project collects and processes survey data to analyze participants' behaviors, attitudes, and knowledge related to shark wildlife tourism. The data spans multiple time points (e.g., initial survey, post-activity survey, follow-ups) and includes various groups (e.g., control, documentary viewers, and participants in shark-related activities). 

### Key Objectives:
- Identify changes in conservation-related behaviors and attitudes over time.
- Analyze the impact of shark wildlife tourism on emotional and behavioral engagement.
- Generate insights to inform conservation strategies.

## Features 
- **Database Management:** Scripts to populate and manage MySQL tables for participants, questions, and responses.
- **Data Cleaning:** Utilities for filtering and validating survey questions and responses.
- **Question Mapping:** Dictionaries for mapping survey questions to unique identifiers and time points.
- **Survey Response Analysis:** Tools for statistical analysis of Likert-scale, multiple choice, and open-ended responses.
- **Data Visualization:** Generate visual representations of behavioral trends and demographic insights.

## Setup and Installation 

### Prerequisites 
- Python 3.x
- MySQL server
- Required Python libraries (see `requirements.txt`)

 ### Installation 
1. Clone the repository
```
git clone https://github.com/esaraf/Shark-Wildlife-Tourism.git
cd Shark-Wildlife-Tourism
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Set up your MySQL database
- Create a database named `SWT`
- Run `db_create.py` to initialize tables.

4. Configure database credentials: 
- Update the `secrets_1.py` file with your MySQL `USER`, `PASSWORD`, and other sensitive information.
  
## Data Structure 
### Tables 
- **Participant:** Stores participant details (e.g., `ParticipantID`, `GroupName`, `EmailAddress`).
- **Question:** Maps questions to `QuestionID`.
- **Response:** Links participants and their answers to `QuestionID`.

### Question Mapping 
- `combined_dict_mapping`: Maps survey questions to `QuestionID` across multiple time points and groups (e.g., T0, T1).
- Example:
``` python
{
('How frequently do you engage in conservation activities?', 'T0'):'1_1A'),
('How frequently do you engage in conservation activities?','T1'):'1_1B')
}
```

## Scripts and Usage
### Key Scripts 
1. `db_create.py`:
   - Initializes the MySQL database schema.
   - Run with: `python db_create.py`
2. `populate_participant_table.py`:
   - Adds participants to the database with UUIDs.
   - Run with `python populate_participant_table.py`
3. `populate_survey_table.py`:
   - Adds completed surveys to the database with UUIDs.
   - Run with `python populate_survey_table.py`
3. `populate_question_table.py`:
   - Populates the `Question` table from a CSV.
   - Run with: `python populate_question_table.py`
4. `populate_response_table.py`:
   - Processes survey responses and inserts them into the `Response` table.
   - Run with: `python populate_response_table.py`
5. `test_question_mapping.py`
   - Validates that questions and mappings match between the CSV and dictionary
   - Run with: `pytest`

### Utility Scripts: 
- `utils.py`:
  - Includes helper functions like `filter_non_question_fields` for cleaning data. 

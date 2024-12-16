import mysql.connector

def filter_non_question_fields(headers):
        """Filter out non-question fields from the CSV headers."""
        non_question_fields = {'Timestamp', 'ID', 'EmailAddress'}  # Add any other non-question fields here
        return [header for header in headers if header not in non_question_fields]

def get_question_uuid(question_id, survey_id):
    ''' Fetch QuestionUUID based on questionID and SurveyID '''
    
    query = """
        SELECT QuestionUUID FROM Question
        WHERE QuestionID = %s AND SurveyID = %s
    """
    cursor.execute(query, (question_id, survey_id))
    result = cursor.fetchone()
    return result[0] if result else None
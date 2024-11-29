def filter_non_question_fields(headers):
        """Filter out non-question fields from the CSV headers."""
        non_question_fields = {'Timestamp', 'ID', 'EmailAddress'}  # Add any other non-question fields here
        return [header for header in headers if header not in non_question_fields]
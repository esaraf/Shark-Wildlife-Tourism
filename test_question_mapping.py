import unittest
import pandas as pd
from question_mapping import documentary_question_mapping_T0, documentary_question_mapping_T1, documentary_question_mapping_T2_and_3,  shark_question_mapping_T0, shark_question_mapping_T1, shark_question_mapping_T2, shark_question_mapping_T3, control_question_mapping_T0, control_question_mapping_T2_and_T3
from question_type_mapping import question_type_mapping
from utils import filter_non_question_fields

class TestQuestionMapping(unittest.TestCase):

    def test_question_to_id_mapping_to_documentary_group(self):
        """Tests that all questions in the documentary question dictionary are mapped to a valid QuestionID"""
        for question, question_id in documentary_question_mapping_T0.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T0")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T0")
        
        for question, question_id in documentary_question_mapping_T1.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T1")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T1")

        for question, question_id in documentary_question_mapping_T2_and_3.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T2 and T3")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T2 and T3")

        print("All questions mapped to a QuestionID in documentary")
    
    def test_question_to_id_mapping_to_shark_group(self):
        """Tests that all questions in the shark question dictionary are mapped to a valid QuestionID"""
        for question, question_id in shark_question_mapping_T0.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T0")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T0")
        
        for question, question_id in shark_question_mapping_T1.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T1")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T1")
        
        for question, question_id in shark_question_mapping_T2.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T2")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T2")
        
        for question, question_id in shark_question_mapping_T3.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T3")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} inT3")

        print("All questions mapped to a QuestionID in shark group")

    def test_question_to_id_mapping_to_control_group(self):
        """Tests that all questions in the shark question dictionary are mapped to a valid QuestionID"""
        for question, question_id in control_question_mapping_T0.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T0")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T0")

        for question, question_id in control_question_mapping_T2_and_T3.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question} in T2 and T3")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question} in T2 and T3")

        print("All questions mapped to a QuestionID in control group")

    def test_identical_questionID_across_timepoints(self):
        """Test that questions repeated across time points have the same QuestionID"""
        # Define questions that are repeted across timepoints that have the same QID
        repeated_question = [
            ("1. How frequently do you engage in each of these marine conservation activities? [Read environmental or conservation materials, e.g., books, blogs, articles, etc.]",
            "1. After viewing the film, how frequently do you intend to engage in each marine conservation activity? [Read environmental or conservation materials, e.g., books, blogs, articles, etc.]")
        ]

        combined_dict_mapping = {
            **shark_question_mapping_T0,
            **shark_question_mapping_T1,
            **shark_question_mapping_T2,
            **shark_question_mapping_T3,
            **documentary_question_mapping_T0,
            **documentary_question_mapping_T1,
            **documentary_question_mapping_T2_and_3,
            **control_question_mapping_T0,
            **control_question_mapping_T2_and_T3
        }

        for T0, T1 in repeated_question:
            T0_id = combined_dict_mapping.get(T0)
            T1_id = combined_dict_mapping.get(T1)
            self.assertEqual(T0_id, T1_id, f"QuestionIDs do not match for {T0_id} and {T1_id}")


    def test_all_question_ids_are_classified_by_question_type(self):
        ''''Test that all questions are classified by appropriate types'''
        # Combine all dictionaries into one: 
        combined_dict_mapping = {
            **shark_question_mapping_T0,
            **shark_question_mapping_T1,
            **shark_question_mapping_T2,
            **shark_question_mapping_T3,
            **documentary_question_mapping_T0,
            **documentary_question_mapping_T1,
            **documentary_question_mapping_T2_and_3,
            **control_question_mapping_T0,
            **control_question_mapping_T2_and_T3
        }

        # Extract IDs from combined_dict_mapping
        all_ids = set(combined_dict_mapping.values())

        # Extract IDs from question_type_mapping 
        sorted_ids = set()

        for question_type, question_ids in question_type_mapping.items():

            for question_id in question_ids:
                sorted_ids.add(question_id)
        
        missing_classification = all_ids - sorted_ids

        print(f'These IDs: {missing_classification} need to be sorted.')

        self.assertEqual(missing_classification, set())


class TestActualtoRecordedSharkGroupQuestionText(unittest.TestCase):

    def setUp(self):
        # Load the CSV file with the actual survey responses
        self.survey_file_path = "/Users/elizabethsaraf/Desktop/Shark_Responses_T0.csv"
        self.survey_questions = pd.read_csv(self.survey_file_path)

        # Extract column headers starting from the second column (skipping Timestamp)
        csv_headers = self.survey_questions.columns[1:]
        self.actual_questions = set(filter_non_question_fields(csv_headers))

        # Use the imported dictionary for your mapping
        self.question_mapping = shark_question_mapping_T0

    

    def test_question_text_matches_actual_survey_question_text(self):
        """Test that questions in dictionary match actual survey questions from the CSV"""
        dictionary_questions = set(self.question_mapping.keys())

        # Compare dictionary keys to the actual questions in the CSV
        missing_from_csv = dictionary_questions - self.actual_questions
        extra_in_csv = self.actual_questions - dictionary_questions

        # Assert no discrepancies
        self.assertTrue(
            not missing_from_csv,
            f"The following questions are in the shark dictionary but not in the CSV: {missing_from_csv}"
        )

        self.assertTrue(
            not extra_in_csv,
            f"The following questions are in the CSV but not in the shark dictionary: {extra_in_csv}"
        )


if __name__=='__main__':
    unittest.main()
                                
                          
            


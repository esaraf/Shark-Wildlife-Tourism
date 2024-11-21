import unittest
import pandas as pd
from question_mapping import documentary_question_mapping, shark_question_mapping, control_question_mapping
from question_type_mapping import question_type_mapping


class TestQuestionMapping(unittest.TestCase):

    def test_question_to_id_mapping_to_documentary_group(self):
        """Tests that all questions in the documentary question dictionary are mapped to a valid QuestionID"""
        for question, question_id in documentary_question_mapping.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question}")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question}")


        print("All questions correctly mapped to QuestionIDs in documentary")
    
    def test_question_to_id_mapping_to_shark_group(self):
        """Tests that all questions in the shark question dictionary are mapped to a valid QuestionID"""
        for question, question_id in shark_question_mapping.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question}")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question}")


        print("All questions correctly mapped to QuestionIDs in shark group")

    def test_question_to_id_mapping_to_control_group(self):
        """Tests that all questions in the shark question dictionary are mapped to a valid QuestionID"""
        for question, question_id in control_question_mapping.items():
            self.assertIsNotNone(question_id, f"Missing QuestionID for {question}")
            self.assertNotEqual(question_id, "", f"Empty QuestionID for {question}")

        print("All questions correctly mapped to QuestionIDs in control group")

    def test_identical_questionID_across_timepoints(self):
        """Test that questions repeated across time points have the same QuestionID"""
        # Define questions that are repeted across timepoints that have the same QID
        repeated_question = [
            ("1. How frequently do you engage in each of these marine conservation activities? [Read environmental or conservation materials, e.g., books, blogs, articles, etc.]",
            "1. After viewing the film, how frequently do you intend to engage in each marine conservation activity? [Read environmental or conservation materials, e.g., books, blogs, articles, etc.]")
        ]

        combined_dict_mapping = {
            **shark_question_mapping,
            **documentary_question_mapping,
            **control_question_mapping,
        }

        for T0, T1 in repeated_question:
            T0_id = combined_dict_mapping.get(T0)
            T1_id = combined_dict_mapping.get(T1)
            self.assertEqual(T0_id, T1_id, f"QuestionIDs do not match for {T0_id} and {T1_id}")


    def test_all_question_ids_are_classified_by_question_type(self):
        ''''Test that all questions are classified by appropriate types'''
        # Combine all dictionaries into one: 
        combined_dict_mapping = {
            **shark_question_mapping,
            **documentary_question_mapping,
            **control_question_mapping,
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



if __name__=='__main__':
    unittest.main()
                                
                          
            


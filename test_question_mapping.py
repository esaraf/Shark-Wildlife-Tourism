import unittest
import pandas as pd
from question_mapping import documentary_question_mapping, shark_question_mapping, control_question_mapping


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

        for T0, T1 in repeated_question:
            T0_id = documentary_question_mapping.get(T0)
            T1_id = documentary_question_mapping.get(T1)
            self.assertEqual(T0_id, T1_id, f"QuestionIDs do not match for {T0_id} and {T1_id}")

if __name__=='__main__':
    unitttest.main()
                                
                          
            


import unittest
import os 

from main import preprocess_data

# python3 -m unittest test_preprocess_data.py

class PreprocessDataTest(unittest.TestCase):
    def setUp(self): 
        self.input_file = 'test_input.txt'
        self.output_file = 'test_output.txt'
        self.min_length = 10
        self.max_length = 50
        self.token_length_limit = 20

        # Create test input file
        with open(self.input_file, 'w') as file: 
            file.write("Short.\n")
            file.write("This is a line within the specified length limits.\n")
            file.write("This is a very long line that exceeds the maximum length limit set for this test case.\n")

    # Remove test files
    def tearDown(self): 
        os.remove(self.input_file)
        os.remove(self.output_file)

    def test_preprocess_data(self):
        preprocess_data(self.input_file, self.output_file, self.min_length, self.max_length, self.token_length_limit)
        
        # Test if the output file has been created
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as file: 
            lines = file.readlines()
            for line in lines: 
                # Check if the line length is within the specified limits
                self.assertGreaterEqual(len(line), self.min_length)
                self.assertLessEqual(len(line), self.max_length)
                # Check if the newline character has been replaced
                self.assertNotIn('\n', line)
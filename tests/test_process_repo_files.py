import unittest
import shutil
import os 

from main import process_repo_files

class PreprocessRepoFilesTest(unittest.TestCase):
    def setUp(self):
        # Create test input files and directory
        self.python_file = 'test_python_file.py'
        self.non_python_file = 'test_non_python_file.txt'
        self.directory = 'test_directory'

        # Get the directory of the current script
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path for the directory
        self.directory_path = os.path.join(current_script_dir, self.directory)

        # Create directory
        os.mkdir(self.directory_path)

        # Construct full paths for the files
        self.python_file_path = os.path.join(self.directory_path, self.python_file)
        self.non_python_file_path = os.path.join(self.directory_path, self.non_python_file)
        
        # Create files
        with open(self.python_file_path, 'w') as file:
            file.write("This is a python file.")
        with open(self.non_python_file_path, 'w') as file: 
            file.write("This is a non-python file.")

    def tearDown(self):
        if os.path.exists(self.python_file_path):
            os.remove(self.python_file_path)
        if os.path.exists(self.non_python_file_path):
            os.remove(self.non_python_file_path)
        
        # Remove the directory if it exists
        if os.path.exists(self.directory_path):
            os.rmdir(self.directory_path)
        print("Test completed")

    def test_preprocess_repo_files(self):
        process_repo_files(self.directory_path)

        python_file_path = os.path.join(self.directory_path, self.python_file)
        self.assertTrue(os.path.exists(self.python_file_path))

        non_python_file_path = os.path.join(self.directory_path, self.non_python_file)
        self.assertFalse(os.path.exists(self.non_python_file_path))
import os
import tokenizers
from git import Repo
from github import Github

def get_access_token():
    """
    Retrieves the GitHub access token from the 'access_token.txt' file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    access_token_file = os.path.join(current_dir, 'access_token.txt')
    
    try:
        with open(access_token_file, 'r') as file:
            access_token = file.read().strip()
        return access_token
    except FileNotFoundError:
        return None
    
def clone_repository(repo_url, destination_path):
    """
    Clones a repository from the given URL and saves it to the specified destination path.
    """
    Repo.clone_from(repo_url, destination_path, depth=1)


def search_repositories(github_instance, query):
    """
    Searches for repositories based on a given query and prints their names, URLs, and tags.
    """
    search_result = github_instance.search_repositories(query)

    print(f"Found {search_result.totalCount} repositories.")

    for repo in search_result:
        print(f"Repository name: {repo.name}")
        print(f"Repository URL: {repo.clone_url}")
        clone_repository(repo.clone_url, os.path.join(os.getcwd(), 'repositories', repo.name))

def is_python_file(filename):
    """
    Check if the given filename is a Python file.

    Parameters:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the filename ends with '.py', False otherwise.
    """
    return filename.endswith('.py')

def preprocess_data(input_file, output_file, min_length, max_length, token_length_limit):
    """
    Preprocesses data by filtering lines based on their character lengths, replacing newline characters with a unique identifier, and splitting lines into chunks based on a token length limit.

    Parameters:
    - input_file (str): The path to the input file.
    - output_file (str): The path to the output file.
    - min_length (int): The minimum allowed character length for a line.
    - max_length (int): The maximum allowed character length for a line.
    - token_length_limit (int): The maximum length of each token.

    Returns:
    - None
    """
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            # Remove leading and trailing whitespace
            line = line.strip()

            # Filter based on minimum and maximum character lengths
            if len(line) < min_length or len(line) > max_length:
                continue

            # Replace newline characters with a unique identifier
            line = line.replace('\n', ' <NEWLINE> ')

            # Split the line into chunks based on token length limit
            chunks = [line[i:i+token_length_limit] for i in range(0, len(line), token_length_limit)]

            # Write each chunk as a separate line in the output file
            for chunk in chunks:
                f_out.write(chunk + '\n')

def process_repo_files(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Process the files in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Perform further processing on the file
            if is_python_file(filename):
                print(f"Keeping: {filename}")
            else:
                os.remove(file_path)
                print(f"Removed: {filename}")

def train_tokenizer(dataset, vocab_size, tokenizer_file):
    """
    Train a Byte-Level BPE tokenizer on a given dataset and save it to a file.

    :param dataset: A list of file paths or a directory containing the dataset.
    :type dataset: List[str]
    :param vocab_size: The size of the vocabulary to be generated.
    :type vocab_size: int
    :param tokenizer_file: The file path to save the trained tokenizer.
    :type tokenizer_file: str
    """
    # Create a Byte-Level BPE tokenizer
    tokenizer = tokenizers.ByteLevelBPETokenizer()

    # Train the tokenizer on the dataset
    tokenizer.train(files=dataset, vocab_size=vocab_size, min_frequency=2, special_tokens=[
        "<s>", "<pad>", "</s>", "<unk>", "<mask>"
    ])

    # Save the trained tokenizer
    tokenizer.save_model(tokenizer_file)

def main():
    access_token = get_access_token()

    # if access_token:
    #     github_instance = Github(access_token)
    #     query = "language:python"
    #     search_repositories(github_instance, query)
    # else:
    #     print("Unable to search repositories.")

    process_repo_files('repositories')

if __name__ == "__main__":
    main()



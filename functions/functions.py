import os
from duckduckgo_search import DDGS


x = 10

def show_x():
    print(x)


project_dir = "./generated"


def debug_args(*args_to_print):
    GREEN = '\033[92m'  # Green color
    YELLOW = '\033[93m'  # Yellow color
    RESET = '\033[0m'   # Reset color to default

    def decorator(func):
        def wrapper(*args, **kwargs):
            arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            print(f"{GREEN}Function name: {func.__name__}{RESET}")
            
            # Only show arguments specified in args_to_print
            for arg_name, value in zip(arg_names, args):
                if arg_name in args_to_print:
                    print(f"{YELLOW}{arg_name}: {value}{RESET}")
            for key, value in kwargs.items():
                if key in args_to_print:
                    print(f"{YELLOW}{key}: {value}{RESET}")

            return func(*args, **kwargs)
        return wrapper
    return decorator

#@debug_args("keywords")
def web_text_search(keywords: str):
        max_results = 10
        results = []
        for r in DDGS().text(keywords=keywords):
            results.append(r)
            if (max_results and len(results) >= max_results):
                break
        return results

def get_clarifiction(requiredClarification:str)->str:
    clarification = input(requiredClarification)
    return clarification




def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created.")
    else:
        print(f"Directory {path} already exists.")

#@debug_args()
def get_file_paths() -> list[str]:
    """
    Return a list of file paths in the current directory.

    Returns:
    - List[str]: The list of file paths.
    """
    import os
    file_paths = []
    for file_name in os.listdir():
        if os.path.isfile(file_name):
            file_paths.append(file_name)
    return file_paths

def list_files_in_directory():
    """
    Returns a list of files in the specified directory.
    
    Returns:
    - list: List of files in the directory.
    """
    with os.scandir(project_dir) as entries:
        return [entry.name for entry in entries if entry.is_file()]


#@debug_args("filename")
def read_file_content(filename: str) -> str:
    """
    Read the content of a file with the given filename.

    Args:
    - filename (str): The name of the file to be read.

    Returns:
    - str: The content of the file.
    """
    file_path = os.path.join(project_dir, filename)
    with open(file_path, 'r') as file:
        content = file.read()
    return content

#@debug_args("filename")
def write_to_file(filename: str, content: str) -> None:
    """
    Create a file with the given filename and write the provided content to it.

    Args:
    - filename (str): The name of the file to be created.
    - content (str): The content to be written to the file.

    Returns:
    - None
    """
    #project_dir = "./generated"
    file_path = os.path.join(project_dir, filename)

    with open(file_path, 'w') as file:
        file.write(content)

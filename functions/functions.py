import os
import subprocess
from duckduckgo_search import DDGS
from metaphor_python import Metaphor


GREEN = '\033[92m'  
YELLOW = '\033[93m' 
RESET = '\033[0m' 


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



def web_text_search(query: str)->str:
    print(f"{GREEN}Serarching: {query}{RESET}")
    metaphor = Metaphor(os.getenv("METAPHOR_API_KEY"))
    search_response = metaphor.search(query,num_results=5,include_domains=["developer.apple.com"])
    contents_response = search_response.get_contents()

    output = ""
    for content in contents_response.contents:
        output += (content.extract + "\n")

    return output




def get_clarifiction(requiredClarification:str)->str:
    print(f"{GREEN}Asking for clarification{RESET}")
    clarification = input(requiredClarification)
    return clarification


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created.")
    else:
        print(f"Directory {path} already exists.")

def list_all_files_relative() -> list[str]:
    """
    List all files in the given root directory, including those in subdirectories, 
    with paths relative to the root directory. Ignores files and directories with a . prefix.

    Args:
    - root_dir (str): The root directory to start the search from.

    Returns:
    - list: A list of file paths relative to the root directory.
    """
    root_dir = project_dir
    file_list = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove directories with . prefix from the list of directories to be explored
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if not filename.startswith('.'):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                file_list.append(relative_path)

    return file_list

print(list_all_files_relative())


def get_file_paths() -> list[str]:
    """
    Return a list of file paths in the current directory.

    Returns:
    - List[str]: The list of file paths.
    """
    print(f"{GREEN}Getting files{RESET}")
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
    print(f"{GREEN}list of files{RESET}")
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
    print(f"{GREEN}Reading: {filename}{RESET}")
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
    print(f"{GREEN}Writing: {filename}{RESET}")
    file_path = os.path.join(project_dir, filename)

    with open(file_path, 'w') as file:
        file.write(content)






def run_xcodebuild(scheme_name: str, configuration: str, sdk: str, project_path: str = None, workspace_path: str = None) -> str:
    """
    Execute the xcodebuild command with the given parameters and return its output.

    Args:
    - scheme_name (str): The name of the scheme to build.
    - configuration (str): The build configuration (e.g., "Release" or "Debug").
    - sdk (str): The SDK to build against (e.g., "iphoneos").
    - project_path (str, optional): The path to the .xcodeproj file.
    - workspace_path (str, optional): The path to the .xcworkspace file.

    Returns:
    - str: The output of the xcodebuild command.
    """
    
    print(f"{GREEN}Building {RESET}")
    
    project_path = "/Users/payman/Develop/WorldTime/WorldTime.xcodeproj"
    scheme =  "WorldTime"
    cmd = ["xcodebuild", "-quiet"]
    
    if project_path:
        cmd.extend(["-project", project_path])
    elif workspace_path:
        cmd.extend(["-workspace", workspace_path])
    
    cmd.extend([
        "-scheme", scheme_name,
        "-configuration", configuration,
        "-sdk", sdk,
        "build"
    ])

    try:
        # Capture the output and return it
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        # If there's an error, capture the error output and return it
        return e.output

# output = run_xcodebuild("WorldTime", "Develop", "iphoneos", project_path="/path/to/YourProject.xcodeproj")
# print(output)


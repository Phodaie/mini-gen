import os
from duckduckgo_search import DDGS
#from marvin import openai
from marvin.core.ChatCompletion.providers.openai import ChatCompletion as OpenAIChatCompletion
from marvin.core.ChatCompletion.base import BaseConversationState

class FConversationState(BaseConversationState):
     def send(self, *args, **kwargs):
        if self.turns:
            kwargs["messages"] = [
                *self.turns[-1].request.messages,
                self.turns[-1].raw.choices[0].message.to_dict(),
                *kwargs.get("messages", []),
            ]

        response = self.model.create(*args, **kwargs)
        self.turns.append(response)
        return response



class FChatCompletion(OpenAIChatCompletion):
    
    _state_class: FConversationState

    def state(self, *args, **kwargs):
        return FConversationState(self, *args, **kwargs)
     
    def prepare_request(self, **kwargs):
        return self.request(
            **(self._defaults or {}), **self.dict(exclude={"_defaults"})
        ).merge(**kwargs)

    def create(self, *args, **kwargs):
        request = self.prepare_request(**kwargs)
        request_dict = request.schema()
        create = getattr(self.model(request), self._create)
        return self.response(raw=create(*args, **request_dict), request=request)

ChatCompletion = FChatCompletion()

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

ROOT_DIR = "./generated"

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created.")
    else:
        print(f"Directory {path} already exists.")

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
    with os.scandir(ROOT_DIR) as entries:
        return [entry.name for entry in entries if entry.is_file()]



def read_file_content(filename: str) -> str:
    """
    Read the content of a file with the given filename.

    Args:
    - filename (str): The name of the file to be read.

    Returns:
    - str: The content of the file.
    """
    file_path = os.path.join(ROOT_DIR, filename)
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def write_to_file(filename: str, content: str) -> None:
    """
    Create a file with the given filename and write the provided content to it.

    Args:
    - filename (str): The name of the file to be created.
    - content (str): The content to be written to the file.

    Returns:
    - None
    """
    #ROOT_DIR = "./generated"
    file_path = os.path.join(ROOT_DIR, filename)

    with open(file_path, 'w') as file:
        file.write(content)

available_funcs = {get_clarifiction , write_to_file , web_text_search , read_file_content , list_files_in_directory }
used_funcs = set()

project_dir = input("What directory do you want to use?\n")
if len(project_dir) > 0:
    ROOT_DIR = project_dir

create_directory_if_not_exists(ROOT_DIR)

user_prompt = input("What do you want to do?\n")

with ChatCompletion(functions=list(available_funcs),model="gpt-4" ) as conversation:

    system_prompt = f'''
    You are an expert iOS developer. 
    Create a xCode project that includes all the requrired source code files, resorece files etc.
    Create .xcodeproj and info.plist so the project can be opened in Xcode.
    Escape Special Characters: Ensure that all special characters within the Swift code, such as double quotes (") and backslashes (\), are properly escaped. For example, a double quote should be represented as \" and a backslash as \\ in the JSON string.
    '''
    user_prompt = f'''
    {user_prompt} 
    Prompt the user if you need any clarification.
    First get the latest ios development documentation from the web before generating the project.
    Escape Special Characters: Ensure that all special characters within the Swift code, such as double quotes (") and backslashes (\), are properly escaped. For example, a double quote should be represented as \" and a backslash as \\ in the JSON string.
   
    '''
    
    
    conversation.send(messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    while conversation.last_response.has_function_call():
        response = conversation.last_response
        print(response.choices[0].message.function_call)
        used_funcs.add(response.choices[0].message.function_call.name)
        conversation.send(messages=[response.call_function()])
        

    print(conversation.last_response.choices[0].message.content)

    available_func_names = {func.__name__ for func in available_funcs}
    print(f"Used functions: {used_funcs}")
    print(f"Unused functions: {available_func_names - used_funcs}")






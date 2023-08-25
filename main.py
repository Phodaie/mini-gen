
from marvin import openai
import functions.functions
from functions.functions import  get_clarifiction , write_to_file , web_text_search , read_file_content , list_files_in_directory , run_xcodebuild , list_all_files_relative


GREEN = '\033[92m'  
YELLOW = '\033[93m' 
RESET = '\033[0m'  

dir = input("What directory do you want to use?\n")
if len(dir) > 0:
    functions.functions.project_dir = dir

user_prompt = input("What do you want to do?\n")

available_funcs = {get_clarifiction , write_to_file , web_text_search , read_file_content , list_all_files_relative , run_xcodebuild}
with openai.ChatCompletion(functions=list(available_funcs),model="gpt-4" ) as conversation:

    system_prompt = f'''
    You are an expert iOS developer. 
    Create all the requrired source code files.
    You are a Large Languge Model whose trainning was till Sep 2021. It's Aug 2023 so make sure you search the web for the latest development documentation.
    Escape Special Characters: Ensure that all special characters within the Swift code, such as double quotes (") and backslashes (\), are properly escaped. For example, a double quote should be represented as \" and a backslash as \\ in the JSON string.
    '''
    user_prompt = f'''
    {user_prompt} 
    Prompt the user if you need any clarification.
    After changing source code, build the project and fix bugs if any.
    Escape Special Characters: Ensure that all special characters within the Swift code, such as double quotes (") and backslashes (\), are properly escaped. For example, a double quote should be represented as \" and a backslash as \\ in the JSON string.
    
    '''
    
    conversation.send(messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    
    while True:
        while conversation.last_response.has_function_call():
            response = conversation.last_response
            # print(f"{GREEN}Function name: {response.choices[0].message.function_call.name}{RESET}")
            conversation.send(messages=[response.call_function()])
            
        print(conversation.last_response.choices[0].message.content)

        next_prompt = input(f"Next step ({YELLOW}end{RESET} to exit)\n")
        if next_prompt == "end":
            break

        conversation.send(messages=[
            {"role": "user", "content": next_prompt},
        ],
        temperature=0.0,
        )

    






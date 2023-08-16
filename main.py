
import os
from marvin import openai
import functions.functions
from functions.functions import  get_clarifiction , write_to_file , web_text_search , read_file_content , list_files_in_directory , create_directory_if_not_exists


GREEN = '\033[92m'  # Green color
YELLOW = '\033[93m'  # Yellow color
RESET = '\033[0m'   # Reset color to default

dir = input("What directory do you want to use?\n")
if len(dir) > 0:
    functions.functions.project_dir = dir

user_prompt = input("What do you want to do?\n")

used_funcs = set()
available_funcs = {get_clarifiction , write_to_file , web_text_search , read_file_content , list_files_in_directory }
with openai.ChatCompletion(functions=list(available_funcs),model="gpt-4" ) as conversation:

    system_prompt = f'''
    You are an expert iOS developer. 
    Create all the requrired source code files.
    Escape Special Characters: Ensure that all special characters within the Swift code, such as double quotes (") and backslashes (\), are properly escaped. For example, a double quote should be represented as \" and a backslash as \\ in the JSON string.
    '''
    user_prompt = f'''
    {user_prompt} 
    Prompt the user if you need any clarification.
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
            print(f"{GREEN}Function name: {response.choices[0].message.function_call.name}{RESET}")
            
            used_funcs.add(response.choices[0].message.function_call.name)
            conversation.send(messages=[response.call_function()])
            

        print(conversation.last_response.choices[0].message.content)

        next_prompt = input("Next step (type end to exit)\n")
        if next_prompt == "end":
            break

        conversation.send(messages=[
            {"role": "user", "content": next_prompt},
        ],
        temperature=0.0,
        )

    available_func_names = {func.__name__ for func in available_funcs}
    print(f"Used functions: {used_funcs}")
    print(f"Unused functions: {available_func_names - used_funcs}")






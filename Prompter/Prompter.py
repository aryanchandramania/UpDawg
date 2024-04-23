import sys
sys.path.append('..')
from DataEngine import DataEngine

class Prompter:
    def __init__(self, sys_prompt):
        # instantiate data engine
        self.DE = DataEngine()
        self.app_names = ['Slack', 'Outlook']
        self.sys_prompt = sys_prompt
        # instantiate llm switcher
        # initialize all variables needed for the prompter

    def prompt(self, dateTime):
        data = self.DE.getData(dateTime)
        user_prompt = self.prompt_contructor(data)
        print(user_prompt)
        # send sys prompt and user prompt to llm switcher

    
    def prompt_contructor(self, data, nlCount=3):
        if nlCount<0:
            nlCount =0 
        user_prompt=''
        for key,value in data.items():
            user_prompt += f'{key}:'
            if isinstance(value,list):
                user_prompt += f'\n'
                for item in value:
                    user_prompt += self.prompt_contructor(item, nlCount-1)
                user_prompt += f'{self.genNLn(nlCount)}'
            else:
                user_prompt += f'{value}\n'
        return user_prompt
        
    def genNLn(self,count):
        return '\n'*count
    

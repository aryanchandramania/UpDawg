
from DataEngine.DataEngine import DataEngine
from AdaService.AdaLLM import AdaLLM
from Message.Message import Message
from DataClasses.MessageServices import MessageServices


class Prompter:
    def __init__(self, summary_sys_prompt):
        # instantiate data engine
        self.DE = DataEngine()
        msgSerData = MessageServices()
        self.app_names = msgSerData.service_names
        self.summary_sys_prompt = summary_sys_prompt
        self.serveLLM = AdaLLM()
        # instantiate llm switcher
        # initialize all variables needed for the prompter


    def prompt(self, dateTime):
        data = self.DE.getData(dateTime)
        user_prompt = self.prompt_contructor(data)
        print("User Prompt:")
        print(user_prompt)

        # call the service on the system and user prompt
        service = self.serveLLM.choose()
        res = service.summarize(user_prompt, self.summary_sys_prompt)
        return res
        

    
    def prompt_contructor(self, data, nlCount=3):
        if nlCount<0:
            nlCount =0 

        if isinstance(data, Message):
            data = data.to_dict()
            data.pop('id')
            data.pop('user_id')
            data.pop('app')
        
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


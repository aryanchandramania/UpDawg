import sys 
sys.path.append('..')

class LLMServices:
    def __init__(self):
        self.service_names = ['openai', 'gemini']

    def getDownDetectorURLs(self):
        downDetectorUrl={'openai':'https://isdown.app/integrations/openai',
                          'gemini':'https://isdown.app/integrations/gemini'}
        return downDetectorUrl
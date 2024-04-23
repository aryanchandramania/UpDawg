import requests
from bs4 import BeautifulSoup

class AdaLLM:
    def __init__(self):
        self.services = ['openai', 'gemini']
        # instantiate openAI service
        # instantiate gemini service
        # pull from user config for API keys
        self.services = {
            'openai': None,
            'gemini': None
        }
        self.APIKeys={'openai':None,
                      'gemini':None}
        self.downDetectorUrl={'openai':'https://isdown.app/integrations/openai',
                              'gemini':'https://isdown.app/integrations/gemini'}
        
        # in days, total period over which number if issues and most recent incident is reported
        self.downPeriod = 30 



    def choose(self):
        filt = self.filterBasedOnKey()
        ser = self.filterBasedOnReliability(filt)
        return self.services[ser]
        

    def filterBasedOnKey(self):
        filt=[]
        for s in self.services:
            if self.APIKeys[s] != None:
                filt.append(s)
        return filt
    

    def filterBasedOnReliability(self, filt):
        final = filt[0]
        best_score = 1000
        for s in filt:
            score = self.getDownScore(self.downDetectorUrl[s])
            if (score < best_score):
                final = s
                best_score = score
        return final


    # higher the score, worse the service is
    def getDownScore(self,url):
        issues = -1
        recency = -1

        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        # getting the data from the webpage
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the issues count element
            issues_obj = soup.find('body').find_all('div')[1].find('section').find('div').find('div').find_all('div')[0].find('div').find_all('div')[1].find_all('div')[1].find('div').find('div').find('div').find_all('p')[1].find('span')
            recency_obj = soup.find('body').find_all('div')[2].find('section').find('div').find('div').find_all('div')[0].find('div').find_all('div')[1].find_all('div')[1].find('div').find('div').find('div').find_all('p')[1].find('span')
            
            # check if the elements were found
            if issues_obj:
                issues = int(issues_obj.text)
                print(issues_obj.text)
            else:
                print("Element not found.")
                return -1
            
            if recency_obj:
                recency = int(recency_obj.text)
                print(recency_obj.text)
            else:
                print("Element not found.")
                return -1

        else:
            print("Failed to retrieve the webpage.")
            return -1
        
        return issues + (30-recency)


import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright 

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
        self.APIKeys={'openai':'',
                      'gemini':''}
        self.downDetectorUrl={'openai':'https://isdown.app/integrations/openai',
                              'gemini':'https://isdown.app/integrations/gemini'}
        

        # in days, total period over which number if issues and most recent incident is reported
        self.downPeriod = 30 
        self.bestService = 'openai'



    def choose(self):
        print(f'{self.bestService} chosen')
        return self.services[self.bestService]
        

    # this may run periodically
    def scoreLLM(self):
        filt = self.filterBasedOnKey()
        ser = self.filterBasedOnReliability(filt)
        self.bestService = ser


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
        issues = 1000
        recency = 1000

        # Launch the Playwright browser instance
        try:
            with sync_playwright() as p:
                browser = p.webkit.launch(headless=True)

                page = browser.new_page()
                page.goto(url)
                # Get the page content after it fully loads
                page.wait_for_load_state('networkidle')
                html_content = page.content()

                # # Close the browser
                browser.close()

                # Parse the HTML content of the webpage
                soup = BeautifulSoup(html_content, 'html.parser')
                # print(html_content)
                
                # Find the issues count element and recency count
                issues_obj = soup.select_one('body > div:nth-of-type(2) > section > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(1) > p:nth-of-type(2) > span:nth-of-type(1)')
                recency_obj = soup.select_one('body > div:nth-of-type(2) > section > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(2) > p:nth-of-type(2) > span:nth-of-type(1)')

                if not issues_obj:
                    issues_obj = soup.select_one('body > div:nth-of-type(2) > section > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div:nth-of-type(1) > p:nth-of-type(2) > span:nth-of-type(1)')
                if not recency_obj:
                    recency_obj = soup.select_one('body > div:nth-of-type(2) > section > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div:nth-of-type(2) > p:nth-of-type(2) > span:nth-of-type(1)')
                

                # check if the elements were found
                if issues_obj:
                    issues = int(issues_obj.text)
                    # print(issues_obj.text)
                else:
                    print("Element not found.")
                    return 1000
                
                if recency_obj:
                    recency = int(recency_obj.text)
                    # print(recency_obj.text)
                else:
                    print("Element not found.")
                    return 1000
        except:
            print("Failed to launch the browser.")
            return 1000
        
        print(issues + (self.downPeriod-recency))
        return issues + (self.downPeriod-recency)


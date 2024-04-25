# this is the driver code for periodic LLM scoring

from time import sleep

import sys
sys.path.append('/home/raghav/Documents/College/SE/Project3/UpDawg/src')

from AdaService.AdaLLM import AdaLLM


period = 1200 # in seconds

llm = AdaLLM()

while True:
    llm.scoreLLM()
    sleep(period)

# this is the driver code for periodic LLM scoring

from src.AdaService.AdaLLM import AdaLLM
from time import sleep


period = 1200 # in seconds

llm = AdaLLM()

while True:
    llm.scoreLLM()
    sleep(period)

# this file is for listening for user requests

# steps for the processRequest listener
# 1. listen for user requests and receive them, user requests will consist of a number, representing the number of days they want the summary for
# 2. this request is sent to the Prompter.prompt() function
# 3. This response is parsed by the response parser and sent back to the user

# this will also support login, logout, and user onboarding functions on various endpoints
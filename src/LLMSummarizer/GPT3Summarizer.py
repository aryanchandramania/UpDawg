from openai import OpenAI
import configparser

# config = configparser.ConfigParser()
# config.read('secrets.ini')

class DataSplitter:
    def split_data_into_chunks(self, data, max_words):
        chunks = []
        remaining_data = data.strip().split()  # Split the data into words

        while remaining_data:
            if len(remaining_data) <= max_words:
                chunks.append(' '.join(remaining_data))
                break

            chunk = ' '.join(remaining_data[:max_words])
            remaining_data = remaining_data[max_words:]

            chunks.append(chunk.strip())

        return chunks

class GPT3Summarizer:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def summarize(self, data, prompt):

        # return "Hello Aryan Chandramania"

        chunks = DataSplitter().split_data_into_chunks(data, 100000)
        # print(len(chunks))
        chunk_messages=[
                {"role": "system", "content": prompt},
            ]
        last_response = ""
        for i,chunk in enumerate(chunks):            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"{prompt} {chunk}"}
                ]
            )
            chunk_messages.append({"role": "assistant", "content": response.choices[0].message.content})
            last_response = response.choices[0].message.content
        
        if len(chunks) > 1:
            chunk_messages.append({"role": "user", "content": "Generate a final combined summary."})  

            # Create completion for final summary
            final_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chunk_messages
            )

            return final_response.choices[0].message.content

        return last_response
    
if __name__ == '__main__':

    data = """Outlook:

Email Subject: Team Meeting Agenda
Sender: John Doe
Date: 2024-04-20

Hi team,

Here's the agenda for our meeting tomorrow:

1. Introduction
2. Project updates
3. Discussion on upcoming deadlines
4. Any other business

Let me know if there's anything else to add.

Best regards,
John

---

Outlook:

Email Subject: Weekly Progress Report
Sender: Sarah Lee
Date: 2024-04-21

Dear team,

Please find attached the weekly progress report for our ongoing projects. 
We're making good progress, but there are a few areas that need attention.

Highlights:
- Project A: On track to meet the deadline. 
- Project B: Facing delays due to resource constraints.
- Project C: Need to rework the design phase.

Let's discuss these in our meeting tomorrow.

Best regards,
Sarah

---

Slack:

Channel: #general
Sender: Jane Smith
Date: 2024-04-18

Hey everyone,

Just a quick reminder that the deadline for the project is approaching. 
Make sure to complete your tasks on time.

Thanks,
Jane

---

Slack:

Channel: #random
Sender: Mark Johnson
Date: 2024-04-19

Anyone interested in joining a lunch meetup tomorrow?

---

Slack:

Channel: #general
Sender: Michael Wang
Date: 2024-04-21

Team,

Just a heads up, we have a new team member joining us next week. 
Let's make sure to welcome them warmly.

Cheers,
Michael

---

Slack:

Channel: #team-projects
Sender: Alice Brown
Date: 2024-04-20

I've uploaded the latest version of the project proposal document. 
Please review and provide feedback by EOD today.

Thanks,
Alice

---

Slack:

Channel: #random
Sender: Emily Chen
Date: 2024-04-22

Hey folks,

I'm organizing a team building event next month. 
Stay tuned for more details!

Best,
Emily

---

Slack:

Channel: #team-projects
Sender: David Liu
Date: 2024-04-22

Team,

I need your input on the budget proposal for Project D. 
Please review and provide feedback by the end of the week.

Thanks,
David
"""
    # OPENAI_API_KEY = config['OPENAI']['secretkey']
    # prompt = "Can you provide a summary of the emails and messages received"
    # summarizer = GPT3Summarizer(OPENAI_API_KEY)
    # print(summarizer.summarize(data=data, prompt=prompt))

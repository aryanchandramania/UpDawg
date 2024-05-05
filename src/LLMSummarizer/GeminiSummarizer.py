import google.generativeai as genai
import configparser

config = configparser.ConfigParser()
config.read('secrets.ini')


class DataSplitter:
    def split_data_into_chunks(self, data, max_tokens):
        chunks = []
        remaining_data = data.strip()

        while remaining_data:
            if len(remaining_data) <= max_tokens:
                chunks.append(remaining_data)
                break

            last_full_stop = remaining_data[:max_tokens].rfind(".")

            if last_full_stop == -1:
                chunk = remaining_data[:max_tokens]
                remaining_data = remaining_data[max_tokens:]
            else:
                chunk = remaining_data[:last_full_stop+1]  # Include the full stop
                remaining_data = remaining_data[last_full_stop+1:]

            chunks.append(chunk.strip())

        return chunks

class GeminiSummarizer:
    
    def __init__(self, google_api_key):
        genai.configure(api_key=google_api_key)

    # def summarize(self, data, prompt):
    #     model = genai.GenerativeModel('gemini-pro')
    #     # print(model.count_tokens(data))
    #     chunks = DataSplitter().split_data_into_chunks(data, 5000)

    #     chat = model.start_chat(history=[])
    #     response = ""

    #     for i,chunk in enumerate(chunks):
    #         response = chat.send_message(prompt + '\n' + chunk) if i == 0 else chat.send_message("Continue the earlier summary with this info:\n" + chunk)

    #     response = chat.send_message("Return the final summary of all the messages")

    #     return response.text

    def summarize(self, data, prompt):

        model = genai.GenerativeModel('gemini-pro')
        chunks = DataSplitter().split_data_into_chunks(data, 5000)
        summaries = []

        # Generate summaries for each chunk
        for chunk in chunks:
            summary = model.generate_content(prompt + '\n' + chunk)
            summaries.append(summary.text)

        # Generate final combined summary
        final_summary = model.generate_content("Generate a final combined summary.\n" + "\n".join(summaries))
        return final_summary.text
    
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
    GOOGLE_API_KEY = config['GEMINI']['secretkey']
    prompt = "Can you provide a summary of the emails and slack messages received"
    summarizer = GeminiSummarizer(GOOGLE_API_KEY)
    print(summarizer.summarize(data=data, prompt=prompt))
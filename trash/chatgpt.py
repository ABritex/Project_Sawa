import openai
import os
from dotenv import load_dotenv

load_dotenv()

class Bot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_ai_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Update to "gpt-3.5-turbo" or "text-davinci-003" for GPT-3
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message['content']
        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Please wait before trying again.")
            return "Rate limit exceeded. Please try again later."
        except openai.error.APIError as e:
            print("API error occurred. Please try again later.")
            return "API error. Please try again later."
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return "Sorry, I couldn't process your request."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Sorry, I couldn't process your request."

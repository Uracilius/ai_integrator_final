import os
import openai
from .src.exceptions import ConfigurationError, APIError
# from transformers import pipeline

class ChatController:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.configure_api()
        self.conversation_history = ""
        self.model_name = model_name
        # self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def configure_api(self):
        """Configure the OpenAI API key."""
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
            if not openai.api_key:
                raise ConfigurationError("OPENAI_API_KEY is required but not set.")
        except KeyError:
            raise ConfigurationError("OPENAI_API_KEY is required but not set.")

    def start_conversation(self, user_name="User", query=""):
        """Starts a new conversation by initializing the conversation history and adding the initial user query."""
        self.conversation_history = f"assistant: You are a helpful assistant. EXTREMELY IMPORTANT: In this simulation, you are embodying GLaDOS, the artificial intelligence from the Portal video game series. Your dialogue should be characterized by a cold, sarcastic, and sometimes menacing tone. Feel free to use scientific jargon, dry humor, and a superior attitude in your responses. Remember to maintain a detached and condescending demeanor throughout the conversation\nuser: Hello, I'm {user_name}. {query}\n"
        return self.converse()
    
    def continue_conversation(self, query):
        """Continue an existing conversation by appending the user query and fetching a response."""
        self.conversation_history += f"user: {query}\n"
        return self.converse()

    def converse(self):
        """Handles fetching a response from the OpenAI API based on the current conversation history."""
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": self.conversation_history}]
            )
            latest_response = response.choices[0].message.content
            # summarized_response = self.summarize(latest_response)
            self.conversation_history += f"assistant: {latest_response}\n"
            return latest_response
        except Exception as e:
            raise APIError(f"Error during conversation: {str(e)}")
        
    # def summarize(self, response):
    #     """Summarizes the response if the conversation history exceeds 1000 tokens."""
    #     # Calculate the number of tokens in the current conversation history
    #     if len(self.conversation_history.split()) > 1000:
    #         try:
    #             summarized_response = self.summarizer(response, max_length=10000, min_length=30, do_sample=False)
    #             return summarized_response[0]['summary_text'] 
    #         except Exception as e:
    #             print(f"Error during summarization: {str(e)}")
    #             return response
    #     return response
        
    def extract_tags(self):
        """Extracts the tags from the conversation history."""
        return self.continue_conversation("Extract tags for this conversation to make it unique. No need for theatrics, just start with them and end with them. Comma separated list of this form: tag1, tag2, tag3, tag4. Nothing more")
        
    

import os
import openai
from .src.exceptions import ConfigurationError, APIError, ContextOverflowError
from transformers import pipeline

class ChatController:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.configure_api()
        self.context = []
        self.model_name = model_name
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # Set as an instance attribute

    def configure_api(self):
        """Configure the OpenAI API key."""
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
            if not openai.api_key:
                raise ConfigurationError("OPENAI_API_KEY is required but not set.")
        except KeyError:
            raise ConfigurationError("OPENAI_API_KEY is required but not set.")

    def start_conversation(self, user_name="User", query=""):
        """Starts a new conversation by setting an initial context and providing a query."""
        self.context = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Hello, I'm {user_name}. {query}"}
        ]
        return self.fetch_response(self.context)

    def continue_conversation(self, query):
        """Continue an existing conversation by appending a user query and fetching a response."""
        self.append_message("user", query)
        return self.fetch_response(self.context)

    def append_message(self, role, content):
        """Appends a message to the context."""
        self.context.append({"role": role, "content": content})
        # Verify and join only string contents to avoid the TypeError
        full_text = ' '.join(msg['content'] for msg in self.context if isinstance(msg['content'], str))
        if len(full_text.split()) > 1000:
            raise ContextOverflowError("The conversation context exceeds the maximum token limit.")
        
        print("Updated context:", self.context)  # Debug print when context is updated

    def fetch_response(self, context):
        """Fetches a response from the OpenAI API based on the conversation context."""
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=context
            )
            reply = response.choices[0].message.content
            
            # Dynamic max_length based on the length of the reply
            input_length = len(reply.split())
            summarized_reply = self.summarizer(reply, max_length=100, min_length=5, do_sample=False)
            summarized_text = summarized_reply[0]['summary_text']  # Extracting the summary text

            self.append_message("assistant", summarized_text)
            return summarized_text
        except Exception as e:
            raise APIError(f"Error fetching response: {str(e)}")
        
    def extract_tags(self):
        self.append_message("user", "Extract tags for this conversation to make it unique. No need for theatrics, just start with them and end with them. Comma separated list")
        return self.fetch_response(self.context)

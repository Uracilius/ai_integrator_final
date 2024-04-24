import os
import openai
from .src.exceptions import ConfigurationError, APIError, ContextOverflowError

class ChatController:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.configure_api()
        self.context = []
        self.model_name = model_name

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
        if len(' '.join(msg['content'] for msg in self.context).split()) > 1000:
            raise ContextOverflowError("The conversation context exceeds the maximum token limit.")

    def fetch_response(self, context):
        """Fetches a response from the OpenAI API based on the conversation context."""
        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=context
            )
            reply = response.choices[0].message.content
            self.append_message("assistant", reply)
            return reply
        except Exception as e:
            raise APIError(f"Error fetching response: {str(e)}")
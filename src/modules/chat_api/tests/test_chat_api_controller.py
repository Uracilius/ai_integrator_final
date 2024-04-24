import unittest
from unittest.mock import patch
from src.modules.chat_api.chat_api_controller import *

class ChatAPITest(unittest.TestCase):

    def test_configure_api_sets_openai_api_key(self):
        # Positive Test case for configuring the API
        configure_api()
        self.assertIsNotNone(openai.api_key)

    def test_start_conversation_returns_expected_message_structure(self):
        # Positive Test case for starting a conversation
        user_name = "User"
        expected_response = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Hello, I'm {user_name}."}
        ]
        response = start_conversation(user_name)
        self.assertEqual(response, expected_response)

    def test_append_message_correctly_adds_message_to_history(self):
        # Positive Test case for appending a message to history
        history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, I'm User."}
        ]
        role = "assistant"
        content = "How can I assist you?"
        expected_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, I'm User."},
            {"role": "assistant", "content": "How can I assist you?"}
        ]
        response = append_message(history, role, content)
        self.assertEqual(response, expected_history)

    def test_check_context_length_raises_context_overflow_error_when_exceeded(self):
        # Negative Test case for checking context length
        messages = [{"role": "system", "content": "You are a helpful assistant. " * 500},
                    {"role": "user", "content": "Hello, I'm User."},
                    {"role": "assistant", "content": "How can I assist you?"}]
        self.assertRaises(ContextOverflowError, check_context_length, messages)

    def test_get_response_returns_non_null_response(self):
        # Positive Test case for getting a response
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, I'm User."},
            {"role": "assistant", "content": "How can I assist you?"}
        ]
        response = get_response(messages)
        self.assertIsNotNone(response)

    def test_new_conversation_initializes_and_returns_response(self):
        # Positive Test case for starting a new conversation
        user_name = "Alice"
        response = new_conversation(user_name)
        self.assertIsNotNone(response)

    def test_existing_conversation_continues_with_user_input_and_returns_response(self):
        # Positive Test case for continuing an existing conversation
        context = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, I'm User."}
        ]
        user_message = "What can you do?"
        response = existing_conversation(context, user_message)
        self.assertIsNotNone(response)

    def test_configure_api_fails_without_environment_variable(self):
        # Negative Test case for configuring API without an environment variable
        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}, clear=True):
            with self.assertRaises(ConfigurationError):
                configure_api()

if __name__ == "__main__":
    unittest.main()

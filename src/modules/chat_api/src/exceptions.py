class ConfigurationError(Exception):
    """Exception raised for errors in the configuration of the API key."""
    def __init__(self, message="API key not found in environment variables."):
        self.message = message
        super().__init__(self.message)

class APIError(Exception):
    """Exception raised for errors that occur during API calls."""
    def __init__(self, error, message="API call failed."):
        self.message = f"{message} Reason: {str(error)}"
        super().__init__(self.message)

class ContextOverflowError(Exception):
    """Exception raised when the conversation context exceeds token limits."""
    def __init__(self, message="Context exceeds the maximum token limit."):
        self.message = message
        super().__init__(self.message)

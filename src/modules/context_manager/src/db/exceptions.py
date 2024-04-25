class DataNotFoundException(Exception):
    """Exception raised when no data is found for a given query."""
    def __init__(self, message="No data found"):
        self.message = message
        super().__init__(self.message)
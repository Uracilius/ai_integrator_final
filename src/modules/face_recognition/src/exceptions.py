class CameraError(Exception):
    """Exception raised when the camera fails to open or operate correctly."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.message = message
        self.errors = errors  

class CaptureError(Exception):
    """Exception raised when capturing a photo fails."""
    def __init__(self, message, frame_count=None):
        super().__init__(message)
        self.message = message
        self.frame_count = frame_count 

class ImageConversionError(Exception):
    """Exception raised for errors in the image conversion process."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class FaceDetectionError(Exception):
    """Exception raised for errors during the face detection process."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ImageProcessingError(Exception):
    """Exception raised for errors during image cropping and resizing."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

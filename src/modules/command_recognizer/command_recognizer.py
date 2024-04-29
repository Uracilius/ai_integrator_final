import fasttext
import os
class CommandRecognizer:
    def __init__(self):
        """
        Initialize the CommandRecognizer with a FastText model.

        Args:
        - model_path (str): Path to the FastText model file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = fasttext.load_model(base_dir+'/intent_model.bin')

    def predict_intent(self, sentence):
        """
        Predict the intent of a given sentence.

        Args:
        - sentence (str): The input sentence.

        Returns:
        - intent (str): The predicted intent label.
        - confidence (float): The confidence score of the prediction.
        """
        labels, probabilities = self.model.predict(sentence, k=1)
        intent = labels[0].replace('__label__', '')
        confidence = probabilities[0]
        return intent, confidence

    def predict(self, sentence):
        """
        Predict the intent of a given sentence and output the result.

        Args:
        - sentence (str): The input sentence.
        """
        intent, confidence = self.predict_intent(sentence)
        print("Predicted intent:", intent, "with confidence", confidence)

# Example usage:
if __name__ == "__main__":
    model_path = "your_model.bin"  # Replace with the path to your FastText model file
    recognizer = CommandRecognizer(model_path)

    sentences = [
        "Ayo let's add someone new.",
        "I want to add a new participant.",
        "Enroll a new participant with details.",
        "Let's discuss a different subject.",
        "Change the topic bruh.",
        "So do these whales cause pollution?",
        "So why would I cause such ruckus on the streets?",
        "I don't agree with you at all.",
        "Lorem ipsum."
    ]

    for sentence in sentences:
        recognizer.predict(sentence)

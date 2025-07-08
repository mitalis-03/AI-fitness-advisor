import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

# Set speaking rate (words per minute)
engine.setProperty('rate', 150)

# Set volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)

# Optional: Change voice (Male/Female depending on OS support)
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)  # Usually male
# engine.setProperty('voice', voices[1].id)  # Usually female

def speak(text):
    """
    Convert text to speech.
    Args:
        text (str): The message to be spoken aloud.
    """
    engine.say(text)
    engine.runAndWait()

# Example usage:
if __name__ == "__main__":
    speak("Welcome to the AI Fitness Advisor!")
    speak("Your posture is correct. Keep it up!")

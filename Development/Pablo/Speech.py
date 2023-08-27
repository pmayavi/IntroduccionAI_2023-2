import speech_recognition as sr
import pyautogui

# Initialize the recognizer
recognizer = sr.Recognizer()

def execute_command(command):
    if "click" in command:
        pyautogui.click()
        print("Clicked!")

def main():
    with sr.Microphone() as source:
        print("Listening for commands...")
        while True:
            try:
                # Adjust energy_threshold based on your microphone sensitivity
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                
                print("You said:", command)
                execute_command(command)
                
            except sr.WaitTimeoutError:
                print("No command detected. Listening again...")
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that. Please try again.")
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()

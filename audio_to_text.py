from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


class SpeechToText:
    
    def __init__(self, model="whisper-1"):
        self.model = model
        self.client = OpenAI()
        
    def speech_to_text(self, input_file_path:str) -> str:
        """
        Recognize speech from audio file and return text from it
        Args:
            input_file_path (str): path to audio.mp3 file

        Returns:
            str: recognized text from audio file
        """
        try:
            with open(input_file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(model=self.model, file=audio_file)
                return transcription.text
        except Exception as e:
            print(e)
            
    
if __name__ == "__main__":
    import os
    files = os.listdir("./output_audio/")
    
    stt = SpeechToText()
    for file in files:
        result = stt.speech_to_text(f"./output_audio/{file}")
        print(result)
        
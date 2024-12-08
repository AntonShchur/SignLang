from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
load_dotenv()



class TextToSpeech:
    
    class Voice(Enum):
        ALLOY = "alloy"
        ECHO =  "echo"
        FABLE = "fable"
        ONYX =  "onyx"
    
    
    def __init__(self, model="tts-1", voice=Voice.ALLOY):
        """_summary_

        Args:
            model (str, optional): _description_. Defaults to "tts-1".
            voice (_type_, optional): _description_. Defaults to Voices.ALLOY.
        """
        if not isinstance(voice, TextToSpeech.Voice):
            raise ValueError("Invalid voice")
        self.model:str = model
        self.voice = voice.value
        self.client = OpenAI()
        
    def text_to_speech(self, text:str, output_file_path:str) -> None:
        """
        Generate audio file from given text
        Args:
            text (str): text to generate audiofrom it
            output_file (str): path to save output speech.mp3 file 
        """
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            response.write_to_file(file=output_file_path)
        except Exception as e:
            print(e)
            
            
if __name__ == "__main__":
    texts_to_voiceover = [
        "Коли надвечір сонце повільно опускалося за обрій, залишаючи за собою багряно-золотий горизонт, на подвір’ї розпочалася вечірня праця.",
        "Попри всі труднощі та перепони, які зустрічалися на його шляху, він завжди знаходив сили йти вперед, адже мріяв здійснити задумане.",
        "Поки старий дуб хитав своїми величезними гілками під натиском сильного вітру, десь далеко чути було тихий спів пташок.",
        "Коли вона відкрила стару скриню, наповнену пожовклими листами й зотлілими фото, спогади дитинства несподівано нахлинули на неї, наче хвиля.",
        "Хоча місто вже потопало в сутінках, його вузькі вулички залишалися наповненими шумом і гамором, що створювали перехожі та вуличні музиканти.",
    ]
    tts = TextToSpeech()
    for i, line in enumerate(texts_to_voiceover):
        tts.text_to_speech(line, output_file_path=f"./output_audio/line{i}.mp3")
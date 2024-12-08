from sign_recognizer import SignRecognizer

from sign_to_lang import SignToLang
from lang_to_sign import LangToSign

from text_to_audio import TextToSpeech
from audio_to_text import SpeechToText

class SignLangTranslator:
    
    def __init__(self):
        pass
    
    def translate_sign_to_lang(self, path_to_video:str)-> str:
        """
        This method accepts path to video

        Args:
            path_to_video (str): path to target video

        Returns:
            str: transalted sentence in ukrainian language 
        """
        
        sign_recornizer = SignRecognizer()
        sign_to_lang = SignToLang()
        
        recognised_signs = sign_recornizer.recognize_sign_on_video(path_to_video)
        sentence_to_translate = " ".join(recognised_signs)
        translated_sentence = sign_to_lang.translate_sentence(sentence_to_translate)
        
        return translated_sentence
        
        
    def translate_text_to_sign(self, text_to_translate):
        lang_to_sign = LangToSign()
        transalted_sentence = lang_to_sign.translate_sentence(text_to_translate)
        return transalted_sentence
    
    def translate_audio_to_sing(self, path_to_audio):
        stt = SpeechToText()
        text = stt.speech_to_text(path_to_audio)
        
        translated_audio = self.translate_text_to_sign(text)
        return translated_audio
    
    def text_to_speech(self, text:str, output_file_path:str) -> None:
        """
        Generate Audio file with text voiceover

        Args:
            text (str): text to voiceover
            output_file_path (str): path to save audiofile
        """
        tts = TextToSpeech()
        tts.text_to_speech(text, output_file_path)
        
        
        
if __name__ == "__main__":
    
    sign_translator = SignLangTranslator()
    result = sign_translator.translate_sign_to_lang("S:/DiplomaProject/Videos/2024-10-20 18-56-23.mp4")
    print(result)
    result = sign_translator.translate_text_to_sign(result)
    print(result)
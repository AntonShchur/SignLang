import gradio as gr
from gradio_multimodalchatbot import MultimodalChatbot
from gradio.data_classes import FileData
from sign_lang_translator import SignLangTranslator
from helpers import *

AUDIO_FOLDER = "./output_audio/"

user_started_message = {"text": "Привіт, я хочу, щоб ти допомагав мені перекладати українську мову жестів.",
             "files": []
             }
bot_started_message = {"text": "Добре, я буду перекладати тобі українську жестову мову (УЖМ) на українську словесну мову та навпаки!",
            "files": []}


conversation = [[user_started_message, bot_started_message]]

sign_language_translator = SignLangTranslator()
iteration = 0
with gr.Blocks() as application:
    
    chat_bot = MultimodalChatbot(value=conversation, height=800, show_label=False)
    msg = gr.Textbox(label="")
    clear = gr.ClearButton([msg, chat_bot], value="Очистити")
    
    with gr.Row():
        with gr.Column(scale=1):  
            video = gr.Video(format="mp4", show_label=False)
        with gr.Column(scale=1):
            audio = gr.Audio(type="filepath", show_label=False)
            
            
    def translate_video(video_path, conversation):
        global iteration
        print(video_path)
        path_to_audio = f"{AUDIO_FOLDER}{iteration}.mp3"
        
        
        translated_video = sign_language_translator.translate_sign_to_lang(video_path)
        message = f"""
        На даному відео зображені такі жести:\n
        {translated_video}
        """
        sign_language_translator.text_to_speech(translated_video, output_file_path=path_to_audio)
        
        
        bot_message = create_message_structure(message,
                                               [{"file": FileData(path=path_to_audio)}])
        user_video_msg = {"text": "",
             "files": [{"file": FileData(path=video_path)}]
             }
        
        conversation.append([user_video_msg, bot_message])
        chat_bot.value = conversation
        iteration +=1
        
        return "", conversation
    
    def translate_audio(audio_path, conversation):


        translated_audio = sign_language_translator.translate_audio_to_sing(path_to_audio=audio_path)
        
        user_audio_msg = {"text": "Переклади мені це аудіо на мову жестів.",
             "files": [{"file": FileData(path=audio_path)}]
             }
        message = f"""
        Переклад даного аудіофайлу на українську мову буде:
        {translated_audio}
        """
        bot_message = create_message_structure(message, [])  
        
        conversation.append([user_audio_msg, bot_message])
        chat_bot.value = conversation
        return "", conversation
    

    def translate_text_to_sign(message, conversation):
        
        translated_message = sign_language_translator.translate_text_to_sign(message)
        user_message = create_message_structure(message, [])
        message = f"""
        Щоб показати це твоє речення на мові жестів, робот має показати наступні жести:
        {translated_message}
        """
        bot_message = create_message_structure(message, [])
        
        conversation.append([user_message, bot_message])
        chat_bot.value = conversation
        return "", conversation

          
        
         
        
    video.upload(translate_video, [video, chat_bot], [msg, chat_bot])
    video.stop_recording(translate_video, [video, chat_bot], [msg, chat_bot]) 
    
    audio.upload(translate_audio, [audio, chat_bot], [msg, chat_bot])
    audio.stop_recording(translate_audio, [audio, chat_bot], [msg, chat_bot])
    
    msg.submit(translate_text_to_sign, [msg, chat_bot], [msg, chat_bot])
     
if __name__ == "__main__":
    application.launch()
    
from constants import *
import sys
sys.path.append("../")
import torch
import numpy as np
import cv2

from constants import classes
from helpers import resize
from dotenv import load_dotenv
load_dotenv()


class SignRecognizer:
    Prompt = prompt
    def __init__(self,
                 path_to_model:str= "./models/mvit32-2.pt",
                 threshold=0,
                 window_size=32,
                 frame_interval=1,
                 fps=30):
        self.path_to_model = path_to_model
        self.model = torch.jit.load(self.path_to_model)
        self.model.eval()
        self.window_size = window_size
        self.threshold = threshold
        self.frame_interval = frame_interval
        self.fps = fps
        self.mean = [123.675, 116.28, 103.53]
        self.std = [58.395, 57.12, 57.375]
        
    
    def __recognize_sign_on_video_vit(self, path_to_video:str):
        cap = cv2.VideoCapture(path_to_video)
        _,frame = cap.read()
        tensors = []
        prediction_list = ["No action"]
        iteration = 0
        while True:
            _, frame = cap.read()
            if frame is None:
                break
            iteration += 1
            if iteration == self.frame_interval:
                frame_image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
                frame_image = resize(frame_image, (224, 224))
                frame_image = (frame_image - self.mean) / self.std
                frame_image = np.transpose(frame_image, [2, 0, 1])
                tensors.append(frame_image)
                if len(tensors) == self.window_size:
                    input_tensor = np.stack(tensors[: self.window_size], axis=1)[None][None]
                    input_tensor = input_tensor.astype(np.float32)
                    input_tensor = torch.from_numpy(input_tensor)
                    outputs = self.model(input_tensor)[0]
                    gloss = str(classes[outputs.argmax().item()])
                    if outputs.max() > self.threshold:
                        if gloss != prediction_list[-1] and len(prediction_list):
                            prediction_list.append(gloss)
                    tensors.clear()
                iteration = 0
        cap.release()
        return prediction_list
    
    
    def recognize_sign_on_video(self, video_path:str) -> list[str]:
        answer = self.__recognize_sign_on_video_vit(video_path)
        return answer
            

if __name__ == "__main__":      
    pass
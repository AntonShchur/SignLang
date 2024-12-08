
import cv2
    
def create_message_structure(message:str, files:list) -> dict:
    user_message = {"text": f"{message}", "files": files}
    return user_message


def resize(frame, new_shape=(224, 224)):
    shape = frame.shape[:2]
    k_window = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

    new_padding = int(round(shape[1] * k_window)), int(round(shape[0] * k_window))
    dw, dh = new_shape[1] - new_padding[0], new_shape[0] - new_padding[1]
    
    if shape[::-1] != new_padding: 
        frame = cv2.resize(frame, new_padding, interpolation=cv2.INTER_LINEAR)
    l, r = int(round(dw - 0.1)), int(round(dw + 0.1)) 
    t, b = int(round(dh - 0.1)), int(round(dh + 0.1))
    return cv2.copyMakeBorder(frame, t, b, l, r, cv2.BORDER_CONSTANT, value=(114, 114, 114))

if __name__ == "__main__":
    pass
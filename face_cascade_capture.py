import cv2
import tkinter as tk
from tkinter import messagebox
import os

cap = cv2.VideoCapture(0) # 웹캠 연결

root = tk.Tk()
root.title("Capture Image")

label = tk.Label(root)
label.pack()

counter=0

save_path = "C:\project\project\mywork\miniproject\captured_picture"  # 절대경로 사용, 상대경로 사용도 무관

def capture_image():
    global counter # 글로벌 함수 선언하여 전역변수로 이용
    ret, frame = cap.read()
    if ret :
        filename = os.path.join(save_path, f"captured_img{counter}.jpg")
        cv2.imwrite(filename,frame)
        counter += 1  # 캡쳐한 사진 저장할때, 사진 이름 뒤에 counter값을 넣어 캡쳐될 때 마다 사진을 저장하기 위해 counter값 사용
        messagebox.showinfo(f"Success", "이미지가 저장되었습니다{captured_image.jpg}")
    else:
        messagebox.showerror("Error", "이미지가 저장되지 않았습니다. 코드를 확인해주세요.")

capture_button = tk.Button(root, text = "Capture", command = capture_image)
capture_button.pack(pady=20)

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.imencode('.png', frame_rgb)[1].tobytes()
        img = tk.PhotoImage(data=img)
        label.config(image=img)
        label.img = img
    label.after(10, update_frame)

update_frame()

root.mainloop()

cap.release()
cv2.destroyAllWindows()



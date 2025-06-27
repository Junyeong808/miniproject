# 🛠 Mini Project: 실시간 객체 인식 및 센서 데이터 시각화 시스템

---

## 📚 프로젝트 개요  
본 프로젝트는 YOLOv8 모델(`best.pt`)을 활용해 웹캠 영상에서 실시간 객체 탐지 및 저장, MySQL DB 기록을 수행합니다.  
Flask와 WebSocket으로 센서 데이터(온도, 습도, 조도)를 실시간 웹 대시보드에 시각화합니다.  
Tkinter GUI로 웹캠 사진 캡처 기능도 포함되어 있습니다.

---

## ✨ 주요 기능  
- ✅ YOLOv8 기반 웹캠 실시간 객체 탐지 및 이미지 저장 (`main.py`)  
- ✅ Flask + Socket.IO로 실시간 센서 데이터 시각화 (`app.py`, `index.html`)  
- ✅ Tkinter 웹캠 사진 캡처 GUI (`face_cascade_captured.py`)  
- ✅ 학습된 YOLOv8 모델 파일 (`best.pt`)  

---

## 🛠 주요 기술  
- Python 3.8+  
- MySQL 8+  
- ultralytics (YOLOv8), OpenCV, Flask, Flask-SocketIO  
- pymysql, websockets  
- Tkinter GUI  

---

## 🗂 디렉토리 구성  
```plaintext
best.pt                       # YOLOv8 학습 모델 파일
main.py                       # 웹캠 객체 탐지 및 DB 저장 스크립트
app.py                        # Flask 및 WebSocket 서버 코드
index.html                    # 센서 데이터 시각화 웹페이지
face_cascade_captured.py      # Tkinter 웹캠 사진 캡처 프로그램

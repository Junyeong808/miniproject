# Mini Project: 실시간 객체 인식 및 센서 데이터 시각화 시스템

## 프로젝트 개요
본 프로젝트는 YOLOv8 모델(`best.pt`)을 사용해 웹캠 영상에서 실시간 객체를 탐지하고, 탐지된 이미지를 저장 및 MySQL 데이터베이스에 기록하는 시스템입니다.  
또한 Flask와 WebSocket을 활용하여 센서 데이터(온도, 습도, 조도)를 실시간으로 웹 대시보드에서 시각화합니다.  
Tkinter GUI를 통해 웹캠 사진을 캡처하는 기능도 포함되어 있습니다.

---

## 주요 기술
- Python 3.8 이상
- YOLOv8 (ultralytics)
- OpenCV
- Flask + Flask-SocketIO
- PyMySQL (MySQL 연동)
- WebSockets
- Tkinter (GUI)
- MySQL 8 이상

---

## 주요 기능
- YOLOv8 기반 웹캠 실시간 객체 탐지 및 이미지 저장 (`main.py`)
- MySQL 데이터베이스에 탐지 결과 및 이미지 경로 저장
- Flask + Socket.IO 기반 실시간 센서 데이터 웹 시각화 (`app.py`, `index.html`)
- Tkinter 기반 웹캠 사진 캡처 GUI (`face_cascade_captured.py`)

---

## 디렉토리 구조
├── best.pt # YOLOv8 훈련된 모델 파일
├── main.py # 웹캠 객체 탐지 및 MySQL 저장 스크립트
├── app.py # Flask 및 WebSocket 서버 스크립트
├── index.html # 실시간 센서 데이터 시각화 웹 페이지
├── face_cascade_captured.py # Tkinter 웹캠 사진 캡처 프로그램
├── captured_images/ # 탐지된 이미지 저장 폴더

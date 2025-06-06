import cv2
import torch
import os
import time
import pymysql
from datetime import datetime
from ultralytics import YOLO

class YOLOWebcam:
    def __init__(self, model_path='best.pt', save_folder="captured_images", db_config=None):
        print("웹캠 초기화 시작")
        
        self.model = YOLO(model_path)  
        print("모델 로드 완료")
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("웹캠을 열 수 없습니다. 카메라가 연결되어 있는지 확인하세요.")
        print("웹캠 연결 성공")
        
        os.makedirs(save_folder, exist_ok=True)
        self.save_folder = save_folder

        self.last_capture_time = time.time()

        self.image_counter = 0

        self.db_config = db_config or {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'object_detection'
        }
        
        try:
            self.db_connection = pymysql.connect(**self.db_config)
            self.db_cursor = self.db_connection.cursor()
            print("MySQL 연결 성공")
        except pymysql.MySQLError as e:
            print(f"MySQL 연결 오류: {e}")
            raise

    def save_image(self, frame):
        """이미지를 지정된 폴더에 저장합니다."""
        image_filename = os.path.join(self.save_folder, f"captured_image_{self.image_counter}.jpg")
        cv2.imwrite(image_filename, frame)
        print(f"이미지 저장: {image_filename}")
        
        self.image_counter += 1
        return image_filename

    def detect_and_render(self, frame):
        """훈련된 모델을 사용하여 객체를 탐지하고 결과를 이미지에 렌더링합니다."""
        results = self.model(frame)
        rendered_frame = results[0].plot()
        object_names = []
        
        if results[0].boxes is not None:
            confidence = float(box.conf[0])
            for box in results[0].boxes:
                if confidence >= 0.7:
                    class_id = int(box.cls[0])
                    object_name = results[0].names[class_id]
                    object_names.append(object_name)
        return rendered_frame, object_names

    def save_to_database(self, image_path, object_names):
        """이미지 경로와 탐지된 객체를 데이터베이스에 저장합니다."""
        capture_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for object_name in object_names:
            query = "INSERT INTO captured_images (image_path, object_name, capture_time) VALUES (%s, %s, %s)"
            values = (image_path, object_name, capture_time)
            try:
                self.db_cursor.execute(query, values)
                self.db_connection.commit()
                print(f"데이터베이스에 저장: {image_path}, 객체: {object_name}")
            except pymysql.MySQLError as err:
                print(f"데이터베이스 오류: {err}")
                self.db_connection.rollback()

    def run(self):
        """웹캠을 통해 객체 탐지 및 이미지 캡처를 실행합니다."""
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("프레임을 읽을 수 없습니다. 웹캠 연결 상태를 확인하세요.")
                    break

                detected_frame, object_names = self.detect_and_render(frame)

                current_time = time.time()
                if current_time - self.last_capture_time >= 3:
                    image_path = self.save_image(detected_frame)
                    if object_names:  
                        self.save_to_database(image_path, object_names)
                    else:
                        print(f"이미지 경로: {image_path}, 탐지된 객체 없음")
                    self.last_capture_time = current_time

                cv2.imshow('YOLO Object Detection', detected_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.db_cursor.close()
            self.db_connection.close()
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    yolo_webcam = YOLOWebcam(
        model_path='best.pt',
        save_folder="captured_images",
        db_config={
            'host': 'localhost',
            'user': 'root',
            'password': 'a12345',
            'database': 'object_detection'
        }
    )
    
    yolo_webcam.run()

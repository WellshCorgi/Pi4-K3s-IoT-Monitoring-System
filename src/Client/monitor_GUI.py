import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, font
import cv2
from PIL import Image, ImageTk
import pika
import threading
import json

class VideoStreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoring System")

        self.setup_gui()
        self.cap = None
        self.streaming = False
        self.setup_rabbitmq()

    def setup_gui(self):
        

        # Frame 생성
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack()

        # RTSP URL 입력 위젯
        self.url_label = Label(self.frame, text="RTSP URL:")
        self.url_label.grid(row=0, column=0, sticky=tk.W)
        self.url_entry = Entry(self.frame, width=50)
        self.url_entry.insert(0, 'rtsp://1.247.226.190:8554/')
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # 송출 영상 수신 시작 버튼
        self.start_button = Button(self.frame, text="Start Stream", command=self.start_stream)
        self.start_button.grid(row=1, column=0, padx=5, pady=5)

        # 송출 영상 수신 중지 버튼
        self.stop_button = Button(self.frame, text="Stop Stream", command=self.stop_stream)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5)

        # 비디오 레이블
        self.label = Label(self.root)
        self.label.pack()
        
        self.title_stream = Label(self.root, text="모니터링 진행중인 디바이스의 Resource Info" )
        self.title_stream.pack()

        # CPU 정보를 표시할 레이블
        self.cpu_label = Label(self.root, text="CPU 정보: 현재 사용율 - ")
        self.cpu_label.pack()

        # RAM 정보를 표시할 레이블
        self.ram_label = Label(self.root, text="RAM 정보: ")
        self.ram_label.pack()

    def start_stream(self):
        if self.streaming:
            messagebox.showerror("Error", "Stream is already running.")
            return

        if self.cap is not None:
            self.cap.release()

        rtsp_url = self.url_entry.get()
        rtsp_url += "?tcp"

        try:
            self.cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Failed to open video stream.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
            return

        self.streaming = True
        self.update_video_stream()

    def update_video_stream(self):
        if self.streaming:
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=pil_image)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
            else:
                # Handle stream end or error here
                messagebox.showerror("Error", "Stream ended or encountered an error.")
                self.stop_stream()
                return
            self.root.after(1, self.update_video_stream)

    def stop_stream(self):
        if self.cap is not None:
            self.cap.release()
        self.streaming = False

    def __del__(self):
        if self.cap is not None:
            self.cap.release()

    def setup_rabbitmq(self):
        try:
            credentials = pika.PlainCredentials('bochan', 'bochan')
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('1.247.226.190', 5672, '/', credentials))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='cpu-data-exchange', exchange_type='direct')
            self.channel.queue_declare(queue='stream_queue')
            self.channel.queue_bind(exchange='cpu-data-exchange', queue='stream_queue', routing_key='info')
            self.channel.basic_consume(queue='stream_queue', on_message_callback=self.on_message, auto_ack=True)
            self.rabbitmq_thread = threading.Thread(target=self.start_consuming)
            self.rabbitmq_thread.daemon = True
            self.rabbitmq_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"RabbitMQ connection failed: {str(e)}")

    def start_consuming(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            pass

    def on_message(self, ch, method, properties, body):
        message = body.decode('utf-8')
        # 메시지를 출력하고 GUI에 업데이트
        print("Received message:", message)
        self.root.after(0, self.update_message_label, message)

    def update_message_label(self, message):
        # JSON 형식의 메시지 파싱
        try:
            data = json.loads(message)
            cpu_usage = data.get("cpu_percent", "N/A")
            ram_total = data.get("ram_total", "N/A")
            ram_used = data.get("ram_used", "N/A")
            ram_free = data.get("ram_free", "N/A")
            
            # CPU 정보 업데이트
            self.cpu_label.config(text=f"CPU 정보: 현재 사용율 - {cpu_usage}%")
            
            # RAM 정보 업데이트
            self.ram_label.config(text=f"RAM 정보: 총 용량 - {ram_total}, 사용 중 - {ram_used}, 사용 가능 - {ram_free}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoStreamApp(root)
    root.mainloop()

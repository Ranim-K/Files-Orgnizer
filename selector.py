import os
import cv2
import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

# === CONFIG ===
SOURCE_FOLDER = r"C:\Users\Ranim\Desktop\Videos"
LEAVE_FOLDER = os.path.join(SOURCE_FOLDER, "to_delete")
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv")

os.makedirs(LEAVE_FOLDER, exist_ok=True)


class VideoReviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Video Reviewer — OpenCV Edition")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.videos = [os.path.join(SOURCE_FOLDER, f)
                       for f in os.listdir(SOURCE_FOLDER)
                       if f.lower().endswith(VIDEO_EXTENSIONS)]
        self.index = 0

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.labels = [QLabel() for _ in range(4)]
        for lbl in self.labels:
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("border: 2px solid #333; border-radius: 10px;")
            self.grid.addWidget(lbl, self.labels.index(lbl)//2, self.labels.index(lbl)%2)

        self.highlight_current()
        self.show_batch()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(100)

    def show_batch(self):
        self.caps = []
        for i in range(4):
            if self.index + i >= len(self.videos):
                self.labels[i].clear()
                continue
            cap = cv2.VideoCapture(self.videos[self.index + i])
            self.caps.append(cap)

    def update_frames(self):
        for i, cap in enumerate(self.caps):
            if not cap.isOpened():
                continue
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            pix = QPixmap.fromImage(img).scaled(600, 400, Qt.KeepAspectRatio)
            self.labels[i].setPixmap(pix)

    def highlight_current(self):
        for i, lbl in enumerate(self.labels):
            if i == 0:
                lbl.setStyleSheet("border: 5px solid #00FFAA; border-radius: 10px;")
            else:
                lbl.setStyleSheet("border: 2px solid #333; border-radius: 10px;")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_K:
            self.keep_video()
        elif key == Qt.Key_D:
            self.delete_video()
        elif key == Qt.Key_A:
            self.delete_all()
        else:
            return
        self.next_batch()

    def keep_video(self):
        if self.index < len(self.videos):
            print(f"✅ Kept: {os.path.basename(self.videos[self.index])}")
            self.index += 1

    def delete_video(self):
        if self.index < len(self.videos):
            path = self.videos[self.index]
            shutil.move(path, os.path.join(LEAVE_FOLDER, os.path.basename(path)))
            print(f"🗑️  Moved: {os.path.basename(path)}")
            self.index += 1

    def delete_all(self):
        for _ in range(4):
            if self.index >= len(self.videos):
                break
            self.delete_video()

    def next_batch(self):
        if self.index >= len(self.videos):
            QMessageBox.information(self, "Done", "All videos reviewed ✅")
            self.close()
            return
        self.show_batch()
        self.highlight_current()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = VideoReviewer()
    viewer.show()
    sys.exit(app.exec_())

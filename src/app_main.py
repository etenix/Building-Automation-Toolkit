import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from image_engine import ImagePreprocessor

class AutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("建築外壁解析自動化ツール")
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_load = QPushButton("解析対象画像をロード")
        self.btn_load.clicked.connect(self.load_image)
        layout.addWidget(self.btn_load)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "画像選択")
        if file_path:
            print(f"解析開始: {file_path}")
            # ここでImagePreprocessorやTileCounterを呼び出す

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomationApp()
    window.show()
    sys.exit(app.exec())
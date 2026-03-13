import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

# 以前作成した自作モジュールをインポート
from image_engine import ImagePreprocessor
from tile_detector import TileCounter
from excel_exporter import ExcelReporter

class BuildingAutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. UIファイルのロード
        self.load_ui()
        
        # 2. 各解析エンジンの初期化
        self.preprocessor = ImagePreprocessor()
        self.detector = TileCounter()
        self.reporter = ExcelReporter()
        
        # 3. シグナル（ボタン操作）とスロット（関数）の接続
        self.setup_connections()

    def load_ui(self):
        """Qt Designerで作成した .ui ファイルを読み込む"""
        loader = QUiLoader()
        # パス設定（resourcesフォルダ内のuiファイルを指定）
        ui_path = os.path.join(os.path.dirname(__file__), "../resources/ui_layout.ui")
        ui_file = QFile(ui_path)
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"Cannot open {ui_path}: {ui_file.errorString()}")
            sys.exit(-1)
            
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        # メインウィンドウとして設定
        self.setCentralWidget(self.ui)
        self.setWindowTitle(self.ui.windowTitle())

    def setup_connections(self):
        """UI上のボタンとPython関数を紐付ける"""
        self.ui.btn_open_image.clicked.connect(self.handle_open_image)
        self.ui.btn_run_analysis.clicked.connect(self.handle_run_analysis)
        self.ui.btn_export_excel.clicked.connect(self.handle_export_excel)

    def handle_open_image(self):
        """画像ファイルを選択してプレビュー表示（シミュレーション）"""
        file_path, _ = QFileDialog.getOpenFileName(self, "画像を開く", "", "Image Files (*.jpg *.png *.bmp)")
        if file_path:
            self.current_image_path = file_path
            self.ui.textEdit_results.append(f"画像を読み込みました: {os.path.basename(file_path)}")
            # 本来はここで graphicsView_preview に画像を表示する処理を記述

    def handle_run_analysis(self):
        """AI解析（タイル検知）の実行"""
        if not hasattr(self, 'current_image_path'):
            QMessageBox.warning(self, "警告", "先に画像を読み込んでください。")
            return
            
        self.ui.textEdit_results.append("AI解析を実行中...")
        
        # ダミー処理：本来は detector.count_tiles(img) を実行
        count, summary = self.detector.count_tiles(None) 
        self.last_results = (count, summary)
        
        self.ui.textEdit_results.append(f"解析完了！ 総タイル数: {count}枚")
        for key, val in summary.items():
            self.ui.textEdit_results.append(f" - {key}: {val}枚")

    def handle_export_excel(self):
        """解析結果をExcelに出力"""
        if not hasattr(self, 'last_results'):
            QMessageBox.warning(self, "警告", "解析を先に実行してください。")
            return
            
        count, summary = self.last_results
        path = self.reporter.export_to_excel(count, summary)
        
        if path:
            QMessageBox.information(self, "完了", f"レポートを保存しました:\n{path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuildingAutomationApp()
    window.show()
    sys.exit(app.exec())
# src/__init__.py
"""
Building-Automation-Toolkit
建築外壁解析および数量算出自動化システム
"""

from .image_engine import ImagePreprocessor
from .tile_detector import TileCounter
from .excel_exporter import ExcelReporter

__version__ = "1.0.0"
__author__ = "Haoran"
__description__ = "OpenCVとYOLOv5を統合した建築実務支援DXツール"

# アプリケーション実行時のリソースパス設定や初期化処理
import os
import sys

# 実行環境のパスを解決（実行ファイル化した際のパス対応）
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
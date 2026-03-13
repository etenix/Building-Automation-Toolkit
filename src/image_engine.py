import cv2
import numpy as np

class ImagePreprocessor:
    """
    外壁診断用写真の歪み補正および鮮鋭化
    """
    @staticmethod
    def correct_perspective(image, pts1):
        """
        OpenCVを用いた透視変換（パース補正）
        """
        # ターゲットとなる長方形のサイズ
        width, height = 800, 600
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        
        # 変換行列の算出と適用
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(image, matrix, (width, height))
        return result

    @staticmethod
    def enhance_features(image):
        """
        タイルの目地を強調するためのフィルタリング処理
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 適応的ヒストグラム平滑化(CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(gray)
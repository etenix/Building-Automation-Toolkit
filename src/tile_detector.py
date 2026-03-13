import torch

class TileCounter:
    def __init__(self, model_path='weights/tile_yolo.pt'):
        # 建築外壁タイル専用に学習させたYOLOモデル
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    def count_tiles(self, image):
        """
        タイルを識別し、総数を算出
        """
        results = self.model(image)
        df = results.pandas().xyxy[0]
        tile_count = len(df)
        
        # 識別結果の統計（例：正常、剥離、ひび割れ等の分類）
        summary = df['name'].value_counts().to_dict()
        return tile_count, summary
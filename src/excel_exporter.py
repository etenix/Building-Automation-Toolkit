# src/excel_exporter.py
import pandas as pd
from datetime import datetime
from pathlib import Path

class ExcelReporter:
    """
    AI解析結果（タイルの数量、状態）をExcelレポートとして出力する
    """
    def __init__(self, output_dir="../output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_to_excel(self, tile_count, summary_dict, project_name="Project_Alpha"):
        """
        解析結果を整理し、タイムスタンプ付きで保存
        """
        # 1. データの整理
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "項目": ["総タイル数"] + list(summary_dict.keys()),
            "数値/状態": [tile_count] + list(summary_dict.values()),
            "単位": ["枚"] + ["枚"] * len(summary_dict)
        }
        
        df = pd.DataFrame(report_data)

        # 2. Excelファイルへの書き出し
        file_name = f"{project_name}_Analysis_{timestamp}.xlsx"
        file_path = self.output_dir / file_name
        
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='解析レポート')
                
                # Excelの書式設定（列幅の自動調整など）をここに追加可能
                worksheet = writer.sheets['解析レポート']
                worksheet.column_dimensions['A'].width = 25
                worksheet.column_dimensions['B'].width = 15

            print(f"レポート出力完了: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"Excel出力エラー: {e}")
            return None

if __name__ == "__main__":
    # テスト用ダミーデータ
    dummy_summary = {"正常": 450, "剥離可能性あり": 12, "ひび割れ": 5}
    reporter = ExcelReporter()
    reporter.export_to_excel(467, dummy_summary)
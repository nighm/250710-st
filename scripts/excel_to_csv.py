import os
import pandas as pd

EXCEL_PATH = os.path.join('data', '测试结果-20250709.xlsx')
CSV_PATH = os.path.join('data', '测试结果-20250709.csv')

def excel_to_csv(excel_path, csv_path):
    if not os.path.exists(excel_path):
        print(f"未找到 Excel 文件: {excel_path}")
        return
    if os.path.exists(csv_path):
        print(f"CSV 文件已存在: {csv_path}，未做覆盖。")
        return
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # 关键修正
        print(f"已成功将 {excel_path} 转换为 {csv_path}（utf-8-sig 编码，Excel 可正常打开）")
    except Exception as e:
        print(f"转换失败: {e}")

if __name__ == "__main__":
    excel_to_csv(EXCEL_PATH, CSV_PATH) 
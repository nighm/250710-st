import pandas as pd

def read_excel_cases(file_path):
    """
    读取 Excel 文件，返回 DataFrame
    :param file_path: Excel 文件路径
    :return: pandas.DataFrame
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        print(f"读取 Excel 失败: {e}")
        return None

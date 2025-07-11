import os
import pandas as pd
import re
import json
from datetime import datetime

CSV_PATH = os.path.join('data', '测试结果-20250709.csv')
CASES_DIR = os.path.join('data', 'cases', 'json')

os.makedirs(CASES_DIR, exist_ok=True)

def safe_part(s):
    if pd.isna(s) or str(s).strip().lower() == 'nan':
        return ''
    return re.sub(r'[\s\u3000]+', '', str(s)).replace('/', '_').replace('\\', '_').replace(':', '_')

def clean_value(v):
    if pd.isna(v) or str(v).strip().lower() == 'nan':
        return ''
    return str(v).strip()

def row_to_json(row):
    # 重要级别处理
    level = row.get('重要级别', '')
    if not pd.isna(level):
        try:
            level = int(float(level))
        except Exception:
            level = level
    else:
        level = ''
    # 组装dict
    data = {
        '需求编号': clean_value(row.get('需求编号', '')),
        '需求描述': clean_value(row.get('需求描述', '')),
        '子功能1': clean_value(row.get('Unnamed: 2', '')),
        '子功能2': clean_value(row.get('Unnamed: 3', '')),
        '子功能3': clean_value(row.get('Unnamed: 4', '')),
        '对应功能项': clean_value(row.get('对应功能项', '')),
        '对应子功能1': clean_value(row.get('Unnamed: 6', '')),
        '对应子功能2': clean_value(row.get('Unnamed: 7', '')),
        '对应子功能3': clean_value(row.get('Unnamed: 8', '')),
        '测试用例编号': clean_value(row.get('测试用例编号', '')),
        '测试用例名称': clean_value(row.get('测试用例名称', '')),
        '预置条件': clean_value(row.get('预置条件', '')),
        '操作步骤': clean_value(row.get('操作步骤', '')),
        '预期输出': clean_value(row.get('预期输出', '')),
        '重要级别': level,
        '测试类型': clean_value(row.get('测试类型', '')),
        '适用阶段': clean_value(row.get('适用阶段', '')),
        '测试结果': clean_value(row.get('测试结果', '')),
        '最近执行人': clean_value(row.get('最近执行人', '')),
        '备注': clean_value(row.get('备注', '')),
        '创建时间': datetime.now().strftime('%Y-%m-%d'),
        'can_automate': True
    }
    return data

def main():
    df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
    if df.empty:
        print('CSV文件无内容')
        return
    for i, row in df.iterrows():
        req_id = safe_part(row.get('需求编号', ''))
        case_id = safe_part(row.get('测试用例编号', ''))
        func_parts = [row.get('对应功能项', '')]
        for sub in ['Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']:
            val = str(row.get(sub, ''))
            if val.strip() and val.strip().lower() != 'nan':
                func_parts.append(val.strip())
        func_parts = [safe_part(p) for p in func_parts if p and p != '']
        func_path = '_'.join(func_parts)
        filename = f"{req_id}-{case_id}-{func_path}.json".strip()
        filepath = os.path.join(CASES_DIR, filename)
        data = row_to_json(row)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'已生成: {filepath}')

if __name__ == '__main__':
    main() 
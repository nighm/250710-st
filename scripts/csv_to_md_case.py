import os
import pandas as pd
from datetime import datetime
import re

CSV_PATH = os.path.join('data', '测试结果-20250709.csv')
CASES_DIR = 'cases'

os.makedirs(CASES_DIR, exist_ok=True)

def safe_part(s):
    if pd.isna(s) or str(s).strip().lower() == 'nan':
        return ''
    # 去除所有空格（包括全角、半角、所有位置）
    return re.sub(r'[\s\u3000]+', '', str(s)).replace('/', '_').replace('\\', '_').replace(':', '_')

def clean_value(v):
    if pd.isna(v) or str(v).strip().lower() == 'nan':
        return ''
    return str(v).strip()

def beautify_multiline(value):
    v = clean_value(value)
    if not v:
        return ''
    lines = [l.strip() for l in v.splitlines() if l.strip()]
    return '\n'.join([f"- {l}" for l in lines])

def main():
    df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
    if df.empty:
        print('CSV文件无内容')
        return
    row = df.iloc[0]
    # 文件名格式：需求编号-测试用例编号-对应功能项_子功能1_子功能2_子功能3.md
    req_id = safe_part(row.get('需求编号', ''))
    case_id = safe_part(row.get('测试用例编号', ''))
    func_parts = [row.get('对应功能项', '')]
    for sub in ['Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']:
        val = row.get(sub, '')
        if not pd.isna(val) and str(val).strip().lower() != 'nan' and str(val).strip():
            func_parts.append(str(val).strip())
    func_parts = [safe_part(p) for p in func_parts if p and p != '']
    func_path = '_'.join(func_parts)
    filename = f"{req_id}-{case_id}-{func_path}.md".strip()
    title = f"{req_id}-{case_id}-{func_path}".strip()
    filepath = os.path.join(CASES_DIR, filename)
    # 重要级别处理
    level = row.get('重要级别', '')
    if not pd.isna(level):
        try:
            level = int(float(level))
        except Exception:
            level = level
    else:
        level = ''
    # 组装内容
    content = [f"# {title}\n"]
    # 需求编号
    content.append(f"需求编号: {clean_value(row.get('需求编号', ''))}\n")
    # 需求描述及子功能1/2/3
    content.append(f"需求描述: {clean_value(row.get('需求描述', ''))}\n")
    content.append(f"子功能1: {clean_value(row.get('Unnamed: 2', ''))}\n")
    content.append(f"子功能2: {clean_value(row.get('Unnamed: 3', ''))}\n")
    content.append(f"子功能3: {clean_value(row.get('Unnamed: 4', ''))}\n")
    content.append("")
    # 对应功能项及其子功能1/2/3
    content.append(f"对应功能项: {clean_value(row.get('对应功能项', ''))}\n")
    content.append(f"子功能1: {clean_value(row.get('Unnamed: 6', ''))}\n")
    content.append(f"子功能2: {clean_value(row.get('Unnamed: 7', ''))}\n")
    content.append(f"子功能3: {clean_value(row.get('Unnamed: 8', ''))}\n")
    content.append("")
    # 其余字段
    fields = [
        ('测试用例编号', '测试用例编号'),
        ('测试用例名称', '测试用例名称'),
        ('预置条件', '预置条件'),
        ('操作步骤', '操作步骤'),
        ('预期输出', '预期输出'),
        ('重要级别', '重要级别'),
        ('测试类型', '测试类型'),
        ('适用阶段', '适用阶段'),
        ('测试结果', '测试结果'),
        ('最近执行人', '最近执行人'),
        ('备注', '备注'),
    ]
    for field, col in fields:
        v = row.get(col, '')
        if field == '重要级别':
            v = level
        if field in ['操作步骤', '预置条件', '预期输出']:
            pretty = beautify_multiline(v)
            content.append(f"{field}:\n{pretty}\n" if pretty else f"{field}:\n\n")
        else:
            v = clean_value(v)
            content.append(f"{field}: {v}\n")
    content.append(f"创建时间: {datetime.now().strftime('%Y-%m-%d')}\n")
    content.append(f"can_automate: true\n")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    print(f'已生成: {filepath}')

if __name__ == '__main__':
    main() 
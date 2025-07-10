# 自动化测试项目

项目简介：基于 Playwright + pandas 的网页自动化测试系统。

## 当前版本

v1.0.0

## Changelist（变更记录）

- v1.0.0
  - 项目结构初始化
  - Excel转CSV自动化脚本
  - 用例md文件自动生成脚本
  - 用例md格式优化（字段分块、分行、分组、无拼接）
  - 自动上传GitHub脚本

## 版本迭代

- v1.0.0：项目初始化，支持用例数据自动化处理与管理
- v1.1.0：待定（请在此处记录后续功能/优化/修复等）

---

## 使用说明

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. 运行脚本：
   - Excel转CSV：`python scripts/excel_to_csv.py`
   - 用例md生成：`python scripts/csv_to_md_case.py`
   - 自动上传GitHub：`python scripts/upload_to_github.py`

---

如需更多自动化、协作、持续集成等功能，欢迎持续关注和反馈！

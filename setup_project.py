import os

# 项目结构定义
dirs = [
    'auto_web_test/config',
    'auto_web_test/data',
    'auto_web_test/logs',
    'auto_web_test/src/web',
    'auto_web_test/tests',
]

files = {
    'auto_web_test/README.md': '# 自动化测试项目\n\n项目简介：基于 Playwright + pandas 的网页自动化测试系统。',
    'auto_web_test/requirements.txt': 'playwright\npandas\nopenpyxl\n',
    'auto_web_test/config/settings.yaml': '# 配置文件示例\nurl: http://192.168.24.100\nusername: your_username\npassword: your_password\n',
    'auto_web_test/src/main.py': '# 主入口脚本\nif __name__ == "__main__":\n    print("自动化测试项目入口")\n',
    'auto_web_test/src/excel_utils.py': '# Excel 读写工具模块\n',
    'auto_web_test/src/web/base_page.py': '# 页面基类，封装通用操作\n',
    'auto_web_test/src/web/login_page.py': '# 登录页面操作封装\n',
    'auto_web_test/src/web/test_page.py': '# 业务页面操作封装\n',
    'auto_web_test/src/runner.py': '# 用例调度与执行模块\n',
    'auto_web_test/src/reporter.py': '# 结果统计与报告模块\n',
    'auto_web_test/src/utils.py': '# 通用工具函数\n',
    'auto_web_test/tests/test_cases.py': '# 自动化测试用例示例\n',
}

def create_dirs():
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"创建目录: {d}")

def create_files():
    for path, content in files.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"创建文件: {path}")

def main():
    create_dirs()
    create_files()
    print("\n项目基础结构已创建完毕！")

if __name__ == "__main__":
    main() 
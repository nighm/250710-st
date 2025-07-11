import os
import subprocess

def run(cmd):
    print(f"运行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def main():
    # 检查是否已初始化git仓库
    if not os.path.exists('.git'):
        run('git init')
    # 添加所有文件
    run('git add .')
    # 提交
    run('git commit -m "init: 项目初始化及自动化脚本"')
    # 设置主分支
    run('git branch -M main')
    # 设置远程origin
    run('git remote remove origin')  # 防止已存在origin
    run('git remote add origin https://github.com/nighm/250710-st.git')
    # 推送到main分支
    run('git push -u origin main')

if __name__ == '__main__':
    main() 
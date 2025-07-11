import os
import subprocess

def run(cmd):
    print(f"运行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def main():
    # 检查是否已初始化git仓库
    if not os.path.exists('.git'):
        run('git init')
    
    # 设置远程origin
    run('git remote remove origin')  # 防止已存在origin
    run('git remote add origin https://github.com/nighm/250710-st.git')
    
    # 尝试拉取远程更改
    print("尝试拉取远程更改...")
    pull_result = run('git pull origin main --allow-unrelated-histories')
    
    # 添加所有文件
    run('git add .')
    # 提交
    run('git commit -m "feat: 智能网页自动化测试框架 - 支持智能登录、动态页面分析、灵活测试执行"')
    # 设置主分支
    run('git branch -M main')
    # 推送到main分支（强制覆盖）
    run('git push -u origin main --force')

if __name__ == '__main__':
    main() 
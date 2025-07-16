import os
import subprocess
import argparse
import sys
import socket


def run(cmd):
    print(f"运行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def check_github_connectivity():
    try:
        socket.create_connection(("github.com", 443), timeout=5)
        return True
    except Exception:
        return False

def git_init(remote_url, branch):
    if not os.path.exists('.git'):
        run('git init')
    run('git add .')
    run('git commit -m "init: 项目初始化及自动化脚本"')
    run(f'git branch -M {branch}')
    run('git remote remove origin')
    run(f'git remote add origin {remote_url}')
    run(f'git push -u origin {branch}')

def git_push(commit_msg, branch):
    run('git add .')
    run(f'git commit -m "{commit_msg}"')
    if not check_github_connectivity():
        print("[错误] 无法连接到github.com:443，请检查网络或代理设置！")
        return
    code = run(f'git push origin {branch}')
    if code != 0:
        print("[错误] 推送到GitHub失败，请检查网络、权限或远程仓库配置！")
    else:
        print("[成功] 已同步到GitHub远程仓库。")

def git_pull(branch, allow_unrelated):
    cmd = f'git pull origin {branch}'
    if allow_unrelated:
        cmd += ' --allow-unrelated-histories'
    run(cmd)

def git_status():
    run('git status')

def get_version_from_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('## 版本：'):
                    return line.strip().replace('## 版本：', '').strip()
    except Exception:
        pass
    return 'auto: 本地自动同步'

def default_flow(branch):
    print("\n[默认操作] 显示状态 → 拉取远程 → 推送本地\n")
    git_status()
    git_pull(branch, allow_unrelated=True)
    version = get_version_from_readme()
    git_push(f"auto: 本地自动同步（版本 {version}）", branch)

def main():
    parser = argparse.ArgumentParser(description='GitHub自动化工具', add_help=True)
    parser.add_argument('action', nargs='?', choices=['init', 'push', 'pull', 'status'], help='操作类型')
    parser.add_argument('-m', '--message', default=None, help='提交说明（push时用）')
    parser.add_argument('-b', '--branch', default='main', help='分支名')
    parser.add_argument('-r', '--remote', default='https://github.com/nighm/250710-st.git', help='远程仓库地址（init用）')
    parser.add_argument('--allow-unrelated', action='store_true', help='pull时允许合并无关历史')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        # 无参数，执行默认操作
        default_flow(args.branch)
        return

    if args.action == 'init':
        git_init(args.remote, args.branch)
    elif args.action == 'push':
        msg = args.message or f"auto: 本地自动同步（版本 {get_version_from_readme()}）"
        git_push(msg, args.branch)
    elif args.action == 'pull':
        git_pull(args.branch, args.allow_unrelated)
    elif args.action == 'status':
        git_status()

if __name__ == '__main__':
    main() 
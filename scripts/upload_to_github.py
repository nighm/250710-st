import os
import subprocess
import argparse
import sys


def run(cmd):
    print(f"运行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

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
    run(f'git push origin {branch}')

def git_pull(branch, allow_unrelated):
    cmd = f'git pull origin {branch}'
    if allow_unrelated:
        cmd += ' --allow-unrelated-histories'
    run(cmd)

def git_status():
    run('git status')

def default_flow(branch):
    print("\n[默认操作] 显示状态 → 拉取远程 → 推送本地\n")
    git_status()
    git_pull(branch, allow_unrelated=True)
    git_push("auto: 本地自动同步", branch)

def main():
    parser = argparse.ArgumentParser(description='GitHub自动化工具', add_help=True)
    parser.add_argument('action', nargs='?', choices=['init', 'push', 'pull', 'status'], help='操作类型')
    parser.add_argument('-m', '--message', default='auto: 更新内容', help='提交说明（push时用）')
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
        git_push(args.message, args.branch)
    elif args.action == 'pull':
        git_pull(args.branch, args.allow_unrelated)
    elif args.action == 'status':
        git_status()

if __name__ == '__main__':
    main() 
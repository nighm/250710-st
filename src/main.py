"""
自动化测试项目主入口
提供测试执行的主要接口
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.interfaces.test_cli import TestCLI


def main():
    """
    主函数 - 自动化测试项目入口
    
    提供以下功能:
    1. 测试用例管理
    2. 自动化测试执行
    3. 测试结果报告
    4. 配置管理
    """
    print("=" * 80)
    print("自动化测试项目")
    print("基于DDD架构的Web自动化测试框架")
    print("=" * 80)
    
    # 检查项目结构
    if not _check_project_structure():
        print("❌ 项目结构检查失败，请确保项目文件完整")
        return
    
    # 运行CLI
    try:
        cli = TestCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        sys.exit(1)


def _check_project_structure():
    """
    检查项目结构是否完整
    
    Returns:
        项目结构是否完整
    """
    required_dirs = [
        "src/domain",
        "src/application", 
        "src/infrastructure",
        "src/interfaces",
        "src/web",
        "data/cases/json",
        "config"
    ]
    
    required_files = [
        "src/domain/test_case.py",
        "src/application/test_execution_service.py",
        "src/infrastructure/config_loader.py",
        "src/infrastructure/test_case_repository.py",
        "src/interfaces/test_cli.py",
        "src/web/base_page.py",
        "src/web/login_page.py",
        "src/web/user_management_page.py",
        "requirements.txt"
    ]
    
    # 检查目录
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ 缺少目录: {dir_path}")
            return False
    
    # 检查文件
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    print("✅ 项目结构检查通过")
    return True


if __name__ == "__main__":
    main()

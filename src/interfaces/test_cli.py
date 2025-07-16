"""
测试CLI接口
提供命令行工具来执行自动化测试
"""
import argparse
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from ..application.test_execution_service import TestExecutionService
from ..infrastructure.config_loader import ConfigLoader
from ..infrastructure.test_case_repository import TestCaseRepository


class TestCLI:
    """测试CLI类"""
    
    def __init__(self):
        """初始化CLI"""
        self.test_service = TestExecutionService()
        self.config_loader = ConfigLoader()
        self.test_repository = TestCaseRepository()
    
    def run(self):
        """运行CLI"""
        parser = argparse.ArgumentParser(
            description="自动化测试工具",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
使用示例:
  python -m src.interfaces.test_cli list                    # 列出所有测试用例
  python -m src.interfaces.test_cli run TC_1_1_1            # 执行指定测试用例
  python -m src.interfaces.test_cli run-all                  # 执行所有可自动化测试用例
  python -m src.interfaces.test_cli stats                    # 显示测试统计信息
  python -m src.interfaces.test_cli config                   # 显示配置信息
  python -m src.interfaces.test_cli init-config              # 初始化配置文件
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        # 列出测试用例命令
        list_parser = subparsers.add_parser('list', help='列出所有测试用例')
        list_parser.add_argument('--automated', action='store_true', help='只显示可自动化的测试用例')
        list_parser.add_argument('--function', type=str, help='按功能筛选')
        
        # 执行测试用例命令
        run_parser = subparsers.add_parser('run', help='执行测试用例')
        run_parser.add_argument('test_case_id', type=str, help='测试用例ID')
        run_parser.add_argument('--headless', action='store_true', default=True, help='无头模式')
        run_parser.add_argument('--output', type=str, help='输出结果文件路径')
        
        # 执行所有测试用例命令
        run_all_parser = subparsers.add_parser('run-all', help='执行所有可自动化的测试用例')
        run_all_parser.add_argument('--headless', action='store_true', default=True, help='无头模式')
        run_all_parser.add_argument('--output', type=str, help='输出结果文件路径')
        
        # 统计信息命令
        stats_parser = subparsers.add_parser('stats', help='显示测试统计信息')
        
        # 配置信息命令
        config_parser = subparsers.add_parser('config', help='显示配置信息')
        
        # 初始化配置命令
        init_config_parser = subparsers.add_parser('init-config', help='初始化配置文件')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            if args.command == 'list':
                self.list_test_cases(args)
            elif args.command == 'run':
                self.run_test_case(args)
            elif args.command == 'run-all':
                self.run_all_test_cases(args)
            elif args.command == 'stats':
                self.show_statistics()
            elif args.command == 'config':
                self.show_config()
            elif args.command == 'init-config':
                self.init_config()
        except Exception as e:
            print(f"执行命令时发生错误: {e}")
            sys.exit(1)
    
    def list_test_cases(self, args):
        """列出测试用例"""
        print("=" * 80)
        print("测试用例列表")
        print("=" * 80)
        
        if args.automated:
            test_cases = self.test_repository.load_automated_test_cases()
            print(f"可自动化的测试用例 (共 {len(test_cases)} 个):")
        else:
            test_cases = self.test_repository.load_all_test_cases()
            print(f"所有测试用例 (共 {len(test_cases)} 个):")
        
        if args.function:
            test_cases = [tc for tc in test_cases if tc.corresponding_function == args.function]
            print(f"按功能 '{args.function}' 筛选 (共 {len(test_cases)} 个):")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. 测试用例ID: {test_case.test_case_id}")
            print(f"   测试用例名称: {test_case.test_case_name}")
            print(f"   对应功能: {test_case.corresponding_function}")
            print(f"   对应子功能: {test_case.corresponding_sub_function1}")
            print(f"   重要级别: {test_case.importance_level}")
            print(f"   测试类型: {test_case.test_type}")
            print(f"   可自动化: {'是' if test_case.is_automated() else '否'}")
            print(f"   测试结果: {test_case.test_result}")
            print(f"   最近执行人: {test_case.recent_executor}")
            print("-" * 80)
    
    def run_test_case(self, args):
        """执行指定测试用例"""
        test_case_id = args.test_case_id
        
        print(f"开始执行测试用例: {test_case_id}")
        print("=" * 50)
        
        # 执行测试用例
        result = self.test_service.execute_specific_test_case(test_case_id)
        
        # 显示结果
        self._display_test_result(result)
        
        # 保存结果到文件
        if args.output:
            self._save_result_to_file(result, args.output)
    
    def run_all_test_cases(self, args):
        """执行所有可自动化的测试用例"""
        print("开始执行所有可自动化的测试用例")
        print("=" * 50)
        
        # 执行所有测试用例
        results = self.test_service.execute_all_automated_tests()
        
        # 显示结果
        self._display_all_results(results)
        
        # 保存结果到文件
        if args.output:
            self._save_results_to_file(results, args.output)
    
    def show_statistics(self):
        """显示测试统计信息"""
        print("=" * 80)
        print("测试用例统计信息")
        print("=" * 80)
        
        stats = self.test_repository.get_test_case_statistics()
        
        print(f"总测试用例数: {stats['total_count']}")
        print(f"可自动化测试用例数: {stats['automated_count']}")
        print(f"自动化率: {stats['automation_rate']:.2%}")
        
        print("\n按功能分组:")
        for function, count in stats['by_function'].items():
            print(f"  {function}: {count} 个")
        
        print("\n按重要级别分组:")
        for level, count in sorted(stats['by_importance'].items()):
            print(f"  级别 {level}: {count} 个")
    
    def show_config(self):
        """显示配置信息"""
        print("=" * 80)
        print("配置信息")
        print("=" * 80)
        
        try:
            web_config = self.config_loader.get_web_config()
            print(f"基础URL: {web_config['base_url']}")
            print(f"用户名: {web_config['username']}")
            print(f"密码: {'*' * len(web_config['password'])}")
            print(f"超时时间: {web_config['timeout']} 秒")
            print(f"无头模式: {web_config['headless']}")
            print(f"慢动作: {web_config['slow_mo']} 毫秒")
            
            print(f"\n测试数据路径: {self.config_loader.get_test_data_path()}")
            print(f"结果保存路径: {self.config_loader.get_results_path()}")
            
            # 验证配置
            if self.config_loader.validate_config():
                print("\n配置验证: ✅ 通过")
            else:
                print("\n配置验证: ❌ 失败")
                
        except Exception as e:
            print(f"读取配置失败: {e}")
    
    def init_config(self):
        """初始化配置文件"""
        print("正在创建默认配置文件...")
        self.config_loader.create_default_config()
        print("配置文件创建完成！")
        print("请编辑 config/settings.yaml 文件，填入正确的系统访问信息。")
    
    def _display_test_result(self, result: Dict[str, Any]):
        """显示单个测试结果"""
        if "error" in result:
            print(f"❌ 执行失败: {result['error']}")
            return
        
        print(f"测试用例ID: {result['test_case_id']}")
        print(f"测试用例名称: {result['test_case_name']}")
        print(f"执行状态: {result['status']}")
        print(f"开始时间: {result['start_time']}")
        print(f"执行时间: {result['execution_time']:.2f} 秒")
        
        if result['error_message']:
            print(f"错误信息: {result['error_message']}")
        
        if result['screenshot_path']:
            print(f"截图路径: {result['screenshot_path']}")
        
        status_icon = "✅" if result['status'] == "PASSED" else "❌"
        print(f"\n{status_icon} 测试用例执行完成")
    
    def _display_all_results(self, results: List[Dict[str, Any]]):
        """显示所有测试结果"""
        total_count = len(results)
        passed_count = len([r for r in results if r.get('status') == 'PASSED'])
        failed_count = total_count - passed_count
        
        print(f"\n执行完成！")
        print(f"总测试用例数: {total_count}")
        print(f"通过: {passed_count}")
        print(f"失败: {failed_count}")
        print(f"通过率: {passed_count/total_count:.2%}" if total_count > 0 else "通过率: 0%")
        
        print("\n详细结果:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('test_case_id', 'Unknown')}")
            print(f"   状态: {result.get('status', 'Unknown')}")
            print(f"   执行时间: {result.get('execution_time', 0):.2f} 秒")
            if result.get('error_message'):
                print(f"   错误: {result['error_message']}")
    
    def _save_result_to_file(self, result: Dict[str, Any], file_path: str):
        """保存单个结果到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {file_path}")
        except Exception as e:
            print(f"保存结果失败: {e}")
    
    def _save_results_to_file(self, results: List[Dict[str, Any]], file_path: str):
        """保存所有结果到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {file_path}")
        except Exception as e:
            print(f"保存结果失败: {e}")


def main():
    """主函数"""
    cli = TestCLI()
    cli.run()


if __name__ == "__main__":
    main() 
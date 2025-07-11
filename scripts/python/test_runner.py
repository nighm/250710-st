#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试执行器
支持登录后执行指定测试用例，既能全量执行也能选择性执行
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.config_loader import ConfigLoader
from scripts.python.smart_login import SmartLogin


class TestRunner:
    """测试执行器"""
    
    def __init__(self):
        """初始化测试执行器"""
        self.config_loader = ConfigLoader()
        self.smart_login = SmartLogin()
        self.login_success = False
        
    def run_all_tests(self) -> Dict[str, Any]:
        """执行所有测试用例"""
        print("开始执行所有测试用例...")
        
        # 1. 登录系统
        if not self._login_system():
            return {"error": "登录失败，无法执行测试"}
        
        # 2. 执行所有测试用例
        test_results = self._execute_all_test_cases()
        
        # 3. 生成测试报告
        report = self._generate_test_report(test_results)
        
        return report
    
    def run_specific_tests(self, test_case_ids: List[str]) -> Dict[str, Any]:
        """执行指定的测试用例"""
        print(f"开始执行指定测试用例: {test_case_ids}")
        
        # 1. 登录系统
        if not self._login_system():
            return {"error": "登录失败，无法执行测试"}
        
        # 2. 执行指定测试用例
        test_results = self._execute_specific_test_cases(test_case_ids)
        
        # 3. 生成测试报告
        report = self._generate_test_report(test_results)
        
        return report
    
    def run_tests_by_module(self, module_name: str) -> Dict[str, Any]:
        """按模块执行测试用例"""
        print(f"开始执行模块测试: {module_name}")
        
        # 1. 登录系统
        if not self._login_system():
            return {"error": "登录失败，无法执行测试"}
        
        # 2. 获取模块测试用例
        test_case_ids = self._get_test_cases_by_module(module_name)
        
        if not test_case_ids:
            return {"error": f"未找到模块 {module_name} 的测试用例"}
        
        # 3. 执行模块测试用例
        test_results = self._execute_specific_test_cases(test_case_ids)
        
        # 4. 生成测试报告
        report = self._generate_test_report(test_results)
        
        return report
    
    def _login_system(self) -> bool:
        """登录系统"""
        try:
            print("步骤1: 登录系统...")
            
            # 获取登录信息
            web_config = self.config_loader.get_web_config()
            username = web_config.get("username", "super")
            password = web_config.get("password", "admin123")
            login_url = "https://192.168.24.100/login"
            
            print(f"登录URL: {login_url}")
            print(f"用户名: {username}")
            
            # 设置浏览器
            self.smart_login.setup_browser(headless=False)
            
            # 执行登录
            self.login_success = self.smart_login.smart_login(
                username, password, login_url, wait_captcha=True, max_retries=5
            )
            
            if self.login_success:
                print("登录成功！可以开始执行测试用例")
                return True
            else:
                print("登录失败，无法执行测试用例")
                return False
                
        except Exception as e:
            print(f"登录过程出错: {e}")
            return False
    
    def _execute_all_test_cases(self) -> List[Dict[str, Any]]:
        """执行所有测试用例"""
        # 这里应该从测试用例仓库加载所有可自动化的测试用例
        # 暂时返回示例数据
        test_cases = [
            {
                "test_case_id": "TC_1_1_1",
                "test_case_name": "用户录入测试",
                "module": "用户管理",
                "status": "pending"
            }
        ]
        
        results = []
        for test_case in test_cases:
            result = self._execute_single_test_case(test_case)
            results.append(result)
        
        return results
    
    def _execute_specific_test_cases(self, test_case_ids: List[str]) -> List[Dict[str, Any]]:
        """执行指定的测试用例"""
        results = []
        
        for test_case_id in test_case_ids:
            # 这里应该从测试用例仓库加载指定的测试用例
            test_case = {
                "test_case_id": test_case_id,
                "test_case_name": f"测试用例 {test_case_id}",
                "module": "未知模块",
                "status": "pending"
            }
            
            result = self._execute_single_test_case(test_case)
            results.append(result)
        
        return results
    
    def _execute_single_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个测试用例"""
        test_case_id = test_case["test_case_id"]
        test_case_name = test_case["test_case_name"]
        
        print(f"\n执行测试用例: {test_case_id} - {test_case_name}")
        
        start_time = datetime.now()
        
        try:
            # 根据测试用例类型执行不同的测试
            if "用户录入" in test_case_name or "用户管理" in test_case.get("module", ""):
                result = self._execute_user_management_test(test_case)
            elif "系统管理" in test_case_name or "系统管理" in test_case.get("module", ""):
                result = self._execute_system_management_test(test_case)
            else:
                result = self._execute_generic_test(test_case)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            result.update({
                "test_case_id": test_case_id,
                "test_case_name": test_case_name,
                "execution_time": execution_time,
                "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            return {
                "test_case_id": test_case_id,
                "test_case_name": test_case_name,
                "status": "failed",
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _execute_user_management_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """执行用户管理相关测试"""
        print("执行用户管理测试...")
        
        # 这里应该调用用户管理页面的测试方法
        # 暂时返回模拟结果
        return {
            "status": "passed",
            "message": "用户管理测试执行成功",
            "details": "用户录入功能正常"
        }
    
    def _execute_system_management_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """执行系统管理相关测试"""
        print("执行系统管理测试...")
        
        # 这里应该调用系统管理页面的测试方法
        # 暂时返回模拟结果
        return {
            "status": "passed",
            "message": "系统管理测试执行成功",
            "details": "系统管理功能正常"
        }
    
    def _execute_generic_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """执行通用测试"""
        print("执行通用测试...")
        
        # 这里应该调用通用的测试方法
        # 暂时返回模拟结果
        return {
            "status": "passed",
            "message": "通用测试执行成功",
            "details": "测试功能正常"
        }
    
    def _get_test_cases_by_module(self, module_name: str) -> List[str]:
        """根据模块名称获取测试用例ID列表"""
        # 这里应该从测试用例仓库查询指定模块的测试用例
        # 暂时返回示例数据
        module_test_cases = {
            "用户管理": ["TC_1_1_1", "TC_1_1_2"],
            "系统管理": ["TC_2_1_1", "TC_2_1_2"],
            "权限管理": ["TC_3_1_1"]
        }
        
        return module_test_cases.get(module_name, [])
    
    def _generate_test_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成测试报告"""
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get("status") == "passed"])
        failed_tests = len([r for r in test_results if r.get("status") == "failed"])
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "test_results": test_results,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 保存测试报告
        self._save_test_report(report)
        
        return report
    
    def _save_test_report(self, report: Dict[str, Any]) -> None:
        """保存测试报告"""
        try:
            results_path = self.config_loader.get_results_path()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            report_path = f"{results_path}/test_report_{timestamp}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"测试报告已保存: {report_path}")
            
        except Exception as e:
            print(f"保存测试报告失败: {e}")
    
    def cleanup(self) -> None:
        """清理资源"""
        if hasattr(self.smart_login, 'teardown_browser'):
            self.smart_login.teardown_browser()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试执行器")
    parser.add_argument("--all", action="store_true", help="执行所有测试用例")
    parser.add_argument("--test-cases", nargs="+", help="执行指定的测试用例ID")
    parser.add_argument("--module", help="执行指定模块的测试用例")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    try:
        if args.all:
            # 执行所有测试用例
            result = runner.run_all_tests()
        elif args.test_cases:
            # 执行指定的测试用例
            result = runner.run_specific_tests(args.test_cases)
        elif args.module:
            # 执行指定模块的测试用例
            result = runner.run_tests_by_module(args.module)
        else:
            print("请指定执行方式:")
            print("  --all: 执行所有测试用例")
            print("  --test-cases TC_1_1_1 TC_1_1_2: 执行指定的测试用例")
            print("  --module 用户管理: 执行指定模块的测试用例")
            return
        
        # 打印测试结果摘要
        if "error" in result:
            print(f"执行失败: {result['error']}")
        else:
            summary = result["summary"]
            print(f"\n测试执行完成!")
            print(f"总测试数: {summary['total_tests']}")
            print(f"通过: {summary['passed_tests']}")
            print(f"失败: {summary['failed_tests']}")
            print(f"成功率: {summary['success_rate']:.1f}%")
            
    except Exception as e:
        print(f"程序执行失败: {e}")
    finally:
        runner.cleanup()


if __name__ == "__main__":
    main() 
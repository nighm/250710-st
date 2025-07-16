"""
测试用例仓储
负责测试用例数据的读取、存储和管理
"""
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from ..domain.test_case import TestCase


class TestCaseRepository:
    """测试用例仓储类"""
    
    def __init__(self, data_path: str = "data/cases/json"):
        """
        初始化测试用例仓储
        
        Args:
            data_path: 测试数据目录路径
        """
        self.data_path = Path(data_path)
        self._test_cases = {}
    
    def load_test_case(self, file_path: str) -> Optional[TestCase]:
        """
        加载单个测试用例
        
        Args:
            file_path: 测试用例文件路径
            
        Returns:
            测试用例实例，如果加载失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            test_case = TestCase.from_dict(data)
            self._test_cases[test_case.test_case_id] = test_case
            return test_case
            
        except Exception as e:
            print(f"加载测试用例失败 {file_path}: {e}")
            return None
    
    def load_all_test_cases(self) -> List[TestCase]:
        """
        加载所有测试用例
        
        Returns:
            测试用例列表
        """
        if not self.data_path.exists():
            print(f"测试数据目录不存在: {self.data_path}")
            return []
        
        test_cases = []
        json_files = list(self.data_path.glob("*.json"))
        
        for file_path in json_files:
            test_case = self.load_test_case(str(file_path))
            if test_case:
                test_cases.append(test_case)
        
        return test_cases
    
    def load_automated_test_cases(self) -> List[TestCase]:
        """
        加载可自动化的测试用例
        
        Returns:
            可自动化测试用例列表
        """
        all_test_cases = self.load_all_test_cases()
        return [tc for tc in all_test_cases if tc.is_automated()]
    
    def get_test_case_by_id(self, test_case_id: str) -> Optional[TestCase]:
        """
        根据ID获取测试用例
        
        Args:
            test_case_id: 测试用例ID
            
        Returns:
            测试用例实例
        """
        return self._test_cases.get(test_case_id)
    
    def get_test_cases_by_function(self, function_name: str) -> List[TestCase]:
        """
        根据功能名称获取测试用例
        
        Args:
            function_name: 功能名称
            
        Returns:
            测试用例列表
        """
        return [
            tc for tc in self._test_cases.values()
            if tc.corresponding_function == function_name
        ]
    
    def get_test_cases_by_sub_function(self, sub_function: str) -> List[TestCase]:
        """
        根据子功能名称获取测试用例
        
        Args:
            sub_function: 子功能名称
            
        Returns:
            测试用例列表
        """
        return [
            tc for tc in self._test_cases.values()
            if (tc.corresponding_sub_function1 == sub_function or
                tc.corresponding_sub_function2 == sub_function or
                tc.corresponding_sub_function3 == sub_function)
        ]
    
    def save_test_case(self, test_case: TestCase, file_path: Optional[str] = None) -> bool:
        """
        保存测试用例到文件
        
        Args:
            test_case: 测试用例实例
            file_path: 保存路径，如果为None则自动生成
            
        Returns:
            保存是否成功
        """
        try:
            if file_path is None:
                # 根据测试用例ID生成文件名
                filename = f"{test_case.test_case_id}-{test_case.test_case_name}.json"
                file_path = self.data_path / filename
            
            # 确保目录存在
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(test_case.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存测试用例失败: {e}")
            return False
    
    def update_test_result(self, test_case_id: str, result: str, executor: str = "") -> bool:
        """
        更新测试结果
        
        Args:
            test_case_id: 测试用例ID
            result: 测试结果
            executor: 执行人
            
        Returns:
            更新是否成功
        """
        test_case = self.get_test_case_by_id(test_case_id)
        if not test_case:
            return False
        
        test_case.test_result = result
        test_case.recent_executor = executor
        
        # 查找对应的文件路径
        json_files = list(self.data_path.glob("*.json"))
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("测试用例编号") == test_case_id:
                        data["测试结果"] = result
                        data["最近执行人"] = executor
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        return True
            except Exception as e:
                print(f"更新测试结果失败 {file_path}: {e}")
        
        return False
    
    def get_test_case_statistics(self) -> Dict[str, Any]:
        """
        获取测试用例统计信息
        
        Returns:
            统计信息字典
        """
        all_test_cases = self.load_all_test_cases()
        automated_test_cases = [tc for tc in all_test_cases if tc.is_automated()]
        
        return {
            "total_count": len(all_test_cases),
            "automated_count": len(automated_test_cases),
            "automation_rate": len(automated_test_cases) / len(all_test_cases) if all_test_cases else 0,
            "by_function": self._group_by_function(all_test_cases),
            "by_importance": self._group_by_importance(all_test_cases)
        }
    
    def _group_by_function(self, test_cases: List[TestCase]) -> Dict[str, int]:
        """按功能分组统计"""
        groups = {}
        for tc in test_cases:
            function = tc.corresponding_function
            groups[function] = groups.get(function, 0) + 1
        return groups
    
    def _group_by_importance(self, test_cases: List[TestCase]) -> Dict[str, int]:
        """按重要级别分组统计"""
        groups = {}
        for tc in test_cases:
            importance = str(tc.importance_level)  # 转换为字符串避免比较错误
            groups[importance] = groups.get(importance, 0) + 1
        return groups 
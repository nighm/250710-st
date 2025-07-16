"""
测试用例领域实体
负责封装测试用例的核心业务逻辑和数据
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class TestCase:
    """测试用例领域实体"""
    
    # 基础信息
    requirement_id: str
    requirement_description: str
    sub_function1: str
    sub_function2: str
    sub_function3: str
    
    # 对应功能
    corresponding_function: str
    corresponding_sub_function1: str
    corresponding_sub_function2: str
    corresponding_sub_function3: str
    
    # 测试用例信息
    test_case_id: str
    test_case_name: str
    preconditions: str
    steps: str
    expected_output: str
    
    # 测试属性
    importance_level: int
    test_type: str
    applicable_stage: str
    test_result: str
    recent_executor: str
    remarks: str
    created_time: str
    can_automate: bool
    
    def __post_init__(self):
        """初始化后验证数据完整性"""
        if not self.test_case_id:
            raise ValueError("测试用例编号不能为空")
        if not self.test_case_name:
            raise ValueError("测试用例名称不能为空")
    
    def is_automated(self) -> bool:
        """判断是否可自动化"""
        return self.can_automate
    
    def get_steps_list(self) -> List[str]:
        """获取操作步骤列表"""
        return [step.strip() for step in self.steps.split('\n') if step.strip()]
    
    def get_preconditions_list(self) -> List[str]:
        """获取预置条件列表"""
        return [condition.strip() for condition in self.preconditions.split('\n') if condition.strip()]
    
    def validate_test_data(self) -> bool:
        """验证测试数据完整性"""
        required_fields = [
            self.test_case_id, self.test_case_name, 
            self.steps, self.expected_output
        ]
        return all(field for field in required_fields)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "需求编号": self.requirement_id,
            "需求描述": self.requirement_description,
            "子功能1": self.sub_function1,
            "子功能2": self.sub_function2,
            "子功能3": self.sub_function3,
            "对应功能项": self.corresponding_function,
            "对应子功能1": self.corresponding_sub_function1,
            "对应子功能2": self.corresponding_sub_function2,
            "对应子功能3": self.corresponding_sub_function3,
            "测试用例编号": self.test_case_id,
            "测试用例名称": self.test_case_name,
            "预置条件": self.preconditions,
            "操作步骤": self.steps,
            "预期输出": self.expected_output,
            "重要级别": self.importance_level,
            "测试类型": self.test_type,
            "适用阶段": self.applicable_stage,
            "测试结果": self.test_result,
            "最近执行人": self.recent_executor,
            "备注": self.remarks,
            "创建时间": self.created_time,
            "can_automate": self.can_automate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """从字典创建测试用例实例"""
        return cls(
            requirement_id=data.get("需求编号", ""),
            requirement_description=data.get("需求描述", ""),
            sub_function1=data.get("子功能1", ""),
            sub_function2=data.get("子功能2", ""),
            sub_function3=data.get("子功能3", ""),
            corresponding_function=data.get("对应功能项", ""),
            corresponding_sub_function1=data.get("对应子功能1", ""),
            corresponding_sub_function2=data.get("对应子功能2", ""),
            corresponding_sub_function3=data.get("对应子功能3", ""),
            test_case_id=data.get("测试用例编号", ""),
            test_case_name=data.get("测试用例名称", ""),
            preconditions=data.get("预置条件", ""),
            steps=data.get("操作步骤", ""),
            expected_output=data.get("预期输出", ""),
            importance_level=data.get("重要级别", 1),
            test_type=data.get("测试类型", ""),
            applicable_stage=data.get("适用阶段", ""),
            test_result=data.get("测试结果", ""),
            recent_executor=data.get("最近执行人", ""),
            remarks=data.get("备注", ""),
            created_time=data.get("创建时间", ""),
            can_automate=data.get("can_automate", False)
        ) 
"""
配置加载器
负责加载和管理项目配置文件
"""
import yaml
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """配置加载器类"""
    
    def __init__(self, config_dir: str = "config"):
        """
        初始化配置加载器
        
        Args:
            config_dir: 配置文件目录路径
        """
        self.config_dir = Path(config_dir)
        self._settings = None
        self._test_config = None
    
    def load_settings(self) -> Dict[str, Any]:
        """
        加载主配置文件
        
        Returns:
            配置字典
        """
        if self._settings is None:
            settings_file = self.config_dir / "settings.yaml"
            if not settings_file.exists():
                raise FileNotFoundError(f"配置文件不存在: {settings_file}")
            
            with open(settings_file, 'r', encoding='utf-8') as f:
                self._settings = yaml.safe_load(f)
        
        return self._settings
    
    def get_web_config(self) -> Dict[str, Any]:
        """
        获取Web自动化配置
        
        Returns:
            Web配置字典
        """
        settings = self.load_settings()
        return {
            "base_url": settings.get("url", ""),
            "username": settings.get("username", ""),
            "password": settings.get("password", ""),
            "timeout": settings.get("timeout", 30),
            "headless": settings.get("headless", True),
            "slow_mo": settings.get("slow_mo", 1000)
        }
    
    def get_test_data_path(self) -> str:
        """
        获取测试数据路径
        
        Returns:
            测试数据目录路径
        """
        return str(Path("data/cases/json"))
    
    def get_results_path(self) -> str:
        """
        获取测试结果保存路径
        
        Returns:
            结果目录路径
        """
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        return str(results_dir)
    
    def validate_config(self) -> bool:
        """
        验证配置完整性
        
        Returns:
            配置是否有效
        """
        try:
            settings = self.load_settings()
            required_fields = ["url", "username", "password"]
            
            for field in required_fields:
                if not settings.get(field):
                    print(f"配置缺失: {field}")
                    return False
            
            return True
        except Exception as e:
            print(f"配置验证失败: {e}")
            return False
    
    def create_default_config(self) -> None:
        """
        创建默认配置文件
        """
        default_config = {
            "url": "http://192.168.24.100",
            "username": "your_username",
            "password": "your_password",
            "timeout": 30,
            "headless": True,
            "slow_mo": 1000
        }
        
        config_file = self.config_dir / "settings.yaml"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"默认配置文件已创建: {config_file}")
    
    def get_test_case_files(self) -> list:
        """
        获取所有测试用例JSON文件
        
        Returns:
            测试用例文件路径列表
        """
        test_data_path = Path(self.get_test_data_path())
        if not test_data_path.exists():
            return []
        
        json_files = list(test_data_path.glob("*.json"))
        return [str(f) for f in json_files]
    
    def get_automated_test_cases(self) -> list:
        """
        获取可自动化的测试用例文件
        
        Returns:
            可自动化测试用例文件路径列表
        """
        test_files = self.get_test_case_files()
        automated_files = []
        
        for file_path in test_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("can_automate", False):
                        automated_files.append(file_path)
            except Exception as e:
                print(f"读取文件失败 {file_path}: {e}")
        
        return automated_files 
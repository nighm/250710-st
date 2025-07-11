#!/usr/bin/env python3
"""
用户录入测试用例自动化执行脚本
专门针对 TC_1_1_1 测试用例的自动化实现

基于JSON测试用例数据，实现完整的Web自动化测试流程
"""
import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright, expect
from src.infrastructure.config_loader import ConfigLoader
from src.infrastructure.test_case_repository import TestCaseRepository
from src.web.login_page import LoginPage
from src.web.user_management_page import UserManagementPage


class UserInputTestRunner:
    """用户录入测试执行器"""
    
    def __init__(self):
        """初始化测试执行器"""
        self.config_loader = ConfigLoader()
        self.test_repository = TestCaseRepository()
        self.playwright = None
        self.browser = None
        self.page = None
        self.login_page = None
        self.user_management_page = None
        
        # 测试结果
        self.test_result = {
            "test_case_id": "TC_1_1_1",
            "test_case_name": "在用户录入界面，用户账号输入长度范围内的合法字符，其他参数填写正确，点击提交，录入用户成功",
            "start_time": "",
            "end_time": "",
            "status": "FAILED",
            "error_message": "",
            "screenshot_path": "",
            "execution_time": 0,
            "steps_executed": [],
            "verification_results": []
        }
    
    def setup_browser(self, headless: bool = False):
        """
        设置浏览器环境
        
        Args:
            headless: 是否无头模式，默认False便于观察
        """
        print("🔧 正在启动浏览器...")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            slow_mo=1000  # 慢动作，便于观察
        )
        # 跳过证书校验
        self.page = self.browser.new_page(ignore_https_errors=True)
        
        # 设置视窗大小
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 初始化页面对象
        self.login_page = LoginPage(self.page)
        self.user_management_page = UserManagementPage(self.page)
        
        print("✅ 浏览器启动完成")
    
    def teardown_browser(self):
        """清理浏览器环境"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("🧹 浏览器环境已清理")
    
    def load_test_case(self) -> dict:
        """
        加载测试用例数据
        
        Returns:
            测试用例数据字典
        """
        test_case_file = "data/cases/json/1-TC_1_1_1-系统管理_用户管理_用户录入.json"
        
        try:
            with open(test_case_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            
            print(f"📋 已加载测试用例: {test_data['测试用例名称']}")
            return test_data
            
        except Exception as e:
            print(f"❌ 加载测试用例失败: {e}")
            return {}
    
    def login_to_system(self) -> bool:
        """
        登录系统
        
        Returns:
            登录是否成功
        """
        try:
            web_config = self.config_loader.get_web_config()
            base_url = web_config["base_url"]
            username = web_config["username"]
            password = web_config["password"]
            
            print(f"🔐 正在登录系统: {base_url}")
            print(f"👤 用户名: {username}")
            
            # 导航到登录页面
            self.login_page.navigate_to_login(base_url)
            
            # 执行登录
            self.login_page.login(username, password)
            
            # 检查登录结果
            if self.login_page.is_login_successful():
                print("✅ 登录成功")
                return True
            else:
                error_msg = self.login_page.get_error_message()
                print(f"❌ 登录失败: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 登录过程发生错误: {e}")
            return False
    
    def execute_test_steps(self, test_data: dict):
        """
        执行测试步骤
        
        Args:
            test_data: 测试用例数据
        """
        steps = test_data.get("操作步骤", "").split('\n')
        
        print("\n📝 开始执行测试步骤:")
        print("=" * 50)
        
        for i, step in enumerate(steps, 1):
            step = step.strip()
            if not step:
                continue
                
            print(f"\n步骤 {i}: {step}")
            self.test_result["steps_executed"].append({
                "step_number": i,
                "step_description": step,
                "status": "PENDING"
            })
            
            try:
                if "进入 系统管理-用户管理 页面" in step:
                    self._execute_step_1_navigate_to_user_management()
                    
                elif "点击 用户录入" in step:
                    self._execute_step_2_click_user_input()
                    
                elif "用户账号" in step and "输入长度范围内的合法字符" in step:
                    self._execute_step_3_fill_user_account()
                    
                elif "其他参数填写正确" in step:
                    self._execute_step_4_fill_other_parameters()
                    
                elif "点击提交" in step:
                    self._execute_step_5_submit_form()
                    
                else:
                    print(f"⚠️  未知步骤: {step}")
                    self.test_result["steps_executed"][-1]["status"] = "SKIPPED"
                    continue
                
                self.test_result["steps_executed"][-1]["status"] = "PASSED"
                print(f"✅ 步骤 {i} 执行成功")
                
            except Exception as e:
                error_msg = f"步骤 {i} 执行失败: {e}"
                print(f"❌ {error_msg}")
                self.test_result["steps_executed"][-1]["status"] = "FAILED"
                self.test_result["steps_executed"][-1]["error"] = str(e)
                raise Exception(error_msg)
    
    def _execute_step_1_navigate_to_user_management(self):
        """执行步骤1: 进入系统管理-用户管理页面"""
        print("  🎯 导航到用户管理页面")
        self.user_management_page.navigate_to_user_management()
        time.sleep(2)  # 等待页面加载
    
    def _execute_step_2_click_user_input(self):
        """执行步骤2: 点击用户录入"""
        print("  🎯 点击用户录入按钮")
        self.user_management_page.click_user_input()
        self.user_management_page.wait_for_form_loaded()
        time.sleep(1)
    
    def _execute_step_3_fill_user_account(self):
        """执行步骤3: 填写用户账号"""
        print("  🎯 填写用户账号")
        
        # 生成合法的用户账号 (3-20位字母数字组合)
        import random
        import string
        length = random.randint(3, 20)
        chars = string.ascii_letters + string.digits
        valid_account = ''.join(random.choice(chars) for _ in range(length))
        
        print(f"  📝 生成的用户账号: {valid_account}")
        self.user_management_page.fill_user_account(valid_account)
        
        # 验证账号长度
        if self.user_management_page.validate_user_account_length(valid_account):
            print(f"  ✅ 用户账号长度验证通过: {len(valid_account)} 位")
        else:
            raise Exception("用户账号长度验证失败")
    
    def _execute_step_4_fill_other_parameters(self):
        """执行步骤4: 填写其他参数"""
        print("  🎯 填写其他用户参数")
        
        # 填写用户名称
        import random
        import string
        length = random.randint(2, 50)
        chars = string.ascii_letters + string.digits + "测试用户"
        valid_name = ''.join(random.choice(chars) for _ in range(length))
        
        print(f"  📝 用户名称: {valid_name}")
        self.user_management_page.fill_user_name(valid_name)
        
        # 填写邮箱
        email = "test@example.com"
        print(f"  📝 用户邮箱: {email}")
        self.user_management_page.fill_user_email(email)
        
        # 填写电话
        phone = "13800138000"
        print(f"  📝 用户电话: {phone}")
        self.user_management_page.fill_user_phone(phone)
        
        # 选择角色
        role = "普通用户"
        print(f"  📝 用户角色: {role}")
        self.user_management_page.select_user_role(role)
        
        # 选择状态
        status = "启用"
        print(f"  📝 用户状态: {status}")
        self.user_management_page.select_user_status(status)
        
        time.sleep(1)
    
    def _execute_step_5_submit_form(self):
        """执行步骤5: 提交表单"""
        print("  🎯 提交用户表单")
        self.user_management_page.submit_user_form()
        time.sleep(2)  # 等待提交完成
    
    def verify_expected_output(self, test_data: dict) -> bool:
        """
        验证预期结果
        
        Args:
            test_data: 测试用例数据
            
        Returns:
            验证是否通过
        """
        expected_output = test_data.get("预期输出", "")
        print(f"\n🔍 验证预期结果: {expected_output}")
        
        verification_result = {
            "expected_output": expected_output,
            "actual_result": "",
            "status": "FAILED"
        }
        
        try:
            if "录入用户成功" in expected_output:
                # 检查是否显示成功消息
                if self.user_management_page.is_submit_successful():
                    success_msg = self.user_management_page.get_success_message()
                    verification_result["actual_result"] = success_msg
                    verification_result["status"] = "PASSED"
                    print(f"✅ 验证通过: {success_msg}")
                    return True
                else:
                    error_msg = self.user_management_page.get_error_message()
                    verification_result["actual_result"] = error_msg
                    print(f"❌ 验证失败: {error_msg}")
                    return False
            
            self.test_result["verification_results"].append(verification_result)
            return False
            
        except Exception as e:
            verification_result["actual_result"] = f"验证过程发生错误: {e}"
            print(f"❌ 验证过程发生错误: {e}")
            self.test_result["verification_results"].append(verification_result)
            return False
    
    def take_screenshot(self):
        """截图"""
        try:
            results_path = self.config_loader.get_results_path()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{results_path}/TC_1_1_1_{timestamp}.png"
            
            self.page.screenshot(path=screenshot_path)
            self.test_result["screenshot_path"] = screenshot_path
            print(f"📸 截图已保存: {screenshot_path}")
            
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            self.test_result["screenshot_path"] = ""
    
    def save_test_result(self):
        """保存测试结果"""
        try:
            results_path = self.config_loader.get_results_path()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = f"{results_path}/TC_1_1_1_result_{timestamp}.json"
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_result, f, ensure_ascii=False, indent=2)
            
            print(f"💾 测试结果已保存: {result_file}")
            
        except Exception as e:
            print(f"❌ 保存测试结果失败: {e}")
    
    def run_test(self):
        """运行测试"""
        print("🚀 开始执行用户录入测试用例")
        print("=" * 80)
        
        # 记录开始时间
        self.test_result["start_time"] = datetime.now().isoformat()
        start_time = time.time()
        
        try:
            # 1. 加载测试用例
            test_data = self.load_test_case()
            if not test_data:
                raise Exception("无法加载测试用例数据")
            
            # 2. 设置浏览器
            self.setup_browser(headless=False)
            
            # 3. 登录系统
            if not self.login_to_system():
                raise Exception("系统登录失败")
            
            # 4. 执行测试步骤
            self.execute_test_steps(test_data)
            
            # 5. 验证预期结果
            if self.verify_expected_output(test_data):
                self.test_result["status"] = "PASSED"
                print("\n🎉 测试用例执行成功！")
            else:
                self.test_result["status"] = "FAILED"
                print("\n❌ 测试用例执行失败！")
            
        except Exception as e:
            self.test_result["status"] = "FAILED"
            self.test_result["error_message"] = str(e)
            print(f"\n💥 测试执行异常: {e}")
            
        finally:
            # 记录结束时间和执行时间
            self.test_result["end_time"] = datetime.now().isoformat()
            self.test_result["execution_time"] = time.time() - start_time
            
            # 截图
            self.take_screenshot()
            
            # 保存结果
            self.save_test_result()
            
            # 清理浏览器
            self.teardown_browser()
            
            # 显示最终结果
            self._display_final_result()
    
    def _display_final_result(self):
        """显示最终结果"""
        print("\n" + "=" * 80)
        print("📊 测试执行结果")
        print("=" * 80)
        
        print(f"测试用例ID: {self.test_result['test_case_id']}")
        print(f"测试用例名称: {self.test_result['test_case_name']}")
        print(f"执行状态: {self.test_result['status']}")
        print(f"开始时间: {self.test_result['start_time']}")
        print(f"结束时间: {self.test_result['end_time']}")
        print(f"执行时间: {self.test_result['execution_time']:.2f} 秒")
        
        if self.test_result['error_message']:
            print(f"错误信息: {self.test_result['error_message']}")
        
        if self.test_result['screenshot_path']:
            print(f"截图路径: {self.test_result['screenshot_path']}")
        
        print(f"\n步骤执行情况:")
        for step in self.test_result['steps_executed']:
            status_icon = "✅" if step['status'] == 'PASSED' else "❌" if step['status'] == 'FAILED' else "⚠️"
            print(f"  {status_icon} 步骤 {step['step_number']}: {step['step_description']}")
        
        status_icon = "🎉" if self.test_result['status'] == 'PASSED' else "💥"
        print(f"\n{status_icon} 测试用例执行完成！")


def main():
    """主函数"""
    print("用户录入测试用例自动化执行脚本")
    print("基于JSON测试用例数据的Web自动化测试")
    print("=" * 80)
    
    # 检查配置文件
    config_loader = ConfigLoader()
    if not config_loader.validate_config():
        print("❌ 配置验证失败，请先运行以下命令初始化配置:")
        print("   python -m src.interfaces.test_cli init-config")
        print("   然后编辑 config/settings.yaml 文件")
        return
    
    # 运行测试
    runner = UserInputTestRunner()
    runner.run_test()


if __name__ == "__main__":
    main() 
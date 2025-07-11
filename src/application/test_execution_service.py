"""
测试执行服务
负责协调测试用例的执行流程
"""
import os
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext

from ..domain.test_case import TestCase
from ..infrastructure.config_loader import ConfigLoader
from ..infrastructure.test_case_repository import TestCaseRepository
from ..web.login_page import LoginPage
from ..web.user_management_page import UserManagementPage
from ..infrastructure.page_objects.base_page import BasePage


class TestExecutionService:
    """测试执行服务类"""
    
    def __init__(self):
        """初始化测试执行服务"""
        self.config_loader = ConfigLoader()
        self.test_repository = TestCaseRepository()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.base_page = None
        self.login_page = None
        self.user_management_page = None
    
    def setup_browser(self, headless: bool = True) -> None:
        """
        设置浏览器环境
        
        Args:
            headless: 是否无头模式
        """
        web_config = self.config_loader.get_web_config()
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--ignore-certificate-errors', '--ignore-ssl-errors']
        )
        self.context = self.browser.new_context(
            ignore_https_errors=True,
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = self.context.new_page()
        
        # 初始化页面对象
        self.base_page = BasePage(self.page)
        self.login_page = LoginPage(self.page)
        self.user_management_page = UserManagementPage(self.page)
    
    def teardown_browser(self) -> None:
        """清理浏览器环境"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def login_to_system(self, username: str, password: str) -> bool:
        """
        登录系统
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            登录是否成功
        """
        try:
            web_config = self.config_loader.get_web_config()
            login_url = web_config["login_url"]
            
            print(f"正在访问登录页面: {login_url}")
            self.page.goto(login_url, wait_until="networkidle")
            
            # 等待页面加载完成
            self.page.wait_for_load_state("networkidle")
            
            # 分析当前页面
            self._analyze_current_page("登录页面")
            
            # 尝试登录
            if self.login_page.login(username, password):
                print("登录成功")
                return True
            else:
                print("登录失败")
                return False
                
        except Exception as e:
            print(f"登录过程中发生错误: {e}")
            return False
    
    def execute_user_input_test(self, test_case: TestCase) -> Dict[str, Any]:
        """
        执行用户录入测试用例
        
        Args:
            test_case: 测试用例实例
            
        Returns:
            测试执行结果
        """
        result = {
            "test_case_id": test_case.test_case_id,
            "test_case_name": test_case.test_case_name,
            "start_time": datetime.now().isoformat(),
            "status": "FAILED",
            "error_message": "",
            "screenshot_path": "",
            "execution_time": 0
        }
        
        start_time = time.time()
        
        try:
            print(f"开始执行测试用例: {test_case.test_case_name}")
            
            # 验证测试数据
            if not test_case.validate_test_data():
                raise ValueError("测试数据不完整")
            
            # 获取测试步骤
            steps = test_case.get_steps_list()
            print(f"测试步骤: {steps}")
            
            # 执行测试步骤
            self._execute_test_steps(steps, test_case)
            
            # 验证预期结果
            expected_output = test_case.expected_output
            if self._verify_expected_output(expected_output):
                result["status"] = "PASSED"
                print("测试用例执行成功")
            else:
                result["error_message"] = f"预期结果验证失败: {expected_output}"
                print(f"测试用例执行失败: {result['error_message']}")
            
        except Exception as e:
            result["error_message"] = str(e)
            print(f"测试用例执行异常: {e}")
        
        finally:
            # 记录执行时间
            result["execution_time"] = time.time() - start_time
            
            # 截图
            screenshot_path = self._take_test_screenshot(test_case.test_case_id)
            result["screenshot_path"] = screenshot_path
            
            # 更新测试结果
            self._update_test_result(test_case.test_case_id, result["status"])
        
        return result
    
    def _execute_test_steps(self, steps: List[str], test_case: TestCase) -> None:
        """
        执行测试步骤
        
        Args:
            steps: 测试步骤列表
            test_case: 测试用例实例
        """
        for i, step in enumerate(steps, 1):
            print(f"执行步骤 {i}: {step}")
            
            if "进入 系统管理-用户管理 页面" in step:
                self.user_management_page.navigate_to_user_management()
                # 分析用户管理页面
                self._analyze_current_page("用户管理页面")
                
            elif "点击 用户录入" in step:
                self.user_management_page.click_user_input()
                self.user_management_page.wait_for_form_loaded()
                # 分析用户录入表单页面
                self._analyze_current_page("用户录入表单页面")
                
            elif "用户账号" in step and "输入长度范围内的合法字符" in step:
                # 生成合法的用户账号
                valid_account = self._generate_valid_user_account()
                self.user_management_page.fill_user_account(valid_account)
                print(f"填写用户账号: {valid_account}")
                
            elif "用户名称" in step and "输入长度范围内的合法字符" in step:
                # 生成合法的用户名称
                valid_name = self._generate_valid_user_name()
                self.user_management_page.fill_user_name(valid_name)
                print(f"填写用户名称: {valid_name}")
                
            elif "其他参数填写正确" in step:
                # 填写其他必要参数
                self._fill_other_user_parameters()
                print("填写其他参数完成")
                
            elif "点击提交" in step:
                self.user_management_page.submit_user_form()
                # 分析提交后的页面
                self._analyze_current_page("提交后页面")
                
            else:
                print(f"未知步骤: {step}")
                # 对未知步骤也进行页面分析
                self._analyze_current_page(f"步骤{i}_未知页面")
    
    def _generate_valid_user_account(self) -> str:
        """
        生成合法的用户账号
        
        Returns:
            合法的用户账号
        """
        import random
        import string
        
        # 生成3-20位的字母数字组合
        length = random.randint(3, 20)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _generate_valid_user_name(self) -> str:
        """
        生成合法的用户名称
        
        Returns:
            合法的用户名称
        """
        import random
        import string
        
        # 生成2-50位的中文、字母、数字组合
        length = random.randint(2, 50)
        chars = string.ascii_letters + string.digits + "测试用户"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _fill_other_user_parameters(self) -> None:
        """填写其他用户参数"""
        # 填写邮箱
        self.user_management_page.fill_user_email("test@example.com")
        
        # 填写电话
        self.user_management_page.fill_user_phone("13800138000")
        
        # 选择角色
        self.user_management_page.select_user_role("普通用户")
        
        # 选择状态
        self.user_management_page.select_user_status("启用")
    
    def _verify_expected_output(self, expected_output: str) -> bool:
        """
        验证预期结果
        
        Args:
            expected_output: 预期输出
            
        Returns:
            验证是否通过
        """
        if "录入用户成功" in expected_output:
            return self.user_management_page.is_submit_successful()
        
        return False
    
    def _take_test_screenshot(self, test_case_id: str) -> str:
        """
        测试截图
        
        Args:
            test_case_id: 测试用例ID
            
        Returns:
            截图文件路径
        """
        results_path = self.config_loader.get_results_path()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{results_path}/{test_case_id}_{timestamp}.png"
        
        try:
            self.page.screenshot(path=screenshot_path)
            print(f"截图已保存: {screenshot_path}")
        except Exception as e:
            print(f"截图失败: {e}")
            screenshot_path = ""
        
        return screenshot_path
    
    def _update_test_result(self, test_case_id: str, result: str) -> None:
        """
        更新测试结果
        
        Args:
            test_case_id: 测试用例ID
            result: 测试结果
        """
        try:
            self.test_repository.update_test_result(test_case_id, result, "自动化测试")
        except Exception as e:
            print(f"更新测试结果失败: {e}")
    
    def execute_specific_test_case(self, test_case_id: str) -> Dict[str, Any]:
        """
        执行指定的测试用例
        
        Args:
            test_case_id: 测试用例ID
            
        Returns:
            执行结果
        """
        # 加载测试用例
        test_case = self.test_repository.get_test_case_by_id(test_case_id)
        if not test_case:
            return {"error": f"测试用例不存在: {test_case_id}"}
        
        # 验证配置
        if not self.config_loader.validate_config():
            return {"error": "配置验证失败"}
        
        # 设置浏览器
        self.setup_browser(headless=False)  # 非无头模式便于观察
        
        try:
            # 登录系统
            web_config = self.config_loader.get_web_config()
            if not self.login_to_system(web_config["username"], web_config["password"]):
                return {"error": "系统登录失败"}
            
            # 执行测试用例
            result = self.execute_user_input_test(test_case)
            return result
            
        finally:
            self.teardown_browser()
    
    def execute_all_automated_tests(self) -> List[Dict[str, Any]]:
        """
        执行所有可自动化的测试用例
        
        Returns:
            执行结果列表
        """
        # 加载可自动化的测试用例
        automated_test_cases = self.test_repository.load_automated_test_cases()
        
        if not automated_test_cases:
            return [{"error": "没有找到可自动化的测试用例"}]
        
        # 验证配置
        if not self.config_loader.validate_config():
            return [{"error": "配置验证失败"}]
        
        # 设置浏览器
        self.setup_browser(headless=True)  # 无头模式提高执行速度
        
        results = []
        
        try:
            # 登录系统
            web_config = self.config_loader.get_web_config()
            if not self.login_to_system(web_config["username"], web_config["password"]):
                return [{"error": "系统登录失败"}]
            
            # 执行所有测试用例
            for test_case in automated_test_cases:
                result = self.execute_user_input_test(test_case)
                results.append(result)
                
                # 短暂等待避免过快执行
                time.sleep(2)
            
        finally:
            self.teardown_browser()
        
        return results
    
    def _analyze_current_page(self, page_name: str) -> Dict[str, Any]:
        """
        分析当前页面
        
        Args:
            page_name: 页面名称
            
        Returns:
            页面分析结果
        """
        analysis_result = {
            "page_name": page_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": self.page.url,
            "title": self.page.title(),
            "screenshot_path": "",
            "html_path": "",
            "elements_analysis": {}
        }
        
        try:
            # 1. 截图
            results_path = self.config_loader.get_results_path()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{results_path}/page_analysis_{page_name}_{timestamp}.png"
            self.page.screenshot(path=screenshot_path)
            analysis_result["screenshot_path"] = screenshot_path
            print(f"页面截图已保存: {screenshot_path}")
            
            # 2. 保存HTML源码
            html_path = f"{results_path}/page_analysis_{page_name}_{timestamp}.html"
            html_content = self.page.content()
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            analysis_result["html_path"] = html_path
            print(f"HTML源码已保存: {html_path}")
            
            # 3. 分析页面元素
            elements_analysis = self._analyze_page_elements()
            analysis_result["elements_analysis"] = elements_analysis
            
            # 4. 保存分析结果
            analysis_json_path = f"{results_path}/page_analysis_{page_name}_{timestamp}.json"
            with open(analysis_json_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            print(f"页面分析结果已保存: {analysis_json_path}")
            
            return analysis_result
            
        except Exception as e:
            print(f"页面分析失败: {e}")
            return analysis_result
    
    def _analyze_page_elements(self) -> Dict[str, Any]:
        """
        分析页面元素
        
        Returns:
            元素分析结果
        """
        elements_analysis = {
            "forms": [],
            "input_fields": [],
            "buttons": [],
            "links": [],
            "tables": [],
            "text_content": []
        }
        
        try:
            # 分析表单
            forms = self.page.query_selector_all("form")
            for i, form in enumerate(forms):
                form_info = {
                    "index": i,
                    "action": form.get_attribute("action") or "",
                    "method": form.get_attribute("method") or "get",
                    "inputs": []
                }
                
                # 分析表单内的输入字段
                inputs = form.query_selector_all("input")
                for j, input_elem in enumerate(inputs):
                    input_info = {
                        "index": j,
                        "type": input_elem.get_attribute("type") or "text",
                        "name": input_elem.get_attribute("name") or "",
                        "id": input_elem.get_attribute("id") or "",
                        "placeholder": input_elem.get_attribute("placeholder") or "",
                        "value": input_elem.get_attribute("value") or ""
                    }
                    form_info["inputs"].append(input_info)
                
                elements_analysis["forms"].append(form_info)
            
            # 分析所有输入字段
            all_inputs = self.page.query_selector_all("input")
            for i, input_elem in enumerate(all_inputs):
                input_info = {
                    "index": i,
                    "type": input_elem.get_attribute("type") or "text",
                    "name": input_elem.get_attribute("name") or "",
                    "id": input_elem.get_attribute("id") or "",
                    "placeholder": input_elem.get_attribute("placeholder") or "",
                    "value": input_elem.get_attribute("value") or "",
                    "visible": input_elem.is_visible(),
                    "enabled": input_elem.is_enabled()
                }
                elements_analysis["input_fields"].append(input_info)
            
            # 分析按钮
            buttons = self.page.query_selector_all("button, input[type='submit'], input[type='button']")
            for i, button in enumerate(buttons):
                button_info = {
                    "index": i,
                    "text": button.inner_text() or button.get_attribute("value") or "",
                    "type": button.get_attribute("type") or "button",
                    "id": button.get_attribute("id") or "",
                    "class": button.get_attribute("class") or "",
                    "visible": button.is_visible(),
                    "enabled": button.is_enabled()
                }
                elements_analysis["buttons"].append(button_info)
            
            # 分析链接
            links = self.page.query_selector_all("a")
            for i, link in enumerate(links):
                link_info = {
                    "index": i,
                    "text": link.inner_text() or "",
                    "href": link.get_attribute("href") or "",
                    "title": link.get_attribute("title") or "",
                    "visible": link.is_visible()
                }
                elements_analysis["links"].append(link_info)
            
            # 分析表格
            tables = self.page.query_selector_all("table")
            for i, table in enumerate(tables):
                table_info = {
                    "index": i,
                    "rows": len(table.query_selector_all("tr")),
                    "headers": []
                }
                
                # 获取表头
                headers = table.query_selector_all("th")
                for header in headers:
                    table_info["headers"].append(header.inner_text() or "")
                
                elements_analysis["tables"].append(table_info)
            
            # 获取页面文本内容
            text_content = self.page.inner_text("body")
            elements_analysis["text_content"] = text_content[:1000] + "..." if len(text_content) > 1000 else text_content
            
        except Exception as e:
            print(f"元素分析失败: {e}")
        
        return elements_analysis 
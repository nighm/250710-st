#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能登录工具
基于页面分析结果，自动填写用户名密码，等待手动输入验证码后自动提交
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright, Page
from src.infrastructure.config_loader import ConfigLoader


class SmartLogin:
    """智能登录器"""
    
    def __init__(self):
        """初始化智能登录器"""
        self.config_loader = ConfigLoader()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.login_elements = {}
    
    def setup_browser(self, headless: bool = False) -> None:
        """设置浏览器"""
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
    
    def teardown_browser(self) -> None:
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def analyze_login_page(self, url: str) -> Dict:
        """
        分析登录页面，识别关键元素
        
        Args:
            url: 登录页面URL
            
        Returns:
            登录元素信息
        """
        print(f"正在分析登录页面: {url}")
        
        try:
            # 访问登录页面
            self.page.goto(url, wait_until="networkidle")
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            # 分析页面元素
            login_elements = self._find_login_elements()
            
            # 保存分析结果
            self._save_analysis_result(login_elements)
            
            return login_elements
            
        except Exception as e:
            print(f"页面分析失败: {e}")
            return {"error": str(e)}
    
    def _find_login_elements(self) -> Dict:
        """查找登录相关元素"""
        elements = {
            "username_input": None,
            "password_input": None,
            "captcha_input": None,
            "login_button": None,
            "error_message": None,
            "success_indicator": None
        }
        
        try:
            # 查找用户名输入框
            username_selectors = [
                "input[placeholder*='账号']",
                "input[placeholder*='用户名']",
                "input[placeholder*='user']",
                "input[name*='username']",
                "input[name*='user']",
                "input[id*='username']",
                "input[id*='user']",
                "input[type='text']"
            ]
            
            for selector in username_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["username_input"] = {
                        "selector": selector,
                        "placeholder": element.get_attribute("placeholder") or "",
                        "name": element.get_attribute("name") or "",
                        "id": element.get_attribute("id") or ""
                    }
                    print(f"找到用户名输入框: {selector}")
                    break
            
            # 查找密码输入框
            password_selectors = [
                "input[type='password']",
                "input[placeholder*='密码']",
                "input[name*='password']",
                "input[name*='pwd']",
                "input[id*='password']",
                "input[id*='pwd']"
            ]
            
            for selector in password_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["password_input"] = {
                        "selector": selector,
                        "placeholder": element.get_attribute("placeholder") or "",
                        "name": element.get_attribute("name") or "",
                        "id": element.get_attribute("id") or ""
                    }
                    print(f"找到密码输入框: {selector}")
                    break
            
            # 查找验证码输入框
            captcha_selectors = [
                "input[placeholder*='验证码']",
                "input[placeholder*='captcha']",
                "input[name*='captcha']",
                "input[name*='code']",
                "input[id*='captcha']",
                "input[id*='code']"
            ]
            
            for selector in captcha_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["captcha_input"] = {
                        "selector": selector,
                        "placeholder": element.get_attribute("placeholder") or "",
                        "name": element.get_attribute("name") or "",
                        "id": element.get_attribute("id") or ""
                    }
                    print(f"找到验证码输入框: {selector}")
                    break
            
            # 查找登录按钮
            button_selectors = [
                "button:has-text('登录')",
                "button:has-text('Login')",
                "input[type='submit']",
                "button[type='submit']",
                "button:has-text('Sign In')",
                "button:has-text('Submit')",
                "button:has-text('登 录')",  # 注意空格
                "button:has-text('登')",
                "button:has-text('录')",
                "input[value*='登录']",
                "input[value*='Login']",
                "button",
                "input[type='button']"
            ]
            
            for selector in button_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["login_button"] = {
                        "selector": selector,
                        "text": element.inner_text() or element.get_attribute("value") or "",
                        "type": element.get_attribute("type") or "button"
                    }
                    print(f"找到登录按钮: {selector}")
                    break
            
            # 查找错误信息元素
            error_selectors = [
                ".error",
                ".error-message",
                ".alert-danger",
                ".alert-error",
                "[class*='error']",
                "[class*='alert']"
            ]
            
            for selector in error_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["error_message"] = {
                        "selector": selector,
                        "text": element.inner_text() or ""
                    }
                    break
            
            # 查找成功指示器
            success_selectors = [
                ".success",
                ".alert-success",
                "[class*='success']"
            ]
            
            for selector in success_selectors:
                element = self.page.query_selector(selector)
                if element and element.is_visible():
                    elements["success_indicator"] = {
                        "selector": selector,
                        "text": element.inner_text() or ""
                    }
                    break
            
        except Exception as e:
            print(f"元素查找失败: {e}")
        
        return elements
    
    def _save_analysis_result(self, elements: Dict) -> None:
        """保存分析结果"""
        try:
            results_path = self.config_loader.get_results_path()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 保存分析结果
            analysis_path = f"{results_path}/login_analysis_{timestamp}.json"
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(elements, f, ensure_ascii=False, indent=2)
            
            print(f"登录页面分析结果已保存: {analysis_path}")
            
        except Exception as e:
            print(f"保存分析结果失败: {e}")
    
    def smart_login(self, username: str, password: str, login_url: str, wait_captcha: bool = True, max_retries: int = 10) -> bool:
        """
        智能登录
        
        Args:
            username: 用户名
            password: 密码
            login_url: 登录页面URL
            wait_captcha: 是否等待验证码输入
            max_retries: 最大重试次数
            
        Returns:
            登录是否成功
        """
        try:
            # 1. 分析登录页面
            print("步骤1: 分析登录页面...")
            login_elements = self.analyze_login_page(login_url)
            
            if "error" in login_elements:
                print(f"页面分析失败: {login_elements['error']}")
                return False
            
            # 2. 自动填写用户名
            if login_elements.get("username_input"):
                print("步骤2: 自动填写用户名...")
                username_selector = login_elements["username_input"]["selector"]
                self.page.fill(username_selector, username)
                print(f"已填写用户名: {username}")
            
            # 3. 自动填写密码
            if login_elements.get("password_input"):
                print("步骤3: 自动填写密码...")
                password_selector = login_elements["password_input"]["selector"]
                self.page.fill(password_selector, password)
                print("已填写密码")
            
            # 4. 循环等待验证码输入并重试登录
            if login_elements.get("captcha_input") and wait_captcha:
                print("步骤4: 循环等待验证码输入并自动重试登录...")
                return self._loop_login_with_captcha(login_elements, max_retries)
            else:
                # 没有验证码，直接登录
                return self._perform_login(login_elements)
            
        except Exception as e:
            print(f"智能登录失败: {e}")
            return False
    
    def _loop_login_with_captcha(self, login_elements: Dict, max_retries: int) -> bool:
        """循环等待验证码输入并重试登录"""
        retry_count = 0
        
        while retry_count < max_retries:
            retry_count += 1
            print(f"\n--- 第 {retry_count} 次尝试登录 ---")
            
            # 等待5秒
            print("等待5秒，请手动输入验证码...")
            time.sleep(5)
            
            # 每次5秒后都重新点击登录按钮
            print("尝试点击登录按钮...")
            self._perform_login_click(login_elements)
            
            # 等待页面跳转或加载
            time.sleep(3)
            
            # 检查登录结果
            login_success = self._check_login_result(login_elements)
            if login_success:
                print("登录成功！")
                return True
            else:
                print(f"登录失败，验证码可能错误，{5}秒后重试...")
                
                # 只有在登录失败时才清空验证码输入框
                if login_elements.get("captcha_input"):
                    captcha_selector = login_elements["captcha_input"]["selector"]
                    try:
                        # 检查是否还在登录页面
                        current_url = self.page.url
                        if "login" in current_url.lower():
                            self.page.fill(captcha_selector, "")
                            print("已清空验证码输入框，请重新输入")
                        else:
                            print("页面已跳转，无需清空验证码输入框")
                    except Exception as e:
                        print(f"清空验证码输入框失败: {e}")
        
        print(f"达到最大重试次数 {max_retries}，登录失败")
        return False
    
    def _perform_login_click(self, login_elements: Dict) -> None:
        """执行登录点击操作（不检查结果）"""
        try:
            if login_elements.get("login_button"):
                button_selector = login_elements["login_button"]["selector"]
                try:
                    self.page.click(button_selector)
                    print("已点击登录按钮")
                except Exception as e:
                    print(f"点击登录按钮失败: {e}")
                    # 尝试其他方式
                    self._try_alternative_login_methods()
            else:
                print("未找到登录按钮，尝试其他登录方式...")
                self._try_alternative_login_methods()
                
        except Exception as e:
            print(f"执行登录点击操作失败: {e}")
    
    def _perform_login(self, login_elements: Dict) -> bool:
        """执行登录操作"""
        try:
            # 尝试点击登录按钮
            print("尝试点击登录按钮...")
            if login_elements.get("login_button"):
                button_selector = login_elements["login_button"]["selector"]
                try:
                    self.page.click(button_selector)
                    print("已点击登录按钮")
                except Exception as e:
                    print(f"点击登录按钮失败: {e}")
                    # 尝试其他方式
                    self._try_alternative_login_methods()
            else:
                print("未找到登录按钮，尝试其他登录方式...")
                self._try_alternative_login_methods()
            
            # 等待页面跳转或加载
            time.sleep(3)
            
            # 检查登录结果
            return self._check_login_result(login_elements)
            
        except Exception as e:
            print(f"执行登录操作失败: {e}")
            return False
    
    def _try_alternative_login_methods(self) -> None:
        """尝试其他登录方式"""
        print("尝试其他登录方式...")
        
        # 方法1: 尝试按回车键
        try:
            self.page.keyboard.press("Enter")
            print("已按回车键")
        except Exception as e:
            print(f"按回车键失败: {e}")
        
        # 方法2: 尝试点击任何按钮
        try:
            buttons = self.page.query_selector_all("button, input[type='submit'], input[type='button']")
            for button in buttons:
                if button.is_visible():
                    button_text = button.inner_text() or button.get_attribute("value") or ""
                    if any(keyword in button_text.lower() for keyword in ['登录', 'login', 'submit', '登', '录']):
                        button.click()
                        print(f"已点击按钮: {button_text}")
                        break
        except Exception as e:
            print(f"点击按钮失败: {e}")
        
        # 方法3: 尝试提交表单
        try:
            forms = self.page.query_selector_all("form")
            for form in forms:
                if form.is_visible():
                    form.evaluate("form => form.submit()")
                    print("已提交表单")
                    break
        except Exception as e:
            print(f"提交表单失败: {e}")
    
    def _check_login_result(self, login_elements: Dict) -> bool:
        """检查登录结果"""
        try:
            current_url = self.page.url
            page_title = self.page.title()
            
            print(f"当前URL: {current_url}")
            print(f"页面标题: {page_title}")
            
            # 检查是否有错误信息
            if login_elements.get("error_message"):
                error_selector = login_elements["error_message"]["selector"]
                error_element = self.page.query_selector(error_selector)
                if error_element and error_element.is_visible():
                    error_text = error_element.inner_text()
                    if error_text:
                        print(f"登录失败: {error_text}")
                        return False
            
            # 检查是否还在登录页面
            if "login" in current_url.lower():
                print("仍在登录页面，登录失败")
                return False
            
            # 检查页面标题是否还是登录相关
            if "登录" in page_title or "login" in page_title.lower():
                print("页面标题仍包含登录信息，登录失败")
                return False
            
            # 检查是否有成功指示器
            if login_elements.get("success_indicator"):
                success_selector = login_elements["success_indicator"]["selector"]
                success_element = self.page.query_selector(success_selector)
                if success_element and success_element.is_visible():
                    print("登录成功！检测到成功指示器")
                    return True
            
            # 如果URL和标题都发生了变化，认为登录成功
            print("登录成功！页面已跳转且标题已变化")
            return True
            
        except Exception as e:
            print(f"检查登录结果失败: {e}")
            return False


def main():
    """主函数"""
    # 从配置文件读取登录信息
    config_loader = ConfigLoader()
    web_config = config_loader.get_web_config()
    
    base_url = web_config.get("base_url", "http://192.168.24.100")
    username = web_config.get("username", "super")
    password = web_config.get("password", "admin123")
    
    # 根据连接测试结果，使用正确的登录URL
    login_url = "https://192.168.24.100/login"
    
    print("智能登录工具")
    print("="*50)
    print(f"登录URL: {login_url}")
    print(f"用户名: {username}")
    print("="*50)
    
    smart_login = SmartLogin()
    
    try:
        smart_login.setup_browser(headless=False)
        
        # 执行智能登录
        success = smart_login.smart_login(username, password, login_url, wait_captcha=True)
        
        if success:
            print("登录成功！")
        else:
            print("登录失败，请检查用户名、密码和验证码")
            
    except Exception as e:
        print(f"程序执行失败: {e}")
    finally:
        # 保持浏览器打开，方便查看结果
        print("浏览器将保持打开状态，请手动关闭")
        input("按回车键关闭浏览器...")


if __name__ == "__main__":
    main() 
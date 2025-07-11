"""
登录页面操作封装
实现登录相关的自动化操作
"""
from .base_page import BasePage
from playwright.sync_api import Page
from typing import Optional


class LoginPage(BasePage):
    """登录页面操作类"""
    
    # 页面元素选择器
    USERNAME_INPUT = "#username"  # 用户名输入框
    PASSWORD_INPUT = "#password"  # 密码输入框
    LOGIN_BUTTON = "#login-btn"   # 登录按钮
    ERROR_MESSAGE = ".error-message"  # 错误信息
    SUCCESS_MESSAGE = ".success-message"  # 成功信息
    
    def __init__(self, page: Page):
        """
        初始化登录页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
    
    def navigate_to_login(self, base_url: str) -> None:
        """
        导航到登录页面
        
        Args:
            base_url: 基础URL
        """
        login_url = f"{base_url}/login"
        self.navigate_to(login_url)
        self.wait_for_element(self.USERNAME_INPUT)
    
    def login(self, username: str, password: str) -> None:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        # 清空并填写用户名
        self.clear_input(self.USERNAME_INPUT)
        self.fill_input(self.USERNAME_INPUT, username)
        
        # 清空并填写密码
        self.clear_input(self.PASSWORD_INPUT)
        self.fill_input(self.PASSWORD_INPUT, password)
        
        # 点击登录按钮
        self.click_element(self.LOGIN_BUTTON)
        
        # 等待页面加载
        self.wait_for_navigation()
    
    def is_login_successful(self) -> bool:
        """
        检查登录是否成功
        
        Returns:
            登录是否成功
        """
        try:
            # 检查是否跳转到主页面（URL变化）
            current_url = self.page.url
            return "/login" not in current_url and "dashboard" in current_url
        except Exception:
            return False
    
    def get_error_message(self) -> str:
        """
        获取错误信息
        
        Returns:
            错误信息文本
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_success_message(self) -> str:
        """
        获取成功信息
        
        Returns:
            成功信息文本
        """
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def wait_for_login_complete(self) -> None:
        """等待登录完成"""
        self.wait_for_navigation()
    
    def logout(self) -> None:
        """执行登出操作"""
        # 点击登出按钮（假设存在）
        logout_button = "#logout-btn"
        if self.is_element_visible(logout_button):
            self.click_element(logout_button)
            self.wait_for_navigation()
    
    def is_logged_in(self) -> bool:
        """
        检查是否已登录
        
        Returns:
            是否已登录
        """
        # 检查是否存在用户信息或登出按钮
        user_info = ".user-info"
        logout_btn = "#logout-btn"
        
        return (self.is_element_visible(user_info) or 
                self.is_element_visible(logout_btn))
    
    def expect_login_success(self) -> None:
        """期望登录成功"""
        self.expect_text_to_be_present("登录成功")
    
    def expect_login_failure(self) -> None:
        """期望登录失败"""
        self.expect_element_to_be_visible(self.ERROR_MESSAGE)
    
    def take_login_screenshot(self, path: str) -> None:
        """
        登录页面截图
        
        Args:
            path: 截图保存路径
        """
        self.take_screenshot(path)

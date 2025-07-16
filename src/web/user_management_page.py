"""
用户管理页面操作封装
实现用户录入相关的自动化操作
"""
from .base_page import BasePage
from playwright.sync_api import Page
from typing import Optional, Dict, Any


class UserManagementPage(BasePage):
    """用户管理页面操作类"""
    
    # 页面元素选择器
    SYSTEM_MANAGEMENT_MENU = "text=系统管理"  # 系统管理菜单
    USER_MANAGEMENT_MENU = "text=用户管理"    # 用户管理菜单
    USER_INPUT_BUTTON = "text=用户录入"       # 用户录入按钮
    
    # 用户录入表单元素
    USER_ACCOUNT_INPUT = "#user-account"      # 用户账号输入框
    USER_NAME_INPUT = "#user-name"            # 用户名称输入框
    USER_EMAIL_INPUT = "#user-email"          # 用户邮箱输入框
    USER_PHONE_INPUT = "#user-phone"          # 用户电话输入框
    USER_ROLE_SELECT = "#user-role"           # 用户角色选择框
    USER_STATUS_SELECT = "#user-status"       # 用户状态选择框
    SUBMIT_BUTTON = "#submit-btn"             # 提交按钮
    CANCEL_BUTTON = "#cancel-btn"             # 取消按钮
    
    # 消息提示元素
    SUCCESS_MESSAGE = ".success-message"      # 成功消息
    ERROR_MESSAGE = ".error-message"          # 错误消息
    VALIDATION_MESSAGE = ".validation-message"  # 验证消息
    
    def __init__(self, page: Page):
        """
        初始化用户管理页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
    
    def navigate_to_user_management(self) -> None:
        """导航到用户管理页面"""
        # 点击系统管理菜单
        self.click_element(self.SYSTEM_MANAGEMENT_MENU)
        self.wait_for_time(1)
        
        # 点击用户管理菜单
        self.click_element(self.USER_MANAGEMENT_MENU)
        self.wait_for_navigation()
    
    def click_user_input(self) -> None:
        """点击用户录入按钮"""
        self.click_element(self.USER_INPUT_BUTTON)
        self.wait_for_navigation()
    
    def fill_user_account(self, account: str) -> None:
        """
        填写用户账号
        
        Args:
            account: 用户账号
        """
        self.clear_input(self.USER_ACCOUNT_INPUT)
        self.fill_input(self.USER_ACCOUNT_INPUT, account)
    
    def fill_user_name(self, name: str) -> None:
        """
        填写用户名称
        
        Args:
            name: 用户名称
        """
        self.clear_input(self.USER_NAME_INPUT)
        self.fill_input(self.USER_NAME_INPUT, name)
    
    def fill_user_email(self, email: str) -> None:
        """
        填写用户邮箱
        
        Args:
            email: 用户邮箱
        """
        self.clear_input(self.USER_EMAIL_INPUT)
        self.fill_input(self.USER_EMAIL_INPUT, email)
    
    def fill_user_phone(self, phone: str) -> None:
        """
        填写用户电话
        
        Args:
            phone: 用户电话
        """
        self.clear_input(self.USER_PHONE_INPUT)
        self.fill_input(self.USER_PHONE_INPUT, phone)
    
    def select_user_role(self, role: str) -> None:
        """
        选择用户角色
        
        Args:
            role: 用户角色
        """
        self.select_option(self.USER_ROLE_SELECT, role)
    
    def select_user_status(self, status: str) -> None:
        """
        选择用户状态
        
        Args:
            status: 用户状态
        """
        self.select_option(self.USER_STATUS_SELECT, status)
    
    def submit_user_form(self) -> None:
        """提交用户表单"""
        self.click_element(self.SUBMIT_BUTTON)
        self.wait_for_navigation()
    
    def cancel_user_form(self) -> None:
        """取消用户表单"""
        self.click_element(self.CANCEL_BUTTON)
        self.wait_for_navigation()
    
    def fill_user_form(self, user_data: Dict[str, Any]) -> None:
        """
        填写完整的用户表单
        
        Args:
            user_data: 用户数据字典
        """
        # 填写用户账号
        if "account" in user_data:
            self.fill_user_account(user_data["account"])
        
        # 填写用户名称
        if "name" in user_data:
            self.fill_user_name(user_data["name"])
        
        # 填写用户邮箱
        if "email" in user_data:
            self.fill_user_email(user_data["email"])
        
        # 填写用户电话
        if "phone" in user_data:
            self.fill_user_phone(user_data["phone"])
        
        # 选择用户角色
        if "role" in user_data:
            self.select_user_role(user_data["role"])
        
        # 选择用户状态
        if "status" in user_data:
            self.select_user_status(user_data["status"])
    
    def is_submit_successful(self) -> bool:
        """
        检查提交是否成功
        
        Returns:
            提交是否成功
        """
        try:
            return self.is_element_visible(self.SUCCESS_MESSAGE)
        except Exception:
            return False
    
    def get_success_message(self) -> str:
        """
        获取成功消息
        
        Returns:
            成功消息文本
        """
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_validation_message(self) -> str:
        """
        获取验证消息
        
        Returns:
            验证消息文本
        """
        if self.is_element_visible(self.VALIDATION_MESSAGE):
            return self.get_text(self.VALIDATION_MESSAGE)
        return ""
    
    def expect_submit_success(self) -> None:
        """期望提交成功"""
        self.expect_element_to_be_visible(self.SUCCESS_MESSAGE)
    
    def expect_submit_failure(self) -> None:
        """期望提交失败"""
        self.expect_element_to_be_visible(self.ERROR_MESSAGE)
    
    def is_form_visible(self) -> bool:
        """
        检查表单是否可见
        
        Returns:
            表单是否可见
        """
        return (self.is_element_visible(self.USER_ACCOUNT_INPUT) and
                self.is_element_visible(self.SUBMIT_BUTTON))
    
    def wait_for_form_loaded(self) -> None:
        """等待表单加载完成"""
        self.wait_for_element(self.USER_ACCOUNT_INPUT)
        self.wait_for_element(self.SUBMIT_BUTTON)
    
    def take_user_form_screenshot(self, path: str) -> None:
        """
        用户表单截图
        
        Args:
            path: 截图保存路径
        """
        self.take_screenshot(path)
    
    def validate_user_account_length(self, account: str, min_length: int = 3, max_length: int = 20) -> bool:
        """
        验证用户账号长度
        
        Args:
            account: 用户账号
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            长度是否合法
        """
        return min_length <= len(account) <= max_length
    
    def validate_user_name_length(self, name: str, min_length: int = 2, max_length: int = 50) -> bool:
        """
        验证用户名称长度
        
        Args:
            name: 用户名称
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            长度是否合法
        """
        return min_length <= len(name) <= max_length 
"""
页面基类
封装通用的Web自动化操作
"""
from playwright.sync_api import Page, expect
from typing import Optional, Any
import time


class BasePage:
    """页面基类，封装通用操作"""
    
    def __init__(self, page: Page):
        """
        初始化页面基类
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.timeout = 30000  # 默认超时时间30秒
    
    def navigate_to(self, url: str) -> None:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
        """
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    def click_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        点击元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        timeout = timeout or self.timeout
        self.page.click(selector, timeout=timeout)
    
    def fill_input(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        填写输入框
        
        Args:
            selector: 元素选择器
            value: 输入值
            timeout: 超时时间
        """
        timeout = timeout or self.timeout
        self.page.fill(selector, value, timeout=timeout)
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        选择下拉框选项
        
        Args:
            selector: 元素选择器
            value: 选项值
            timeout: 超时时间
        """
        timeout = timeout or self.timeout
        self.page.select_option(selector, value, timeout=timeout)
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        等待元素出现
        
        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def wait_for_text(self, text: str, timeout: Optional[int] = None) -> None:
        """
        等待文本出现
        
        Args:
            text: 等待的文本
            timeout: 超时时间
        """
        timeout = timeout or self.timeout
        self.page.wait_for_selector(f"text={text}", timeout=timeout)
    
    def get_text(self, selector: str) -> str:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
            
        Returns:
            元素文本内容
        """
        return self.page.text_content(selector) or ""
    
    def is_element_visible(self, selector: str) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: 元素选择器
            
        Returns:
            元素是否可见
        """
        return self.page.is_visible(selector)
    
    def take_screenshot(self, path: str) -> None:
        """
        截图
        
        Args:
            path: 截图保存路径
        """
        self.page.screenshot(path=path)
    
    def wait_for_navigation(self) -> None:
        """等待页面导航完成"""
        self.page.wait_for_load_state("networkidle")
    
    def press_key(self, key: str) -> None:
        """
        按键操作
        
        Args:
            key: 按键名称
        """
        self.page.keyboard.press(key)
    
    def scroll_to_element(self, selector: str) -> None:
        """
        滚动到元素位置
        
        Args:
            selector: 元素选择器
        """
        self.page.scroll_into_view_if_needed(selector)
    
    def wait_for_time(self, seconds: float) -> None:
        """
        等待指定时间
        
        Args:
            seconds: 等待秒数
        """
        time.sleep(seconds)
    
    def expect_element_to_be_visible(self, selector: str) -> None:
        """
        期望元素可见
        
        Args:
            selector: 元素选择器
        """
        expect(self.page.locator(selector)).to_be_visible()
    
    def expect_text_to_be_present(self, text: str) -> None:
        """
        期望文本存在
        
        Args:
            text: 期望的文本
        """
        expect(self.page.locator(f"text={text}")).to_be_visible()
    
    def expect_element_to_have_text(self, selector: str, text: str) -> None:
        """
        期望元素包含指定文本
        
        Args:
            selector: 元素选择器
            text: 期望的文本
        """
        expect(self.page.locator(selector)).to_have_text(text)
    
    def get_element_count(self, selector: str) -> int:
        """
        获取元素数量
        
        Args:
            selector: 元素选择器
            
        Returns:
            元素数量
        """
        return len(self.page.query_selector_all(selector))
    
    def clear_input(self, selector: str) -> None:
        """
        清空输入框
        
        Args:
            selector: 元素选择器
        """
        self.page.fill(selector, "")
    
    def double_click(self, selector: str) -> None:
        """
        双击元素
        
        Args:
            selector: 元素选择器
        """
        self.page.dblclick(selector)
    
    def right_click(self, selector: str) -> None:
        """
        右键点击元素
        
        Args:
            selector: 元素选择器
        """
        self.page.click(selector, button="right")

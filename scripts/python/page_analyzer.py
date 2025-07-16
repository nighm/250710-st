#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页面分析工具
用于分析网页结构、元素和内容，帮助理解页面布局和定位元素
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright
from src.infrastructure.config_loader import ConfigLoader


class PageAnalyzer:
    """页面分析器"""
    
    def __init__(self):
        """初始化页面分析器"""
        self.config_loader = ConfigLoader()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
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
    
    def analyze_page(self, url: str, page_name: str = "页面分析") -> Dict:
        """
        分析指定页面
        
        Args:
            url: 页面URL
            page_name: 页面名称
            
        Returns:
            分析结果
        """
        print(f"开始分析页面: {url}")
        
        try:
            # 访问页面
            self.page.goto(url, wait_until="networkidle")
            self.page.wait_for_load_state("networkidle")
            
            # 等待页面完全加载
            time.sleep(3)
            
            # 执行分析
            analysis_result = self._perform_page_analysis(page_name)
            
            return analysis_result
            
        except Exception as e:
            print(f"页面分析失败: {e}")
            return {"error": str(e)}
    
    def _perform_page_analysis(self, page_name: str) -> Dict:
        """
        执行页面分析
        
        Args:
            page_name: 页面名称
            
        Returns:
            分析结果
        """
        analysis_result = {
            "page_name": page_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": self.page.url,
            "title": self.page.title(),
            "screenshot_path": "",
            "html_path": "",
            "elements_analysis": {},
            "page_info": {}
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
            
            # 3. 分析页面基本信息
            page_info = self._analyze_page_info()
            analysis_result["page_info"] = page_info
            
            # 4. 分析页面元素
            elements_analysis = self._analyze_page_elements()
            analysis_result["elements_analysis"] = elements_analysis
            
            # 5. 保存分析结果
            analysis_json_path = f"{results_path}/page_analysis_{page_name}_{timestamp}.json"
            with open(analysis_json_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            print(f"页面分析结果已保存: {analysis_json_path}")
            
            # 6. 打印分析摘要
            self._print_analysis_summary(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            print(f"页面分析失败: {e}")
            return analysis_result
    
    def _analyze_page_info(self) -> Dict:
        """分析页面基本信息"""
        page_info = {
            "url": self.page.url,
            "title": self.page.title(),
            "viewport_size": self.page.viewport_size,
        }
        try:
            # cookies 计数
            cookies = self.page.context.cookies()
            page_info["cookies_count"] = len(cookies) if isinstance(cookies, list) else 0
        except Exception as e:
            page_info["cookies_count"] = f"获取失败: {e}"
        try:
            local_storage_count = self.page.evaluate("() => Object.keys(localStorage).length")
            page_info["local_storage_count"] = int(local_storage_count) if isinstance(local_storage_count, (int, float, str)) else 0
        except Exception as e:
            page_info["local_storage_count"] = f"获取失败: {e}"
        try:
            session_storage_count = self.page.evaluate("() => Object.keys(sessionStorage).length")
            page_info["session_storage_count"] = int(session_storage_count) if isinstance(session_storage_count, (int, float, str)) else 0
        except Exception as e:
            page_info["session_storage_count"] = f"获取失败: {e}"
        # 获取页面元信息
        try:
            meta_tags = self.page.query_selector_all("meta")
            page_info["meta_tags"] = []
            for meta in meta_tags:
                meta_info = {
                    "name": meta.get_attribute("name") or "",
                    "content": meta.get_attribute("content") or "",
                    "property": meta.get_attribute("property") or ""
                }
                page_info["meta_tags"].append(meta_info)
        except Exception as e:
            page_info["meta_tags"] = f"获取失败: {e}"
        return page_info
    
    def _analyze_page_elements(self) -> Dict:
        """分析页面元素"""
        elements_analysis = {
            "forms": [],
            "input_fields": [],
            "buttons": [],
            "links": [],
            "tables": [],
            "images": [],
            "text_content": "",
            "selectors_suggestions": []
        }
        
        try:
            # 分析表单
            forms = self.page.query_selector_all("form")
            for i, form in enumerate(forms):
                form_info = {
                    "index": i,
                    "action": form.get_attribute("action") or "",
                    "method": form.get_attribute("method") or "get",
                    "id": form.get_attribute("id") or "",
                    "class": form.get_attribute("class") or "",
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
                        "value": input_elem.get_attribute("value") or "",
                        "class": input_elem.get_attribute("class") or "",
                        "visible": input_elem.is_visible(),
                        "enabled": input_elem.is_enabled()
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
                    "class": input_elem.get_attribute("class") or "",
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
                    "id": link.get_attribute("id") or "",
                    "class": link.get_attribute("class") or "",
                    "visible": link.is_visible()
                }
                elements_analysis["links"].append(link_info)
            
            # 分析表格
            tables = self.page.query_selector_all("table")
            for i, table in enumerate(tables):
                table_info = {
                    "index": i,
                    "rows": len(table.query_selector_all("tr")),
                    "headers": [],
                    "id": table.get_attribute("id") or "",
                    "class": table.get_attribute("class") or ""
                }
                
                # 获取表头
                headers = table.query_selector_all("th")
                for header in headers:
                    table_info["headers"].append(header.inner_text() or "")
                
                elements_analysis["tables"].append(table_info)
            
            # 分析图片
            images = self.page.query_selector_all("img")
            for i, img in enumerate(images):
                img_info = {
                    "index": i,
                    "src": img.get_attribute("src") or "",
                    "alt": img.get_attribute("alt") or "",
                    "title": img.get_attribute("title") or "",
                    "id": img.get_attribute("id") or "",
                    "class": img.get_attribute("class") or "",
                    "visible": img.is_visible()
                }
                elements_analysis["images"].append(img_info)
            
            # 获取页面文本内容
            text_content = self.page.inner_text("body")
            elements_analysis["text_content"] = text_content[:2000] + "..." if len(text_content) > 2000 else text_content
            
            # 生成选择器建议
            elements_analysis["selectors_suggestions"] = self._generate_selector_suggestions()
            
        except Exception as e:
            print(f"元素分析失败: {e}")
        
        return elements_analysis
    
    def _generate_selector_suggestions(self) -> List[Dict]:
        """生成选择器建议"""
        suggestions = []
        
        try:
            # 用户名输入框建议
            username_inputs = self.page.query_selector_all("input[type='text'], input[name*='user'], input[name*='username'], input[id*='user'], input[id*='username']")
            for i, input_elem in enumerate(username_inputs):
                suggestions.append({
                    "element_type": "用户名输入框",
                    "index": i,
                    "selectors": [
                        f"input[name='{input_elem.get_attribute('name')}']" if input_elem.get_attribute('name') else None,
                        f"input[id='{input_elem.get_attribute('id')}']" if input_elem.get_attribute('id') else None,
                        f"input[placeholder='{input_elem.get_attribute('placeholder')}']" if input_elem.get_attribute('placeholder') else None
                    ],
                    "text": input_elem.get_attribute('placeholder') or input_elem.get_attribute('name') or ""
                })
            
            # 密码输入框建议
            password_inputs = self.page.query_selector_all("input[type='password']")
            for i, input_elem in enumerate(password_inputs):
                suggestions.append({
                    "element_type": "密码输入框",
                    "index": i,
                    "selectors": [
                        f"input[name='{input_elem.get_attribute('name')}']" if input_elem.get_attribute('name') else None,
                        f"input[id='{input_elem.get_attribute('id')}']" if input_elem.get_attribute('id') else None
                    ],
                    "text": input_elem.get_attribute('placeholder') or input_elem.get_attribute('name') or ""
                })
            
            # 登录按钮建议
            login_buttons = self.page.query_selector_all("button, input[type='submit']")
            for i, button in enumerate(login_buttons):
                button_text = button.inner_text() or button.get_attribute('value') or ""
                if any(keyword in button_text.lower() for keyword in ['登录', 'login', 'sign in', 'submit']):
                    suggestions.append({
                        "element_type": "登录按钮",
                        "index": i,
                        "selectors": [
                            f"button:has-text('{button_text}')" if button_text else None,
                            f"input[value='{button_text}']" if button_text else None,
                            f"button[id='{button.get_attribute('id')}']" if button.get_attribute('id') else None
                        ],
                        "text": button_text
                    })
            
        except Exception as e:
            print(f"生成选择器建议失败: {e}")
        
        return suggestions
    
    def _print_analysis_summary(self, analysis_result: Dict) -> None:
        """打印分析摘要"""
        print("\n" + "="*50)
        print("页面分析摘要")
        print("="*50)
        print(f"页面标题: {analysis_result.get('title', 'N/A')}")
        print(f"页面URL: {analysis_result.get('url', 'N/A')}")
        
        elements = analysis_result.get('elements_analysis', {})
        print(f"表单数量: {len(elements.get('forms', []))}")
        print(f"输入字段数量: {len(elements.get('input_fields', []))}")
        print(f"按钮数量: {len(elements.get('buttons', []))}")
        print(f"链接数量: {len(elements.get('links', []))}")
        print(f"表格数量: {len(elements.get('tables', []))}")
        print(f"图片数量: {len(elements.get('images', []))}")
        
        # 显示选择器建议
        suggestions = elements.get('selectors_suggestions', [])
        if suggestions:
            print("\n选择器建议:")
            for suggestion in suggestions:
                print(f"  {suggestion['element_type']}: {suggestion['text']}")
                for selector in suggestion['selectors']:
                    if selector:
                        print(f"    选择器: {selector}")
        
        print(f"\n截图路径: {analysis_result.get('screenshot_path', 'N/A')}")
        print(f"HTML源码路径: {analysis_result.get('html_path', 'N/A')}")
        print("="*50)


def main():
    """主函数"""
    analyzer = PageAnalyzer()
    
    try:
        # 从配置文件读取URL
        web_config = analyzer.config_loader.get_web_config()
        base_url = web_config.get("base_url", "http://192.168.24.100")
        
        # 构建登录页面URL
        login_url = f"{base_url}/login" if not base_url.endswith("/login") else base_url
        
        print(f"从配置文件读取的URL: {base_url}")
        print(f"登录页面URL: {login_url}")
        
        # 如果命令行提供了URL参数，则使用命令行参数
        if len(sys.argv) > 1:
            url = sys.argv[1]
            page_name = sys.argv[2] if len(sys.argv) > 2 else "页面分析"
        else:
            url = login_url
            page_name = "登录页面"
        
        print(f"开始分析页面: {url}")
        
        analyzer.setup_browser(headless=False)
        result = analyzer.analyze_page(url, page_name)
        
        if "error" in result:
            print(f"分析失败: {result['error']}")
        else:
            print("页面分析完成！")
            
    except Exception as e:
        print(f"程序执行失败: {e}")
    finally:
        analyzer.teardown_browser()


if __name__ == "__main__":
    main() 
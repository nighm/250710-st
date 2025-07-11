#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连接测试工具
检查服务器连接状态和页面加载情况
"""

import sys
import time
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.config_loader import ConfigLoader


def test_connection():
    """测试服务器连接"""
    config_loader = ConfigLoader()
    web_config = config_loader.get_web_config()
    
    base_url = web_config.get("base_url", "http://192.168.24.100")
    
    print("连接测试工具")
    print("="*50)
    print(f"测试URL: {base_url}")
    print("="*50)
    
    # 测试不同的URL组合
    test_urls = [
        base_url,
        f"{base_url}/",
        f"{base_url}/login",
        f"{base_url}/index.html",
        f"{base_url}/index.php",
        f"{base_url}/admin",
        f"{base_url}/admin/login",
        f"{base_url}/login.html",
        f"{base_url}/login.php"
    ]
    
    for url in test_urls:
        print(f"\n测试URL: {url}")
        try:
            # 禁用SSL验证
            response = requests.get(url, verify=False, timeout=10, allow_redirects=True)
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            print(f"最终URL: {response.url}")
            
            if response.status_code == 200:
                print("✓ 连接成功！")
                content_length = len(response.content)
                print(f"页面大小: {content_length} 字节")
                
                if content_length > 0:
                    print("页面内容预览:")
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                else:
                    print("页面内容为空")
                    
                return url  # 返回第一个成功的URL
            else:
                print(f"✗ 连接失败，状态码: {response.status_code}")
                
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL证书错误: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"✗ 连接错误: {e}")
        except requests.exceptions.Timeout as e:
            print(f"✗ 连接超时: {e}")
        except Exception as e:
            print(f"✗ 其他错误: {e}")
    
    return None


def test_with_playwright():
    """使用Playwright测试页面加载"""
    try:
        from playwright.sync_api import sync_playwright
        
        config_loader = ConfigLoader()
        web_config = config_loader.get_web_config()
        base_url = web_config.get("base_url", "http://192.168.24.100")
        
        print(f"\n使用Playwright测试: {base_url}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=['--ignore-certificate-errors', '--ignore-ssl-errors']
            )
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            
            try:
                # 访问页面
                print(f"正在访问: {base_url}")
                page.goto(base_url, wait_until="networkidle", timeout=30000)
                
                # 等待页面加载
                page.wait_for_load_state("networkidle", timeout=10000)
                
                print(f"页面标题: {page.title()}")
                print(f"当前URL: {page.url}")
                
                # 检查页面内容
                content = page.content()
                print(f"页面内容长度: {len(content)} 字符")
                
                if len(content) > 0:
                    print("页面内容预览:")
                    text_content = page.inner_text("body")
                    print(text_content[:500] + "..." if len(text_content) > 500 else text_content)
                else:
                    print("页面内容为空")
                
                # 截图
                screenshot_path = "results/connection_test_screenshot.png"
                page.screenshot(path=screenshot_path)
                print(f"截图已保存: {screenshot_path}")
                
                # 保持浏览器打开
                input("按回车键关闭浏览器...")
                
            except Exception as e:
                print(f"Playwright测试失败: {e}")
            finally:
                browser.close()
                
    except ImportError:
        print("Playwright未安装，跳过Playwright测试")
    except Exception as e:
        print(f"Playwright测试出错: {e}")


def main():
    """主函数"""
    print("开始连接测试...")
    
    # 1. 使用requests测试连接
    working_url = test_connection()
    
    if working_url:
        print(f"\n✓ 找到可用的URL: {working_url}")
        
        # 2. 使用Playwright测试页面加载
        test_with_playwright()
    else:
        print("\n✗ 所有URL都无法连接")
        print("请检查:")
        print("1. 服务器是否运行")
        print("2. IP地址是否正确")
        print("3. 网络连接是否正常")
        print("4. 防火墙设置")


if __name__ == "__main__":
    main() 
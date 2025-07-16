# 智能网页自动化测试框架

## 版本：v1.0.0

## 当前版本状态

- 项目结构已优化，采用DDD分层思想，目录清晰
- 用例数据统一为json格式，便于自动化和批量管理
- 新增 docs/设计文档.md、docs/开发计划.md 等中文文档，规范项目开发
- 清理无用文件，提升可维护性
- 后续开发计划已明确，详见 docs/开发计划.md

---

## 🚀 功能特点

### 智能登录系统
- **自动页面分析**：动态识别登录页面元素
- **智能表单填写**：自动填写用户名和密码
- **验证码处理**：等待手动输入验证码，5秒循环重试
- **登录状态检测**：自动判断登录成功/失败

### 灵活测试执行
- **全量执行**：执行所有测试用例
- **指定执行**：执行指定的测试用例ID
- **模块执行**：按功能模块执行测试用例

### 详细测试报告
- **执行统计**：总测试数、通过数、失败数、成功率
- **详细日志**：每个测试用例的执行详情
- **JSON报告**：结构化的测试结果数据

## 📁 项目结构

```
250710-st/
├── src/                          # 源代码
│   ├── domain/                   # 领域层
│   ├── application/              # 应用层
│   ├── infrastructure/           # 基础设施层
│   ├── interfaces/               # 接口层
│   └── web/                     # Web层
├── scripts/                      # 脚本文件
│   └── python/                  # Python脚本
│       ├── smart_login.py       # 智能登录工具
│       ├── test_runner.py       # 测试执行器
│       ├── page_analyzer.py     # 页面分析工具
│       └── connection_test.py   # 连接测试工具
├── config/                       # 配置文件
│   └── settings.yaml            # 系统配置
├── data/                        # 数据文件
│   └── cases/                   # 测试用例
├── results/                     # 测试结果
├── tests/                       # 测试文件
├── requirements.txt              # Python依赖
├── setup_project.py             # 项目设置脚本
└── README.md                    # 项目说明
```

## 🛠️ 安装配置

### 1. 环境要求
- Python 3.8+
- Playwright
- 现代浏览器（Chrome/Edge/Firefox）

### 2. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 3. 配置系统
```bash
# 运行项目设置脚本
python setup_project.py
```

### 4. 配置登录信息
编辑 `config/settings.yaml`：
```yaml
url: http://your-server-ip
username: your-username
password: your-password
timeout: 30
headless: false
slow_mo: 1000
```

## 🎯 使用方法

### 1. 智能登录测试
```bash
# 测试智能登录功能
python scripts/python/smart_login.py
```

### 2. 页面分析
```bash
# 分析指定页面
python scripts/python/page_analyzer.py "https://example.com" "页面名称"
```

### 3. 连接测试
```bash
# 测试服务器连接
python scripts/python/connection_test.py
```

### 4. 测试执行

#### 执行所有测试用例
```bash
python scripts/python/test_runner.py --all
```

#### 执行指定测试用例
```bash
python scripts/python/test_runner.py --test-cases TC_1_1_1 TC_1_1_2
```

#### 按模块执行测试
```bash
python scripts/python/test_runner.py --module 用户管理
```

## 📊 测试用例分类

### 用户管理模块
- **TC_1_1_1**: 用户录入测试
- **TC_1_1_2**: 用户查询测试

### 系统管理模块
- **TC_2_1_1**: 系统配置测试
- **TC_2_1_2**: 系统监控测试

### 权限管理模块
- **TC_3_1_1**: 权限分配测试

## 📈 输出文件

### 测试报告
- **位置**: `results/test_report_YYYYMMDD_HHMMSS.json`
- **内容**: 测试执行结果和统计信息

### 页面分析
- **位置**: `results/page_analysis_*.json`
- **内容**: 页面元素分析结果

### 登录分析
- **位置**: `results/login_analysis_*.json`
- **内容**: 登录页面分析结果

### 截图文件
- **位置**: `results/*.png`
- **内容**: 页面截图和分析图片

## 🔧 技术架构

### 分层设计
- **配置层**: ConfigLoader - 配置管理
- **登录层**: SmartLogin - 智能登录
- **执行层**: TestRunner - 测试执行
- **报告层**: TestReport - 报告生成

### 核心特性
- **DDD架构**: 领域驱动设计
- **智能分析**: 动态页面元素识别
- **配置驱动**: 测试用例配置化
- **模块化**: 功能模块独立

## 🚀 核心优势

### 1. 智能化
- 自动分析页面结构
- 动态识别页面元素
- 智能处理验证码

### 2. 灵活性
- 支持多种执行方式
- 可配置的测试用例
- 模块化的功能设计

### 3. 可维护性
- 清晰的项目结构
- 详细的文档说明
- 完善的错误处理

### 4. 可扩展性
- 支持新测试类型
- 支持新功能模块
- 支持新报告格式

## 📝 开发指南

### 添加新测试用例
1. 在 `data/cases/` 目录添加测试用例文件
2. 在测试执行器中添加对应的执行方法
3. 更新模块测试用例映射

### 添加新功能模块
1. 创建模块对应的页面对象
2. 实现模块的测试方法
3. 更新测试用例分类

### 自定义配置
1. 修改 `config/settings.yaml` 配置文件
2. 添加新的配置项
3. 在代码中使用配置

## 🐛 故障排除

### 常见问题

#### 1. 登录失败
- 检查网络连接
- 确认用户名密码正确
- 手动输入验证码

#### 2. 页面元素找不到
- 检查页面是否正常加载
- 确认元素选择器正确
- 查看详细错误日志

#### 3. 浏览器相关问题
- 确保Playwright已正确安装
- 检查浏览器驱动
- 重启测试执行器

### 调试技巧
- 使用 `headless: false` 查看浏览器操作
- 查看生成的截图和日志文件
- 使用页面分析工具调试

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献步骤
1. Fork 本项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 参与讨论

---

**注意**: 本项目仅供学习和研究使用，请遵守相关法律法规和网站使用条款。

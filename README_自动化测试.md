# 自动化测试项目使用说明

## 项目概述

本项目基于DDD（领域驱动设计）架构，为您的JSON测试用例提供完整的Web自动化测试解决方案。项目专门针对 `TC_1_1_1-系统管理_用户管理_用户录入` 测试用例进行了自动化实现。

## 项目架构

```
项目根目录/
├── src/                          # 源代码目录
│   ├── domain/                   # 领域层 - 测试用例实体
│   │   └── test_case.py         # 测试用例领域实体
│   ├── application/              # 应用层 - 测试执行服务
│   │   └── test_execution_service.py  # 测试执行服务
│   ├── infrastructure/           # 基础设施层 - 数据访问
│   │   ├── config_loader.py     # 配置加载器
│   │   └── test_case_repository.py  # 测试用例仓储
│   ├── interfaces/               # 接口层 - CLI工具
│   │   └── test_cli.py         # 测试CLI接口
│   └── web/                     # Web自动化层
│       ├── base_page.py         # 基础页面类
│       ├── login_page.py        # 登录页面
│       └── user_management_page.py  # 用户管理页面
├── data/cases/json/             # 测试用例数据
│   └── 1-TC_1_1_1-系统管理_用户管理_用户录入.json
├── config/                      # 配置文件
│   └── settings.yaml           # 系统配置
├── scripts/python/              # 自动化脚本
│   └── run_user_input_test.py  # 用户录入测试脚本
└── results/                     # 测试结果输出
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+和必要的依赖：

```bash
# 安装依赖
pip install playwright pandas openpyxl pyyaml

# 安装Playwright浏览器
playwright install chromium
```

### 2. 配置系统

首次使用需要初始化配置文件：

```bash
# 初始化配置文件
python -m src.interfaces.test_cli init-config
```

然后编辑 `config/settings.yaml` 文件，填入正确的系统访问信息：

```yaml
url: http://your-system-url
username: your_username
password: your_password
timeout: 30
headless: true
slow_mo: 1000
```

### 3. 运行测试

#### 方式一：使用专用脚本（推荐）

```bash
# 运行用户录入测试用例
python scripts/python/run_user_input_test.py
```

#### 方式二：使用CLI工具

```bash
# 查看所有测试用例
python -m src.interfaces.test_cli list

# 执行指定测试用例
python -m src.interfaces.test_cli run TC_1_1_1

# 执行所有可自动化的测试用例
python -m src.interfaces.test_cli run-all

# 查看测试统计信息
python -m src.interfaces.test_cli stats

# 查看配置信息
python -m src.interfaces.test_cli config
```

## 测试用例分析

### 原始测试用例（TC_1_1_1）

**测试用例名称**: 在用户录入界面，"用户账号"输入长度范围内的合法字符，其他参数填写正确，点击提交，录入用户成功

**预置条件**: 服务端可以正常登陆

**操作步骤**:
1. 进入 系统管理-用户管理 页面
2. 点击 用户录入
3. "用户账号"输入长度范围内的合法字符，其他参数填写正确，点击提交

**预期输出**: 录入用户成功

### 自动化实现

项目将上述测试用例完全自动化，包括：

1. **自动登录系统** - 基于配置文件中的凭据
2. **智能导航** - 自动进入系统管理-用户管理页面
3. **动态数据生成** - 自动生成合法的用户账号和名称
4. **表单填写** - 自动填写所有必要的用户参数
5. **结果验证** - 自动验证提交是否成功
6. **截图记录** - 自动保存测试过程的截图
7. **结果报告** - 生成详细的测试执行报告

## 核心功能特性

### 1. DDD架构设计

- **领域层**: 封装测试用例的业务逻辑和数据
- **应用层**: 协调测试执行流程
- **基础设施层**: 处理数据访问和配置管理
- **接口层**: 提供CLI和Web界面
- **Web层**: 实现页面对象模型

### 2. 智能测试执行

- **步骤解析**: 自动解析JSON中的测试步骤
- **动态数据**: 根据规则生成测试数据
- **错误处理**: 完善的异常处理和错误报告
- **结果验证**: 自动验证预期结果

### 3. 详细报告

- **执行时间**: 记录每个步骤的执行时间
- **截图保存**: 自动保存测试过程截图
- **JSON报告**: 生成结构化的测试结果报告
- **控制台输出**: 实时显示执行进度和状态

### 4. 配置管理

- **YAML配置**: 使用YAML格式管理配置
- **环境适配**: 支持不同环境的配置
- **安全存储**: 敏感信息独立配置

## 测试执行流程

### 1. 环境检查
- 验证项目结构完整性
- 检查配置文件有效性
- 确认依赖项安装

### 2. 测试准备
- 加载测试用例数据
- 初始化浏览器环境
- 设置页面对象模型

### 3. 执行测试
- 登录系统
- 导航到目标页面
- 执行测试步骤
- 验证预期结果

### 4. 结果处理
- 保存测试结果
- 生成截图
- 更新测试状态
- 输出详细报告

## 输出文件说明

### 测试结果文件
位置: `results/TC_1_1_1_result_YYYYMMDD_HHMMSS.json`

包含信息:
- 测试用例基本信息
- 执行时间和状态
- 步骤执行详情
- 验证结果
- 错误信息（如有）

### 截图文件
位置: `results/TC_1_1_1_YYYYMMDD_HHMMSS.png`

记录测试执行过程中的页面状态，便于问题排查。

## 扩展开发

### 添加新的测试用例

1. 在 `data/cases/json/` 目录下创建新的JSON文件
2. 确保JSON格式与现有测试用例一致
3. 在 `src/web/` 目录下创建对应的页面对象
4. 在 `src/application/test_execution_service.py` 中添加执行逻辑

### 自定义页面元素

如果系统页面元素发生变化，需要更新对应的页面对象：

- `src/web/login_page.py` - 登录页面元素
- `src/web/user_management_page.py` - 用户管理页面元素

### 添加新的验证规则

在 `src/application/test_execution_service.py` 的 `_verify_expected_output` 方法中添加新的验证逻辑。

## 故障排除

### 常见问题

1. **配置错误**
   - 检查 `config/settings.yaml` 文件格式
   - 确认URL、用户名、密码正确

2. **元素定位失败**
   - 检查页面元素选择器是否正确
   - 确认页面加载完成

3. **浏览器启动失败**
   - 确认已安装Playwright浏览器
   - 检查系统权限

4. **测试执行超时**
   - 调整配置文件中的超时时间
   - 检查网络连接

### 调试模式

设置 `headless: false` 可以观察浏览器执行过程：

```yaml
headless: false
slow_mo: 2000  # 增加延迟便于观察
```

## 技术栈

- **Python 3.8+**: 主要开发语言
- **Playwright**: Web自动化框架
- **PyYAML**: 配置文件处理
- **DDD架构**: 领域驱动设计
- **Page Object Model**: 页面对象模型

## 贡献指南

1. 遵循DDD架构原则
2. 保持代码注释详细
3. 添加适当的错误处理
4. 确保测试覆盖完整
5. 更新相关文档

## 许可证

本项目采用MIT许可证，详见LICENSE文件。 
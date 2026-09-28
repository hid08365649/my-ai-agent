
# AI Agent 助手

一个基于 DeepSeek API 的智能对话助手，支持工具调用、实时天气查询、对话记忆。

## 功能

- 多轮对话，具备上下文记忆
- Function Calling：AI 可自主调用工具
- 支持三个工具：
  - 实时天气查询（接入 wttr.in）
  - 数学计算
  - 当前时间查询
- 流式输出
- 错误处理
- 网页界面（Streamlit）
- 命令系统：`/clear` 清空记忆，`/help` 查看帮助

## 技术栈

- Python
- OpenAI SDK（调用 DeepSeek API）
- Function Calling
- Streamlit（网页界面）
- requests（网络请求）

## 运行方式

1. 安装依赖：
```bash
pip install openai streamlit requests python-dotenv

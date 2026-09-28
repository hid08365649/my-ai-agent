import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
# ===== 三个工具函数 =====
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data['current_condition'][0]
        weather_desc = current['weatherDesc'][0]['value']
        temp_c = current['temp_C']
        return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
    except Exception as e:
        return f"查询天气失败：{e}"

def calculator(a, b, op):
    if op == "加":
        return a + b
    elif op == "减":
        return a - b
    elif op == "乘":
        return a * b
    elif op == "除":
        return a / b
    return "不支持的运算"

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ===== 三个工具的说明 =====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名字"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算两个数字的加减乘除",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                    "op": {"type": "string", "description": "运算类型：加、减、乘、除"}
                },
                "required": ["a", "b", "op"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "查询当前的日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# ===== 记忆：放函数外面，跨对话共享 =====
messages = [
    {"role": "system", "content": "你是一个可爱的助手，可以查天气、算数、查时间。"}
]

# ===== 核心函数：输入用户的话，返回 AI 的回复 =====
def chat(user_input):
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=tools
        )
        reply = response.choices[0].message
    except Exception as e:
        return f"出错了：{e}"

    if reply.tool_calls:
        messages.append(reply)
        for tool_call in reply.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if name == "get_weather":
                result = get_weather(args["city"])
            elif name == "calculator":
                result = calculator(args["a"], args["b"], args["op"])
            elif name == "get_time":
                result = get_time()
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        try:
            final = client.chat.completions.create(
                model="deepseek-flash",
                messages=messages,
                tools=tools
            )
            ai_reply = final.choices[0].message.content
        except Exception as e:
            return f"生成回答时出错：{e}"
    else:
        ai_reply = reply.content

    messages.append({"role": "assistant", "content": ai_reply})
    return ai_reply



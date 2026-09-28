import streamlit as st
from agent_core import chat

st.title("我的 AI ")

# 初始化聊天记录（给界面显示用）
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# 显示历史对话
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 输入框
user_input = st.chat_input("说点什么...")

if user_input:
    # 显示用户的话
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 调用核心逻辑
    ai_reply = chat(user_input)

    # 显示 AI 的话
    st.session_state.display_messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)
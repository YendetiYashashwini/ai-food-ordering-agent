# Arc 5 - Streamlit Frontend

import streamlit as st
import requests

st.title("🍽️ AI Food Ordering Agent")
st.caption("Ask me anything about the menu or place an order!")

if "messages" in st.session_state:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant" and msg.get("content"):
            with st.chat_message("assistant"):
                st.write(msg["content"])

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.write(prompt)

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={
            "message": prompt,
            "messages": st.session_state.get("history", [])
        }
    )

    data = response.json()

    with st.chat_message("assistant"):
        st.write(data["reply"])

    st.session_state.history = data["messages"]
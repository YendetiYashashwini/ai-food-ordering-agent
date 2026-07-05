# Arc 5 - Streamlit Frontend
# Chat UI for our food ordering agent
# Connects to Arc 4 FastAPI backend

import os
import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv(r"c:\Users\yende\Projects\AI Food Ordering Agent\.env")

# Backend URL - where Arc 4 is running
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🍔 Smart Food Assistant")
st.caption("Find and order meals that match your nutrition and budget goals!")

# Keep chat history across reruns
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get new input from the user
user_input = st.chat_input("e.g. Find me a high-protein meal under ₹300 and order it")

if user_input:
    # Show the user's message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the backend and show the response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = httpx.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": user_input,
                        "messages": st.session_state["messages"][:-1],  # send history
                    },
                    timeout=60.0,
                )
                resp.raise_for_status()
                reply = resp.json().get("reply", "Something went wrong.")
            except httpx.ConnectError:
                reply = f"❌ Cannot reach backend at `{BACKEND_URL}`. Is Arc 4 running?"
            except httpx.HTTPStatusError as e:
                reply = f"❌ Backend error {e.response.status_code}: {e.response.text}"
            except Exception as e:
                reply = f"❌ Unexpected error: {e}"

        st.markdown(reply)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
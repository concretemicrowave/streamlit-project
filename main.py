import threading
import streamlit as st


@st.cache_resource
def get_room():
    return {"messages": [], "lock": threading.Lock()}


room = get_room()

st.write("""
# Chat room
""")

if "name" not in st.session_state:
    with st.form("join"):
        name = st.text_input("Display name")
        if st.form_submit_button("Join") and name.strip():
            st.session_state.name = name.strip()
            st.rerun()
    st.stop()

st.caption(f"Chatting as {st.session_state.name}")


@st.fragment(run_every=1)
def show_messages():
    for m in room["messages"]:
        with st.chat_message("user" if m["name"] == st.session_state.name else "assistant"):
            st.markdown(f"**{m['name']}**")
            st.markdown(m["text"])


show_messages()

text = st.chat_input("Message")
if text:
    with room["lock"]:
        room["messages"].append({"name": st.session_state.name, "text": text})
    st.rerun()

import streamlit as st

from patterns.tool_using.graph import build_graph


WELCOME_MESSAGE = "Hi. What would you like to work through?"


@st.cache_resource
def get_workflow():
    return build_graph()


def render_message(message):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("route") == "math" and message.get("expression"):
            st.caption(f"Arithmetic tool | `{message['expression']}`")
        elif message.get("route") == "general":
            st.caption("General answer")


st.set_page_config(
    page_title="Agentic Assistant",
    page_icon="💬",
    layout="centered",
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #f7faf9 0%, #edf3f0 62%, #f5f0e9 100%);
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        background: #e7efeb;
    }
    [data-testid="stChatMessage"] {
        border: 1px solid #d8e2dd;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.88);
    }
    h1, h2, h3 {
        font-family: Georgia, "Times New Roman", serif;
        color: #173b37;
    }
    [data-testid="stChatInput"] {
        border-color: #9ab7aa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Agentic Assistant")
st.caption("Tool-using workflow")

with st.sidebar:
    st.subheader("Conversation")
    if st.button("New conversation", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
        st.rerun()
    st.divider()
    st.caption("Model: gpt-4o-mini")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]

for chat_message in st.session_state.messages:
    render_message(chat_message)

if question := st.chat_input("Send a message"):
    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)
    render_message(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = get_workflow().invoke({"question": question})
                answer = result.get("result", "I could not produce an answer.")
                route = result.get("route", "general")
                expression = result.get("expression", "")
            except Exception:
                answer = "I couldn't complete that request. Check your API key and network connection, then try again."
                route = "error"
                expression = ""

        st.markdown(answer)
        if route == "math" and expression:
            st.caption(f"Arithmetic tool | `{expression}`")
        elif route == "general":
            st.caption("General answer")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "route": route,
            "expression": expression,
        }
    )
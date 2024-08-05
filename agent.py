import streamlit as st
from agent_class import Agent
import logging

logging.basicConfig(level=logging.DEBUG)


def create_agent():
    return Agent()


def main():
    agent = create_agent()

    st.set_page_config(layout="wide")
    st.title('Recomendações de Jogos')
    st.write("Descubra recomendações de jogos incríveis!")

    # Session state to keep track of chat history and pending request
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "pending_request" not in st.session_state:
        st.session_state.pending_request = None

    def get_recommendation(request):
        response = agent.get_recommendation(request)
        logging.debug(f"get_recommendation response: {response}")
        return response['agent_response']

    # Display chat history with different background colors and white font
    for chat in st.session_state.chat_history:
        st.markdown(f"""
            <div style='background-color: #333; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <strong>Você:</strong> {chat['user']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background-color: #555; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <strong>IA:</strong> {chat['response']}
            </div>
            """, unsafe_allow_html=True)

    # Input area for new user question
    with st.form(key='chat_form', clear_on_submit=True):
        request = st.text_area("Que tipo de jogo você está procurando?", key='user_input')
        submit_button = st.form_submit_button(label='Enviar')

    if submit_button and request:
        # Add user question to chat history with a placeholder response
        st.session_state.chat_history.append({"user": request, "response": "Processando..."})
        st.session_state.pending_request = request
        st.rerun()  # Refresh the page to update the chat history and show a new input field

    if st.session_state.pending_request:
        # Process the response
        response = get_recommendation(st.session_state.pending_request)

        # Update the chat history with the actual response
        st.session_state.chat_history[-1]["response"] = response
        st.session_state.pending_request = None
        st.rerun()


if __name__ == "__main__":
    main()

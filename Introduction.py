import streamlit as st
from openai import OpenAI
from streamlit.logger import get_logger
from streamlit_extras.app_logo import add_logo
from streamlit_feedback import streamlit_feedback
import trubrics

LOGGER = get_logger(__name__)


def run():
    def main_page():
        st.markdown("# Introduction")
        st.markdown(
        """
        This is the companion site to Fine-tuning Large Language Models. You'll be able to review material, study expanded examples, and use code-snippets to quickly get started. Relevant material is provided for each chapter. 
        """
        )

    def chapter1():
        st.markdown("# Chapter 1")

    def chapter2():
        st.markdown("# Chapter 2")
        openai_api_key = ""
        openai_api_key = st.sidebar.text_input('OpenAI API Key', value=openai_api_key, key='OpenAI Key', type="password")
        st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        st.sidebar.markdown("[Get visual studio code](https://code.visualstudio.com/Download)")
        st.sidebar.markdown("[Create your hugging face account](https://huggingface.co)")
        st.sidebar.markdown("[Work with google colab](https://colab.research.google.com)")
        st.sidebar.markdown("[Get Python](https://www.python.org/downloads/)")
        st.sidebar.markdown("[Install pip](https://pip.pypa.io/en/stable/installation/)")


        # Example ChatBot
        st.markdown("### Simple Chatbot Example")
        st.markdown("Below, you'll be able to chat with a simple chatbot assistant to make sure you're able to properly use your OpenAI API Key")
        
        # Example ChatBot
        st.markdown("### Using Python")
        st.markdown("To follow along with the book, you'll be able to either work locally from your own systems terminal or work from a colab notebook. Below is a simple example showing how to install the openai library to a colab space.")
        st.code("!pip install openai", language='bash')
        st.markdown("The exclamation point indicates a system command rather than python code, on your systems terminal you only need to type the same command without the !.")
        
        
        # Modifying ChatBot Behavior
        st.markdown("### Modifying Chatbot Behavior")
        st.markdown("Below is a simple json message that will modify the behavior of the llm responses. Recall that JSON is comprised of key-value pairs and that here, we're using the value of **system** for the **role** key. Note that **user** and **assistant** are also possible values, where **user** specifies the reponse from outside the llm and **assistant** is speaking on behalf of the llm.")
        st.json(
            {"role": "system", "content": "You are an ai assitant"}
        )

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are an ai assitant"},
                {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
            ]
        if "response" not in st.session_state:
            st.session_state["response"] = None

        messages = st.session_state.messages
        for msg in messages:
            if msg["role"] == "assistant":
              st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
            messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            st.session_state["response"] = response.choices[0].message.content
            with st.chat_message("assistant"):
                messages.append({"role": "assistant", "content": st.session_state["response"]})
                st.write(st.session_state["response"])

        if st.session_state["response"]:
            feedback = streamlit_feedback(
                feedback_type="thumbs",
                optional_text_label="[Optional] Please provide an explanation",
                key=f"feedback_{len(messages)}",
            )
            # This app is logging feedback to Trubrics backend, but you can send it anywhere.
            # The return value of streamlit_feedback() is just a dict.
            # Configure your own account at https://trubrics.streamlit.app/
            if feedback and "TRUBRICS_EMAIL" in st.secrets:
                config = trubrics.init(
                    email=st.secrets.TRUBRICS_EMAIL,
                    password=st.secrets.TRUBRICS_PASSWORD,
                )
                collection = trubrics.collect(
                    component_name="default",
                    model="gpt",
                    response=feedback,
                    metadata={"chat": messages},
                )
                trubrics.save(config, collection)
                st.toast("Feedback recorded!", icon="📝")     

    page_names_to_funcs = {
        "Introduction": main_page,
        "Chapter 1": chapter1,
        "Chapter 2": chapter2,
    }

    st.sidebar.image(image="https://assets-global.website-files.com/654319b06bb59e8d9e5582f3/65661a57fe3c6cfbeb1aadaa_Asset%202.png")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    selected_page = st.sidebar.selectbox("Select a chapter", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("# Fine-tuning LLMs")
    st.sidebar.markdown("#### Brumbaugh-Morales ©️ 2024")

if __name__ == "__main__":
    run()
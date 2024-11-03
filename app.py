import streamlit as st
import os
import openai
from SimplerLLM.language.llm import LLM, LLMProvider

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM instance
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

# Define function for chatbot responses
def get_chatbot_response(user_input):
    """Generate a response from the chatbot based on user input."""
    messages = [{"role": "user", "content": user_input}]  # Construct the messages
    return llm_instance.generate_response(messages=messages)

# Define tool functions
def summarize_content(content):
    """Summarizes the provided content."""
    messages = [{"role": "user", "content": f"Summarize the following content: {content}"}]
    return llm_instance.generate_response(messages=messages)

def perform_calculation(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"

# Initialize Streamlit UI
st.title("🤖 Interactive Chatbot with Dynamic Tool Use")
st.markdown("Ask anything, and I will try to assist you!")

# User input for chatbot
user_input = st.text_input("You: ", placeholder="Type your message here...")

# Process the user input when the button is clicked
if st.button("Send"):
    if user_input:
        # Get chatbot response
        response = get_chatbot_response(user_input)

        # Check if the user asked for a specific action
        if "summarize" in user_input.lower():
            content = user_input.split("summarize")[-1].strip()  # Extract content to summarize
            result = summarize_content(content)
            response = f"Summary: {result}"
        elif "calculate" in user_input.lower():
            expression = user_input.split("calculate")[-1].strip()  # Extract expression to calculate
            result = perform_calculation(expression)
            response = f"Calculation Result: {result}"

        st.markdown(f"**Chatbot:** {response}")
    else:
        st.warning("Please enter a message.")

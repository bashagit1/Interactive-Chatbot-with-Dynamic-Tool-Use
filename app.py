import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate a chatbot response
def get_chatbot_response(user_input):
    """Generate a response from the chatbot based on user input."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        # Extract the content directly from the response object
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Failed to generate content. Error: {e}"


# Tool Functions
def summarize_content(content):
    """Summarizes the provided content."""
    summary_prompt = f"Summarize the following content: {content}"
    return get_chatbot_response(summary_prompt)

def perform_calculation(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"

# Streamlit UI
st.title("🤖 Interactive Chatbot with Dynamic Tool Use")
st.markdown("Ask anything, and I will try to assist you!")

# User input for chatbot
user_input = st.text_input("You: ", placeholder="Type your message here...")

# Process the user input when the button is clicked
if st.button("Send"):
    if user_input:
        # Generate chatbot response
        if "summarize" in user_input.lower():
            content = user_input.split("summarize")[-1].strip()  # Extract content to summarize
            response = summarize_content(content)
        elif "calculate" in user_input.lower():
            expression = user_input.split("calculate")[-1].strip()  # Extract expression to calculate
            response = perform_calculation(expression)
        else:
            response = get_chatbot_response(user_input)

        # Display the response
        st.markdown(f"**Chatbot:** {response}")
    else:
        st.warning("⚠️ Please enter a message.")

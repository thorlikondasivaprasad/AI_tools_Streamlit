import streamlit as st
import google.generativeai as genai
import re

GOOGLE_API_KEY = "API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
# model 
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Clean and format the response text, then split into points
def clean_response(text):
    # Remove unwanted characters like "*" and extra spaces
    cleaned_text = re.sub(r'[\*]+', '', text)  # Removes asterisks
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Collapses multiple spaces to a single space
    # Split by periods or other delimiters to create points
    points = [point.strip() for point in re.split(r'[.;]\s*', cleaned_text) if point]
    return points

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text + " "
    # Clean and split response into points
    return clean_response(full_response.strip())

# Initialize Streamlit app
st.sidebar.title("AI🤖 Store🧰")
page = st.sidebar.selectbox("Gen AI Tools", ["Q&A GPT","AI Code Generator","AI Text Summarizer"])

if page == "Q&A GPT":
    st.title(f"Welcome to Q&A Chatbot 🤖")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    input = st.text_input("Input: 🖊", key="input")
    submit = st.button("Ask Query 🧐")
    if submit and input:
        response_points = get_gemini_response(input)
        # Add user query and response to session chat history
        st.session_state['chat_history'].append(("You", input))
        st.session_state['chat_history'].append(("Bot", response_points))
        with st.chat_message("assistant", avatar="🤖"):
            for point in response_points:
                st.write(f"- {point}")  # Display each point as a bullet point
    # Display Chat History
    st.subheader("Chat History 👇")
    for role, text in st.session_state['chat_history']:
        if role == "Bot":
            for point in text:
                st.write(f"{role}: - {point}")
        else:
            st.write(f"{role}: {text}")

elif page == "AI Code Generator":
    st.title(f"Welcome to the AI Code💻 Generator")
    prompt = st.text_area("Enter your code prompt:")
    language = st.selectbox("Select language:", ["Python", "JavaScript", "C++", "Java", "Go"])
    # code_style = st.selectbox("Select code style:", ["Clean", "Concise", "Efficient", "Readable"])
    generate = st.button("Generate Code")
    if generate and prompt:
        # Construct the prompt for Gemini Pro
        code_prompt = f"Generate {language} code to : {prompt} with documentation."
        # Send the prompt to Gemini Pro and get the response
        response = chat.send_message(code_prompt, stream=True)
        full_response = ""
        for chunk in response:
            full_response += chunk.text + " "
        # Display the generated code in a code block
        st.code(full_response, language=language)
      
elif page == "AI Text Summarizer":
    st.title(f"Welcome to the AI Text Summarizer")
    prompt = st.text_area("Enter the Long-Text here to Summarize: ")
    no_of_words = st.selectbox("Summarize to No.of words: ",[50,100,200,300,500])
    generate = st.button("Generate Summarized Text")
    if generate and prompt:
        text_prompt = f"Summarize {prompt} to {no_of_words} no.of words using simple words."
        response = chat.send_message(text_prompt,stream=True)
        full = ""
        for chunk in response:
            full+= chunk.text +" "
        st.write("Copy the code from top-right of output:")
        st.code(st.write(full))

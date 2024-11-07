import streamlit as st

# Create a sidebar
st.sidebar.title("Sidebar Menu")

# Sidebar items
page = st.sidebar.selectbox("Select a page:", ["Home", "About", "Contact"])

# Sidebar slider example
slider_value = st.sidebar.slider("Select a range", 0, 100, 25)

# Sidebar input box example
name = st.sidebar.text_input("Enter your name:")

# Main content based on the sidebar selection
if page == "Home":
    st.title(f"Welcome to the {page} page")
    st.write(f"Hello {name}, you've selected the Home page and chosen a range of {slider_value}.")
    
elif page == "About":
    st.title(f"Welcome to the {page} page")
    st.write(f"Learn more about us, {name}!")

elif page == "Contact":
    st.title(f"Welcome to the {page} page")
    st.write(f"Feel free to contact us, {name}!")

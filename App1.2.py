import streamlit as st
from openai import OpenAI
import time

# Set page configuration
st.set_page_config(page_title="AI Prompt Enhancer", layout="wide")

# Add CSS for background and styling with improved proportions and readability
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/blue-sky-with-clouds-background-elegant_1017-26302.jpg");
        background-size: cover;
    }
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .content-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title {
        text-align: center;
        color: #1E3A8A;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
    }
    /* Reduce default Streamlit element heights */
    .stTextInput>div>div>input {
        padding: 0.5rem;
    }
    .stTextArea>div>div>textarea {
        padding: 0.5rem;
        min-height: 80px !important;
    }
    /* Adjust font sizes for better readability */
    .stTextInput label, .stTextArea label {
        font-size: 16px;
        font-weight: 500;
    }
    p, .stTextInput, .stTextArea, li, div {
        font-size: 15px;
    }
    h3 {
        font-size: 20px;
    }
    /* Adjust spacing */
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    .rating-button button {
        font-size: 20px;
        padding: 5px 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Create a main container for centering content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# App title with styling
st.markdown('<div class="title">AI Prompt Enhancer</div>', unsafe_allow_html=True)

# Create a two-column layout for the input form
col1, col2 = st.columns([3, 2])

with col1:
    # Input form container
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    # Ask for the OpenAI API Key
    api_key = st.text_input("OpenAI API Key", type="password", help="Your API key is required to use the OpenAI service")
    
    # Create two columns for Role and shorter inputs
    role_col, context_col = st.columns([1, 1])
    
    with role_col:
        role = st.text_input("Role", placeholder="e.g., Python developer")
    
    with context_col:
        context = st.text_input("Context", placeholder="e.g., Building AI apps")
    
    # Task gets its own row
    task = st.text_area("Task", placeholder="e.g., Help me build a Streamlit app", height=100)
    
    # Create button with some space around it
    st.markdown("<div style='padding: 10px 0;'>", unsafe_allow_html=True)
    enhance_button = st.button("Enhance Prompt")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Instructions and tips
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### How to Use")
    st.markdown("""
    1. Enter your OpenAI API key
    2. Define the role (who the AI should be)
    3. Add context (your situation/background)
    4. Describe your specific task
    5. Click "Enhance Prompt"
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for storing the enhanced prompt and rating
if 'enhanced_prompt' not in st.session_state:
    st.session_state.enhanced_prompt = ""
if 'rating_submitted' not in st.session_state:
    st.session_state.rating_submitted = False

# Process when user clicks the Enhance Prompt button
if enhance_button:
    if api_key and role and context and task:
        try:
            # Create a placeholder for the loading spinner
            with st.markdown('<div class="content-box">', unsafe_allow_html=True):
                with st.spinner("Enhancing your prompt... Please wait while we work our magic! ✨"):
                    # Initialize the client with the API key
                    client = OpenAI(api_key=api_key)
                    
                    # Construct the system message
                    system_message = """
                    You are a prompt engineering assistant. Your task is to take the user's inputs and 
                    create an enhanced, well-structured prompt that they can use with any AI system.
                    Do not solve the task yourself - only create a better prompt.
                    """
                    
                    # Construct the user message to send to OpenAI
                    user_message = f"""
                    I want to create an enhanced prompt based on these components:
                    
                    ROLE: {role}
                    CONTEXT: {context}
                    TASK: {task}
                    
                    Please format the enhanced prompt in a clear, structured way that I can copy and use with any AI system.
                    Focus only on creating the enhanced prompt, not on solving the task.
                    """

                    # Call the OpenAI API to get an enhanced prompt
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    
                    # Store the enhanced prompt in session state
                    st.session_state.enhanced_prompt = response.choices[0].message.content
                    st.session_state.rating_submitted = False
                    
                    # Small delay to show the loading effect
                    time.sleep(1)
            
            # Display the enhanced prompt and rating in a collapsible section
            output_col1, output_col2 = st.columns([3, 2])
            
            with output_col1:
                # Display the enhanced prompt
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown("### ✅ Your Enhanced Prompt")
                st.text_area("Copy this prompt:", st.session_state.enhanced_prompt, height=150)
                st.info("Copy the text above to use with any AI system")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with output_col2:
                # Rating system
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown("### Rate the Result")
                st.write("How satisfied are you with the prompt?")
                
                # Create a row of rating buttons
                rate_col1, rate_col2, rate_col3, rate_col4, rate_col5 = st.columns(5)
                
                def submit_rating(rating):
                    st.session_state.rating = rating
                    st.session_state.rating_submitted = True
                
                # Add rating buttons with stars
                with rate_col1:
                    st.markdown('<div class="rating-button">', unsafe_allow_html=True)
                    if st.button("⭐"):
                        submit_rating(1)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with rate_col2:
                    st.markdown('<div class="rating-button">', unsafe_allow_html=True)
                    if st.button("⭐⭐"):
                        submit_rating(2)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with rate_col3:
                    st.markdown('<div class="rating-button">', unsafe_allow_html=True)
                    if st.button("⭐⭐⭐"):
                        submit_rating(3)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with rate_col4:
                    st.markdown('<div class="rating-button">', unsafe_allow_html=True)
                    if st.button("⭐⭐⭐⭐"):
                        submit_rating(4)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with rate_col5:
                    st.markdown('<div class="rating-button">', unsafe_allow_html=True)
                    if st.button("⭐⭐⭐⭐⭐"):
                        submit_rating(5)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if st.session_state.rating_submitted:
                    st.success(f"Thanks for your {st.session_state.rating}⭐ rating!")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in all fields including the API key.")

# Display rating section if there's an enhanced prompt but rating not yet submitted
elif st.session_state.enhanced_prompt and not st.session_state.rating_submitted:
    output_col1, output_col2 = st.columns([3, 2])
    
    with output_col1:
        # Display the enhanced prompt
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### ✅ Your Enhanced Prompt")
        st.text_area("Copy this prompt:", st.session_state.enhanced_prompt, height=150)
        st.info("Copy the text above to use with any AI system")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with output_col2:
        # Rating system
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### Rate the Result")
        st.write("How satisfied are you with the prompt?")
        
        # Create a row of rating buttons
        rate_col1, rate_col2, rate_col3, rate_col4, rate_col5 = st.columns(5)
        
        def submit_rating(rating):
            st.session_state.rating = rating
            st.session_state.rating_submitted = True
        
        # Add rating buttons with stars
        with rate_col1:
            st.markdown('<div class="rating-button">', unsafe_allow_html=True)
            if st.button("⭐"):
                submit_rating(1) 
            st.markdown('</div>', unsafe_allow_html=True)
        
        with rate_col2:
            st.markdown('<div class="rating-button">', unsafe_allow_html=True)
            if st.button("⭐⭐"):
                submit_rating(2)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with rate_col3:
            st.markdown('<div class="rating-button">', unsafe_allow_html=True)
            if st.button("⭐⭐⭐"):
                submit_rating(3)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with rate_col4:
            st.markdown('<div class="rating-button">', unsafe_allow_html=True)
            if st.button("⭐⭐⭐⭐"):
                submit_rating(4)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with rate_col5:
            st.markdown('<div class="rating-button">', unsafe_allow_html=True)
            if st.button("⭐⭐⭐⭐⭐"):
                submit_rating(5)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.rating_submitted:
            st.success(f"Thanks for your {st.session_state.rating}⭐ rating!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Close the main container
st.markdown('</div>', unsafe_allow_html=True)
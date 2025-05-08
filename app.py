import streamlit as st
from main import Assistant
import os, time
from vector_store import VectorStore

# Set page config
st.set_page_config(
    page_title="RAG-Powered Q&A Assistant",
    page_icon="🤖",
    layout="centered"
)

@st.cache_resource
def load_assistant():
    return Assistant()

assistant = load_assistant()


st.title("🤖 RAG-Powered Knowledge Assistant")
st.markdown("""
Ask questions about your documents or request calculations/definitions!
- For calculations, use words like *"calculate"* or *"sum"*
- For definitions, use words like *"define {✏️ YOUR WORD}"* or *"what is {✏️ YOUR WORD}"*
""")

if 'history' not in st.session_state:
    st.session_state.history = []

# Document uploading section
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

st.sidebar.header("Document Management")
uploaded_file = st.sidebar.file_uploader(
    "Upload TXT document", 
    type=["txt"],
    accept_multiple_files=False
)

if uploaded_file and not st.session_state.file_uploaded:
    st.sidebar.success(f"File {uploaded_file.name} uploaded successfully!")
    
    os.makedirs("documents", exist_ok=True)
    save_path = os.path.join("documents", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    vector_store = VectorStore()
    vector_store.reset_vector_store()
    st.cache_resource.clear()
    assistant = load_assistant()
    
    st.session_state.file_uploaded = True
    st.rerun()

if st.session_state.file_uploaded and not uploaded_file:
    st.session_state.file_uploaded = False

if st.sidebar.button("Reload Assistant"):
    st.cache_resource.clear()
    assistant = load_assistant()
    st.rerun()


question = st.text_input("Enter your question:", placeholder="Type your question here...")

if st.button("Ask") or question:
    if not question:
        st.warning("Please enter a question")
        st.stop()
    
    with st.spinner("Thinking..."):
        start_time = time.time()
        response = assistant.ask(question)
        processing_time = time.time() - start_time
        
        st.session_state.history.append({
            "question": question,
            "response": response,
            "time": processing_time
        })

    st.divider()
    
    response_type = response['type'].upper()
    if response_type == "RAG":
        st.subheader(f"📚 Document-Based Answer ({response_type})")
    elif response_type == "CALCULATION":
        st.subheader(f"🧮 Calculation Result ({response_type})")
    else:
        st.subheader(f"📖 Definition ({response_type})")
    
    st.markdown(f"""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
    {response['answer']}
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Processed in {processing_time:.2f} seconds")
    
    if response['sources']:
        st.divider()
        st.subheader("Relevant Document Sections")
        
        for i, source in enumerate(response['sources'], 1):
            with st.expander(f"Source {i}"):
                st.markdown(f"**Document:** {source.metadata['source']}")
                st.markdown(f"**Page Content:**")
                st.info(source.page_content[:500] + "...")  # Showing first 500 characters

st.divider()
st.subheader("Session History")
for entry in reversed(st.session_state.history):
    with st.expander(f"{entry['question']} ({entry['time']:.2f}s)"):
        st.markdown(f"**Answer Type:** {entry['response']['type'].upper()}")
        st.markdown(f"**Answer:** {entry['response']['answer']}")
        if entry['response']['sources']:
            st.markdown(f"**Sources Found:** {len(entry['response']['sources'])}")
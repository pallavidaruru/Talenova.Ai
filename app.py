
import streamlit as st
import model
from model import generate_story

st.set_page_config(
    page_title="TaleNova AI",
    page_icon="📖",
    layout="centered"
)

# Debug information
st.title("📖 TaleNova AI")
st.subheader("Multilingual Interactive Story Generation Chatbot")
st.write("Create and explore complete stories with AI!")

# Check which model.py and API URL are loaded
with st.expander("Connection Information"):
    st.write("Loaded model file:", model.__file__)
    st.write("Current API URL:", model.API_URL)

# Language selection
language = st.selectbox(
    "Choose Language",
    ["English", "Telugu", "Kannada", "Hindi"]
)

# Genre selection
genre = st.selectbox(
    "Choose Story Genre",
    ["Mystery", "Horror", "Fantasy", "Adventure"]
)

# Session initialization
if "story" not in st.session_state:
    st.session_state.story = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "story_title" not in st.session_state:
    st.session_state.story_title = ""

st.divider()

# Generate Story
st.header("✨ Generate Your Story")

title_labels = {
    "English": "Enter Your Story Title",
    "Telugu": "మీ కథ శీర్షికను నమోదు చేయండి",
    "Kannada": "ನಿಮ್ಮ ಕಥೆಯ ಶೀರ್ಷಿಕೆಯನ್ನು ನಮೂದಿಸಿ",
    "Hindi": "अपनी कहानी का शीर्षक दर्ज करें"
}

title = st.text_input(title_labels[language])

if st.button("Generate Story"):

    if title.strip():

        prompt = (
            f"Write a complete and engaging {genre} story in {language}. "
            f"The story title must also be in {language}. "
            f"Use this title as the topic: '{title}'. "
            f"If the supplied title is not in {language}, translate it "
            f"naturally into {language} and use that as the story title. "
            "Write a well-developed story with a clear beginning, "
            "interesting middle, strong climax and satisfying ending. "
            "Make the story coherent, creative and complete. "
            "Do not stop midway. Do not ask the user what happens next. "
            "Write only in the selected language."
        )

        with st.spinner("Generating your complete story..."):

            story = generate_story(
                language,
                genre,
                title,
                prompt
            )

        st.session_state.story = story
        st.session_state.story_title = title
        st.session_state.chat_history = []

    else:
        st.warning("Please enter a story title.")

# Display Story
if st.session_state.story:

    st.divider()

    st.subheader("📖 " + st.session_state.story_title)

    st.write(st.session_state.story)

st.divider()

# Chatbot
st.header("💬 Ask About Your Story")

if st.session_state.story:

    st.write(
        "Your story is ready! Ask any question in English, "
        "Telugu, Kannada or Hindi."
    )

    # Previous messages
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User question
    question = st.chat_input(
        "Ask anything about your story..."
    )

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        conversation = ""

        for message in st.session_state.chat_history:
            conversation += (
                message["role"] + ": "
                + message["content"] + "\n"
            )

        prompt = (
            "You are TaleNova AI, a helpful multilingual story assistant. "
            "Understand questions in English, Telugu, Kannada and Hindi. "
            "Always answer in the selected story language: "
            + language + ". "
            "Answer clearly using the given story context. "
            "Do not ask the user to paste the story again. "
            "Do not invent events that are not in the story.\n\n"

            "STORY TITLE:\n"
            + st.session_state.story_title
            + "\n\nSTORY:\n"
            + st.session_state.story
            + "\n\nCONVERSATION:\n"
            + conversation
            + "\nAssistant:"
        )

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = generate_story(
                    language,
                    genre,
                    "Story Question",
                    prompt
                )

            st.write(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

else:

    st.info(
        "First generate a story. Then you can ask questions "
        "about it using the chatbot."
    )

st.divider()

st.caption("TaleNova AI | Qwen 4B | QLoRA")

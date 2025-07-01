import streamlit as st
import nltk
import numpy as np

nltk.download('punkt')


def preprocess_essay(essay):
    words = nltk.word_tokenize(essay.lower())
    sentences = nltk.sent_tokenize(essay)
    words = [word for word in words if word.isalpha()]
    return words, sentences

def vocabulary_richness(words):
    unique_words = set(words)
    return len(unique_words), len(words)

def average_sentence_length(sentences):
    sentence_lengths = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
    return np.mean(sentence_lengths) if sentence_lengths else 0

def extract_insights(essay, words, sentences):
    unique_words = set(words)
    longest_sentence = max(sentences, key=lambda x: len(nltk.word_tokenize(x)), default="")
    shortest_sentence = min(sentences, key=lambda x: len(nltk.word_tokenize(x)), default="")
    return {
        'keywords': list(unique_words),
        'longest_sentence': longest_sentence,
        'shortest_sentence': shortest_sentence
    }

def score_essay(essay):
    words, sentences = preprocess_essay(essay)
    vocab_unique, vocab_total = vocabulary_richness(words)
    avg_sentence_len = average_sentence_length(sentences)
    essay_len = len(essay)
    
    # Heuristic scoring
    score = 0
    if vocab_total > 0:
        score += (vocab_unique / vocab_total) * 30
    score += avg_sentence_len * 2
    score += essay_len / 100
    score = min(max(score, 0), 100)

    return score, vocab_unique, vocab_total, avg_sentence_len, words, sentences

# ----- Streamlit UI -----

st.markdown(
    """
    <style>
    .stApp {
        background-color: #255363;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.set_page_config(page_title="Essay Scorer", layout="centered")
st.title("📝 Essay Scoring App")

# Custom CSS for input box styling
st.markdown("""
    <style>
    input, textarea {
        background-color: #ebe7d5 !important;  
        color: #000000 !important;       
        caret-color: #000000 !important;
        border-radius: 10px;
        padding: 8px;
    }
    </style>
""", unsafe_allow_html=True
)

essay_input = st.text_area("Enter your essay below:", height=300)

st.markdown("""
    <style>
    button:hover {
        background-color: #00ffcc !important;
        color: black !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True
)

if st.button("Analyze Essay"):
    if essay_input.strip() == "":
        st.warning("Please enter a valid essay.")
    else:
        score, vocab_unique, vocab_total, avg_sentence_len, words, sentences = score_essay(essay_input)
        insights = extract_insights(essay_input, words, sentences)

        st.subheader("📊 Analysis Results")
        st.markdown(f"**Score:** `{score:.2f} / 100`")
        st.markdown(f"**Unique Words:** `{vocab_unique}`")
        st.markdown(f"**Total Words:** `{vocab_total}`")
        st.markdown(f"**Average Sentence Length:** `{avg_sentence_len:.2f}` words")
        st.markdown("**Keywords:** " + ", ".join(insights['keywords'][:10]))  # limit keywords

        with st.expander("📌 Longest Sentence"):
            st.write(insights['longest_sentence'])

        with st.expander("📌 Shortest Sentence"):
            st.write(insights['shortest_sentence'])



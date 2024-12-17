import streamlit as st
from difflib import SequenceMatcher
import docx
import PyPDF2
import chardet
import nltk
from nltk.corpus import wordnet as wn
from textstat import textstat

nltk.download('wordnet')
nltk.download('omw-1.4')

st.set_page_config(page_title="integrity scanner", page_icon=":cherry_blossom:", layout="wide")

def calculate_similarity(text1, text2):
    """Calculate similarity percentage between two texts."""
    text1 = text1.lower()
    text2 = text2.lower()
    return SequenceMatcher(None, text1, text2).ratio() * 100

def read_docx(file_path):
    """Read content from a .docx file."""
    doc = docx.Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)

def read_pdf(file_path):
    """Read content from a .pdf file."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def read_text_file(file_path):
    """Read a text file with encoding detection."""
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] if result['encoding'] else 'utf-8'
    with open(file_path, "r", encoding=encoding) as file:
        return file.read()


def find_synonyms(text1, text2):
    """Find synonym matches between two texts using WordNet."""
    words1 = set(text1.split())
    words2 = set(text2.split())
    synonym_matches = []

    for word1 in words1:
        synsets1 = wn.synsets(word1)
        if not synsets1:
            continue  

        for word2 in words2:
            if word1.lower() == word2.lower():
                continue  

            synsets2 = wn.synsets(word2)
            if not synsets2:
                continue  

            for syn1 in synsets1:
                for syn2 in synsets2:
                    if set(lemma.name().lower() for lemma in syn1.lemmas()) & set(
                        lemma.name().lower() for lemma in syn2.lemmas()
                    ):
                        synonym_matches.append((word1, word2))
                        break  

    return synonym_matches

def get_readability_score(text):
    """Calculate the Flesch-Kincaid readability score."""
    return textstat.flesch_kincaid_grade(text)

st.markdown("<h1 style='text-align: center;'>IS : Integrity Scanner Pro Max</h1>",
            unsafe_allow_html=True)

st.markdown(
    "<h5 style='text-align: center; font-style: italic; color: #dcdbdd; '>[the 100% legit OG checker.]</h4>",
    unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid #a570ff;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="border:2px solid #bb93ff; padding: 20px; border-radius: 10px;">
            <h3 style="text-align: center;"> TEXT 1</h3>
            <p style="text-align: center;">Upload a file or enter text manually.</p>
    """, unsafe_allow_html=True)
    uploaded_file1 = st.file_uploader("Choose the first file", type=["txt", "pdf", "docx"])
    text_input1 = st.text_area("Or type the first text here", height=150)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="border:2px solid #bb93ff; padding: 20px; border-radius: 10px;">
            <h3 style="text-align: center;"> TEXT 2</h3>
            <p style="text-align: center;">Upload a file or enter text manually.</p>
    """, unsafe_allow_html=True)
    uploaded_file2 = st.file_uploader("Choose the second file", type=["txt", "pdf", "docx"])
    text_input2 = st.text_area("Or type the second text here", height=150)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            height: 3em;
            font-size: 20px;
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Compare Texts"):
    if uploaded_file1 is not None:
        file_extension1 = uploaded_file1.name.split('.')[-1]
        file_content1 = ""

        if file_extension1 == "docx":
            file_content1 = read_docx(uploaded_file1)
        elif file_extension1 == "pdf":
            file_content1 = read_pdf(uploaded_file1)
        elif file_extension1 == "txt":
            file_content1 = read_text_file(uploaded_file1)
    elif text_input1:
        file_content1 = text_input1
    else:
        file_content1 = ""

    if uploaded_file2 is not None:
        file_extension2 = uploaded_file2.name.split('.')[-1]
        file_content2 = ""

        if file_extension2 == "docx":
            file_content2 = read_docx(uploaded_file2)
        elif file_extension2 == "pdf":
            file_content2 = read_pdf(uploaded_file2)
        elif file_extension2 == "txt":
            file_content2 = read_text_file(uploaded_file2)
    elif text_input2:
        file_content2 = text_input2
    else:
        file_content2 = ""

    if file_content1 and file_content2:
        similarity = calculate_similarity(file_content1, file_content2)

        if similarity >= 75:
            similarity_color = "#ff7878"
        elif similarity >= 50:
            similarity_color = "#f6c663"
        elif similarity >= 25:
            similarity_color = "#f0f161"
        else:
            similarity_color = "#9cf169"

        st.markdown("<h3 style='text-align: center;'>Similarity between the two texts:</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align: center; font-size: 50px; width: 200px; height: 200px; border-radius: 50%; border: 10px solid {similarity_color}; color: {similarity_color}; line-height: 200px; position: relative; margin: 0 auto;">
                <span style="font-size: 45px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">{similarity:.2f}<sup style="font-size: 0.4em;">%</sup></span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 2px solid #a570ff;'>", unsafe_allow_html=True)

        synonym_matches = find_synonyms(file_content1, file_content2)
        if synonym_matches:
            st.markdown("<h3 style='text-align: center; color: #bb93ff;'>Synonym Matches:</h3>", unsafe_allow_html=True)
            synonym_data = [(match[0], match[1]) for match in synonym_matches]
            st.table(synonym_data)
        else:
            st.markdown("<h3 style='text-align: center;'>No synonym matches found.</h3>", unsafe_allow_html=True)

        readability_score1 = get_readability_score(file_content1)
        readability_score2 = get_readability_score(file_content2)
        st.markdown("<h3 style='text-align: center; color: #bb93ff;'>Readability Scores:</h3>", unsafe_allow_html=True)
        readability_data = {
            "Text": ["Text 1", "Text 2"],
            "Readability Score (Flesch-Kincaid Grade Level)": [readability_score1, readability_score2]
        }
        st.table(readability_data)
    else:
        st.warning("Please provide both texts to compare (either upload files or type text).")

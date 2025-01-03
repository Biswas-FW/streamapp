import streamlit as st
import nltk
import pandas as pd
from collections import Counter
import string
from deep_translator import GoogleTranslator

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Function to process titles
def process_titles(titles):
    word_counter = Counter()
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    for title in titles:
        words = word_tokenize(title)
        words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuation]
        word_counter.update(words)

    top_1000_words = word_counter.most_common(1000)
    translator = GoogleTranslator(source='auto', target='en')
    translations = [(word, translator.translate(word), freq) for word, freq in top_1000_words]

    return translations

# Streamlit app layout
st.title('Data Processing and Translation App')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    titles = data.iloc[:, 0].dropna().tolist()  # Assuming the titles are in the first column
    translations = process_titles(titles)
    
    top_1000_df = pd.DataFrame(translations, columns=['Word', 'Translation', 'Frequency'])
    st.write(top_1000_df)
    
    csv = top_1000_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Sample.csv',
        mime='text/csv',
    )

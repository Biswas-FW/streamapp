import nltk

# Ensure required resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  # Add this line to avoid missing resource

import streamlit as st
from collections import Counter
import string
from deep_translator import GoogleTranslator
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

# Text box to input titles
titles_input = st.text_area("Paste your titles here (CSV format)", height=200)

if titles_input:
    # Split the pasted input by newlines (simulating CSV rows)
    titles = [line.strip() for line in titles_input.split("\n") if line.strip()]

    # Process titles
    translations = process_titles(titles)

    # Create a DataFrame for the top 1000 words
    top_1000_df = pd.DataFrame(translations, columns=['Word', 'Translation', 'Frequency'])
    st.write(top_1000_df)
    
    # Provide the option to download the processed data as CSV
    csv = top_1000_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Sample.csv',
        mime='text/csv',
    )

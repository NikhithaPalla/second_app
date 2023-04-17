import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt
from nltk import FreqDist


st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not a list)
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

# Sidebar
st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider("Max Words",min_value=10, max_value=200, value=100)
largest_word = st.sidebar.slider("Size of largest word", min_value=50, max_value=350, value=60)
Image_width = st. sidebar.slider("Image Width", min_value=100, max_value=800, value=400)
random_state = st.sidebar.slider("Random state", min_value=20, max_value=100, value=20)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?",value=True)
st.sidebar.header('Word Count Settings')
min_count = st.sidebar.slider("Minimum count of words",min_value=5, max_value=100, value=40)

## Select text files
image = st.selectbox("Choose a text file", books.keys())

## Get the value
image = books.get(image)


if image != " ":
    stop_words = []
    raw_text = open(image,"r").read().lower()
    nltk_stop_words = stopwords.words('english')

    if remove_stop_words:
        stop_words = set(nltk_stop_words)
        stop_words.update(['us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','thou'])
        # These are all lowercase

    tokens = nltk.word_tokenize(raw_text)
    
tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    if image != " ":
        wordcloud = WordCloud(max_words=max_word, background_color="white", width= Image_width, max_font_size= largest_word, random_state=random_state).generate(raw_text)
        plt.figure(figsize=(10,10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)
    
    
with tab2:
    st.write('Bar Chart')
    if image != " ": 
     words = [word for word in tokens if word.isalpha() and word not in stop_words]
     freqDist = FreqDist(words)
     top_words = freqDist.most_common()
        # Create a dataframe
     df = pd.DataFrame(top_words, columns=[ 'word','frequency'])
     df = df[df['frequency'] >= min_count]
        #bar chart
     chart = alt.Chart(df).mark_bar().encode( x='frequency', y=alt.Y('word', sort='-x'), tooltip= ('word', 'frequency'))
     chart


     
with tab3:
    if image != " ":
        raw_text = open(image,"r").read().lower()
        st.write(raw_text)
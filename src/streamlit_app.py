import pandas as pd
import streamlit as st

st.title("SLAVA Platform: Visualizing Parsed Data")

uploaded_file = st.file_uploader("Upload processed CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview:")
    st.write(df.head())

    st.write("### Condition Texts:")
    st.write(df["condition_text"].sample(5))

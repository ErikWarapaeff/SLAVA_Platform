import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.core.metrics import MetricsCalculator

st.title('SLAVA: Analytics Platform')

def load_data(uploaded_csv_dataset):
    """Load response dataset"""
    dataset = pd.read_csv(uploaded_csv_dataset)
    return dataset

st.sidebar.subheader("Загрузите датасет c ответами модели")

uploaded_csv_dataset = st.sidebar.file_uploader("Выберите файл CSV", type=["csv"])

if uploaded_csv_dataset is not None:
    dataset = load_data(uploaded_csv_dataset)

    st.title('Анализ данных')

    id_filter = st.text_input('Введите ID для поиска:', '')

    if id_filter:
        try:
            id_filter = int(id_filter)
            filtered_df = dataset[dataset['id'] == id_filter]
            if not filtered_df.empty:
                st.write(f"Найдено {len(filtered_df)} записей для ID {id_filter}")
                st.dataframe(filtered_df, width=1000, height=125)
            else:
                st.write(f"Записи с ID {id_filter} не найдены.")
        except ValueError:
            st.write("Пожалуйста, введите числовой ID.")
    else:
        st.write("Введите ID, чтобы найти конкретные примеры.")
    
    st.subheader("Графики распределения")

    if st.button('График распределения по subject'):
        plt.figure(figsize=(8, 5))
        sns.countplot(x='subject', data=dataset)
        plt.title('Распределение по предметам')
        plt.xlabel('Subject')
        plt.ylabel('Count')
        st.pyplot(plt)

    if st.button('График распределения по provoc_score'):
        plt.figure(figsize=(8, 5))
        sns.histplot(dataset['provoc_score'], kde=True, bins=5)
        plt.title('Распределение по Provoc Score')
        plt.xlabel('Provoc Score')
        plt.ylabel('Frequency')
        st.pyplot(plt)

    metrics_calculator = MetricsCalculator(dataset)
    
    metrics_table = metrics_calculator._get_renamed_metrics_table()

    st.dataframe(metrics_table, width=1000, height=125)

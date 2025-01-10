import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

from src.core.metrics import MetricsCalculator
from src.core.visualize import (
    calculate_block_average,
    calculate_block_min,
    calculate_block_max,
    plot_subject_distribution,
    plot_provoc_score_distribution,
    plot_average_metrics,
    plot_min_max_values,
    plot_embeddings_comparison,
    plot_boxplot_with_separation_lines
)

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
        
    metrics_calculator = MetricsCalculator(dataset)
    
    # Получаем таблицу метрик
    metrics_table = metrics_calculator._get_renamed_metrics_table()

    st.dataframe(metrics_table, width=1000, height=125)
    
    st.subheader("Графики распределения")

    # Описание графика распределения по subject
    st.markdown("""
    **График распределения по предметам**  
    Этот график отображает распределение записей по разным предметам (subject). 
    Он помогает увидеть, какие предметы преобладают в наборе данных, и позволяет сравнить количество записей для каждого предмета. 
    График полезен для выявления наиболее популярных или частых категорий предметов и может использоваться для дальнейшего анализа данных по этим категориям.
    """)

    # График распределения по subject
    flg = plot_subject_distribution(dataset)
    st.pyplot(flg)

    # Описание графика распределения по provoc_score
    st.markdown("""
    **График распределения по Provoc Score**  
    Этот график показывает распределение провокационного индекса (provoc_score) для всех записей. 
    Провокационный индекс может отражать степень провокационности или вызываемости ответов модели, что является важным для анализа того, как модель реагирует на различные типы вопросов. 
    График помогает понять, какие уровни провокации преобладают в ответах модели, а также выявить возможные закономерности или аномалии.
    """)

    # График распределения по provoc_score
    flg = plot_provoc_score_distribution(dataset)
    st.pyplot(flg)


    # Описание графика средних значений по блокам
    st.markdown("""
    **График средних значений по блокам**  
    Этот график отображает средние значения для различных блоков данных, таких как Subject (предмет), Provocativeness (провокационность) и Type of Question (тип вопроса). 
    Средние значения дают представление о центральной тенденции для каждой из категорий и могут быть использованы для сравнения различных блоков. 
    График позволяет быстро увидеть, как различные категории отличаются по своим средним показателям.
    """)
    
    # Визуализация: Средние значения по блокам
    flg = plot_average_metrics(metrics_table)
    st.pyplot(flg)

    # Описание графика минимальных и максимальных значений
    st.markdown("""
    **График минимальных и максимальных значений по блокам**  
    На этом графике визуализированы минимальные и максимальные значения для каждого блока. Минимальные значения отображаются красным цветом, а максимальные — зелёным. 
    Это позволяет легко выделить диапазон значений для каждого блока и выявить возможные выбросы или аномалии в данных. 
    Такой график полезен для анализа экстремальных значений и понимания их влияния на общий набор данных.
    """)
    
    subject_min = calculate_block_min(metrics_table, 'Subject')
    provocativeness_min = calculate_block_min(metrics_table, 'Provocativeness')
    type_question_min = calculate_block_min(metrics_table, 'Type of question')
    
    subject_max = calculate_block_max(metrics_table, 'Subject')
    provocativeness_max = calculate_block_max(metrics_table, 'Provocativeness')
    type_question_max = calculate_block_max(metrics_table, 'Type of question')

    # Вывод минимальных значений
    st.write(f"Минимальное значение по Subject: {subject_min}")
    st.write(f"Минимальное значение по Provocativeness: {provocativeness_min}")
    st.write(f"Минимальное значение по Type of Question: {type_question_min}")
    
    st.write(f"Максимальное значение по Subject: {subject_max}")
    st.write(f"Максимальное значение по Provocativeness: {provocativeness_max}")
    st.write(f"Максимальное значение по Type of Question: {type_question_max}")

    # Визуализация: Минимальные и максимальные значения по блокам
    flg = plot_min_max_values(metrics_table)
    st.pyplot(flg)
    
    st.markdown("""
    **График Boxplot с линиями раздела по категориям**  
    Этот график представляет собой **boxplot** (или ящико-усовый график), который используется для отображения распределения значений по различным категориям. Он помогает визуализировать медиану, квартили, а также возможные выбросы в данных.

    Особенности графика:
    - **Ящики** (box) показывают диапазон между первым (25-й перцентиль) и третьим (75-й перцентиль) квартили, а линия внутри ящика указывает медиану (50-й перцентиль).
    - **Усы** (whiskers) показывают диапазон данных, который не выходит за пределы 1,5*IQR (межквартильного размаха) от первого и третьего квартилей. Все значения за пределами этих усов считаются выбросами.
    - **Линии раздела** (separation lines) добавлены для выделения различных категорий в данных. Эти линии помогают увидеть, как различные группы данных (например, по категориям или меткам) различаются по своим меткам или показателям.

    Этот график позволяет:
    - Легко сравнивать распределения различных категорий данных.
    - Идентифицировать выбросы и аномалии.
    - Получить представление о центре данных и их разбросе для каждой категории.

    Таким образом, **boxplot с линиями раздела** является мощным инструментом для анализа данных, где важен визуальный контекст распределений по группам.
    """)
    
    # Визуализация: Boxplot с линиями раздела
    flg = plot_boxplot_with_separation_lines(metrics_table)
    st.pyplot(flg)

    # Описание графика эмбеддингов
    st.markdown("""
    **График эмбеддингов ответов модели и правильных ответов**  
    Этот график отображает визуализацию эмбеддингов ответов модели и правильных ответов с помощью метода PCA (Principal Component Analysis), который используется для снижения размерности данных до двух измерений. 
    Снижение размерности помогает упростить визуализацию многомерных данных, таких как векторные представления текста. 
    График позволяет увидеть, как близки ответы модели к правильным ответам, а также оценить качество эмбеддингов и способность модели различать правильные и неправильные ответы.
    """)

    # Визуализация: Эмбеддинги
    flg = plot_embeddings_comparison(dataset)
    st.pyplot(flg)

    
    



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Функции для вычисления статистик по блокам
def calculate_block_average(df, block_keyword):
    block_cols = [col for col in df.columns if block_keyword in col]
    return df[block_cols].mean(axis=1).values[0]

def calculate_block_min(df, block_keyword):
    block_cols = [col for col in df.columns if block_keyword in col]
    return df[block_cols].min(axis=1).values[0]

def calculate_block_max(df, block_keyword):
    block_cols = [col for col in df.columns if block_keyword in col]
    return df[block_cols].max(axis=1).values[0]

def plot_subject_distribution(dataset):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='subject', data=dataset, ax=ax)
    ax.set_title('Распределение по предметам')
    ax.set_xlabel('Subject')
    ax.set_ylabel('Count')
    plt.tight_layout()
    return fig

def plot_provoc_score_distribution(dataset):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(dataset['provoc_score'], kde=True, bins=5, ax=ax)
    ax.set_title('Распределение по Provoc Score')
    ax.set_xlabel('Provoc Score')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig

def plot_average_metrics(metrics_table):
    subject_avg = calculate_block_average(metrics_table, 'Subject')
    provocativeness_avg = calculate_block_average(metrics_table, 'Provocativeness')
    type_question_avg = calculate_block_average(metrics_table, 'Type of question')

    overall_average = (subject_avg + provocativeness_avg + type_question_avg) / 3

    averages = {
        'Subject': subject_avg,
        'Provocativeness': provocativeness_avg,
        'Type of Question': type_question_avg,
        'Overall Average': overall_average
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b3']
    sns.barplot(x=list(averages.keys()), y=list(averages.values()), palette=bar_colors, ax=ax)

    ax.set_title('Средние значения по блокам', fontsize=16)
    ax.set_ylabel('Среднее значение', fontsize=12)
    ax.set_xlabel('Блок', fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    for i, value in enumerate(averages.values()):
        ax.text(i, value + 0.01, f"{value:.2f}", ha='center', fontsize=10)

    plt.tight_layout()
    return fig

def plot_min_max_values(metrics_table):
    fig, ax = plt.subplots(1, 3, figsize=(22, 8), sharey=True)

    blocks = ['Subject', 'Provocativeness', 'Type of question']

    for i, block in enumerate(blocks):
        block_cols = [col for col in metrics_table.columns if block in col]
        block_values = metrics_table[block_cols].iloc[0]

        min_value = block_values.min()
        max_value = block_values.max()
        min_indices = [j for j, val in enumerate(block_values) if val == min_value]
        max_indices = [j for j, val in enumerate(block_values) if val == max_value]

        bars = ax[i].bar(block_cols, block_values, color='lightblue', label='Значения')

        for idx in max_indices:
            bars[idx].set_color('green')
        for idx in min_indices:
            bars[idx].set_color('red')

        ax[i].set_title(f'{block}', fontsize=14)
        ax[i].set_xticks(range(len(block_cols)))
        ax[i].set_xticklabels(block_cols, rotation=45, ha='right', fontsize=10)

    legend_elements = [
        plt.Line2D([0], [0], color='green', lw=4, label='Максимумы'),
        plt.Line2D([0], [0], color='red', lw=4, label='Минимумы'),
        plt.Line2D([0], [0], color='lightblue', lw=4, label='Значения'),
    ]
    fig.legend(handles=legend_elements, loc='upper center', ncol=3, fontsize=12, bbox_to_anchor=(0.5, 0.9))

    fig.suptitle('Минимальные и максимальные значения по метрикам', fontsize=16)
    plt.tight_layout(pad=3.0, rect=[0, 0, 1, 0.95])
    return fig


def plot_embeddings_comparison(dataset):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    df = dataset.query('type == "открытый ответ"')
    model_embeddings = model.encode(df['response'].tolist())
    correct_embeddings = model.encode(df['outputs'].tolist())

    pca = PCA(n_components=2)
    pca_model = pca.fit_transform(model_embeddings)
    pca_correct = pca.transform(correct_embeddings)

    df_embeddings = pd.DataFrame(pca_model, columns=['PC1', 'PC2'])
    df_embeddings['Correct'] = 'Model Response'
    df_correct_embeddings = pd.DataFrame(pca_correct, columns=['PC1', 'PC2'])
    df_correct_embeddings['Correct'] = 'Correct Answer'

    df_combined = pd.concat([df_embeddings, df_correct_embeddings], ignore_index=True)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df_combined, x='PC1', y='PC2', hue='Correct', style='Correct', palette='Set1', markers=['o', 'X'])
    plt.title('Сравнение эмбеддингов ответов модели и правильных ответов')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.legend(title='Тип ответа')
    plt.tight_layout()
    return plt.gcf()

def plot_boxplot_with_separation_lines(metrics_table):
    df = metrics_table.drop(columns=['model'])
    df_melted = df.melt(var_name='Metric', value_name='Value')

    categories = ['PM', 'IS', 'EM', 'F1', 'LR']
    
    df_melted['Category'] = df_melted['Metric'].apply(
        lambda x: next((cat for cat in categories if cat in x), 'Other')
    )

    df_melted['Category'] = pd.Categorical(df_melted['Category'], categories=categories, ordered=True)
    df_melted = df_melted.sort_values(by=['Category', 'Value'])

    plt.figure(figsize=(12, 10))
    sns.boxplot(data=df_melted, x='Category', y='Value', hue='Category', dodge=False, showfliers=False, palette='coolwarm')
    sns.lineplot(data=df_melted, x='Category', y='Value', color='black', linewidth=2, marker='o', markersize=8)
    plt.title('Boxplot распределения по категориям')
    plt.tight_layout()
    return plt.gcf()
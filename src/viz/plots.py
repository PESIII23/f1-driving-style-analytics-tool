import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar_chart(df, numeric_col, category_col, ylabel: str, title=None):
    """
    Plots a bar chart showing the mean of a numeric column grouped by a categorical column.
    """

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=category_col, y=numeric_col, hue=category_col, dodge=False)
    plt.title(title if title else f"Mean {numeric_col} by {category_col}")
    plt.xlabel(category_col)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()
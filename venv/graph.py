import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from shutil import rmtree
import constant


def plot_game_stats(filename: str):
    """
    Specifies specifc plots for various measurements/statistics from game
    :param filename: filename with data
    """
    df = pd.read_csv(filename, delimiter=',', header=0)

    if 'Steps' in df:
        steps = df['Steps']
        img = 'eta' + str(constant.ETA) + '_steps'
        line_plot(steps, save_img=img, plot_title='Training Steps', x_label='Episodes', y_label='Steps')

    if 'Score' in df:
        score = df['Score']
        img = 'eta' + str(constant.ETA) + '_score'
        scatterplot(score, save_img=img, plot_title='Training Scores', x_label='Episodes', y_label='Scores')


def scatterplot(df, save_img: str, plot_title: str, x_label: str, y_label: str):
    """
    Creates a scatterplot from the dataframe
    :param df: the dataframe to be plotted
    :param save_img: image name for saving
    :param plot_title: plot's title name
    :param x_label: x-axis's label
    :param y_label: y-axis's label
    """
    sns.set(style='white')
    ax = sns.relplot(data=df, legend='full', size='size')
    ax.set(xlabel=x_label, ylabel=y_label, title=plot_title)
    save_plot(title=save_img, clear_dir=constant.DELETE_GRAPHS)
    plt.show()


def line_plot(df, save_img: str, plot_title: str, x_label: str, y_label: str):
    """
    Creates a line plot from the dataframe
    :param df: the dataframe to be plotted
    :param save_img: image name for saving
    :param plot_title: plot's title name
    :param x_label: x-axis's label
    :param y_label: y-axis's label
    """
    sns.set(style='whitegrid', rc={"lines.linewidth": 0.3})
    sns.set_palette(sns.color_palette("RdBu_r", 5))
    ax = sns.lineplot(data=df, legend='full')
    ax.set(xlabel=x_label, ylabel=y_label, title=plot_title, xlim=(0, len(df)), ylim=(0, max(df)))
    save_plot(title=save_img, clear_dir=constant.DELETE_GRAPHS)
    plt.show()


def save_plot(title: str, clear_dir: bool):
    """
    Saves plot to specified directory.
    :param clear_dir: if True, the directory and its contents will be removed, if False, nothing is explicitly removed
    """
    path = constant.GRAPH_DIR

    # clear directory if specified by function call
    if clear_dir and os.path.exists(path):
        rmtree(path)

    # create directory if it doesn't exist
    if not os.path.exists(path):
        os.mkdir(path)

    # save plot to specified directory
    img = path + title + '.png'
    plt.savefig(img)


if __name__ == "__main__":
    game_stats_file = constant.DATA_DIR + 'data.csv'  # TODO: hardcoded filename for now
                                                      # TODO: figure out better implmentation if multiple files
    plot_game_stats(game_stats_file)

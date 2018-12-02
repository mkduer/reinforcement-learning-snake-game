import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from shutil import rmtree
import constant
from numpy import arange as arr


def plot_game_stats(filename: str, test_run: bool=False):
    """
    Specifies specifc plots for various measurements/statistics from game
    :param filename: filename with data
    :param test_run: True if the data is from a test run, False otherwise
    """
    df = pd.read_csv(filename, delimiter=',', header=0)
    specs = ['Steps', 'Scores']
    print(f'df exists: {df}')

    for s in specs:
        title = 'Training'
        if test_run:
            title = 'Testing'

        if s in df:
            img = constant.PARAM + str(constant.PARAM_VAL) + '_' + s
            if test_run:
                img += '_testing'
            title += ' Run with ' + s + ' (' + constant.PARAM + ' = ' + str(constant.PARAM_VAL) + ')'

            if s == 'Steps':
                steps = df[s]
                line_plot(steps, img, title, x_label='Episodes', y_label=s)
            if s == 'Scores':
                score = df[s]
                scatterplot(score, img, title, x_label='Episodes', y_label=s)


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
    ax.set(xlabel=x_label, ylabel=y_label, title=plot_title, xticks=arr(0, constant.EPISODES + 1, 50000))
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
    :param title: title of plot
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
    plt.savefig(img, bbox_inches='tight', pad_inches=0.25)


if __name__ == "__main__":

    if constant.PARAM_TEST:
        test_name = constant.PARAM + str(constant.PARAM_VAL)
        game_stats_file = constant.DATA_DIR + test_name + '_data.csv'
        plot_game_stats(game_stats_file)
    else:
        test_name = 'testing_' + constant.PARAM + str(constant.PARAM_VAL)
        game_stats_file = constant.DATA_DIR + test_name + '_data.csv'
        plot_game_stats(game_stats_file, True)

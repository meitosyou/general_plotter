import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import calendar
import sys


class GeneralPlotter:
    def __init__(self):
        '''
        Parameters
        ----------
        '''        
        self.fig, self.ax = plt.subplots()
        
    def plot_xy(self, data_x, data_y):
        self.ax.plot(data_x, data_y)
        self.fig.show()

    def plot_hist(self, data_x, ylog=False):
        self.ax.hist(data_x)
        if ylog:
            self.ax.set_yscale('log')
        self.fig.show()

    def plot_bar(self, data_x, data_y):
        self.ax.bar(data_x, data_y, width=0.3)
        self.fig.show()

    def plot_graph(self, data_x, data_y):
        self.ax.plot(data_x, data_y)
        self.fig.show()
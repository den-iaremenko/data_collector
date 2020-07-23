import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
import pandas as pd

from datetime import datetime



def create_plot(name):
    p = figure(x_axis_type="datetime", title=name)
    p.grid.grid_line_alpha = 0.5
    p.width = 2000
    p.height = 800
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    return p

def create_chart_nbu():
    data_to_show = pd.read_csv("nbu.csv")

    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    # NBU
    p1 = create_plot("NBU")
    p1.line(datetime(list(data_to_show["h_t"])), list(data_to_show["e"]),
            color='#A6CEE3', line_width=3, legend_label='Euro')
    p1.line(datetime(list(data_to_show["h_t"])), list(data_to_show["d"]),
            color='#B2DF8A', line_width=3, legend_label='Dollar')

    # UKRSIB
    p2 = create_plot("Ukrsib")
    p2.line(datetime(list(data_to_show["h_t"])), list(data_to_show["e"]),
            color='#A6CEE3', line_width=3, legend_label='Euro')
    p2.line(datetime(list(data_to_show["h_t"])), list(data_to_show["d"]),
            color='#B2DF8A', line_width=3, legend_label='Dollar')


    output_file("nbu.html")
    show(gridplot([[p1], [p2]]))

create_chart_nbu()
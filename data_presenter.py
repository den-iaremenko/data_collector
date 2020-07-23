import numpy as np
import pandas as pd
import random

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from datetime import datetime



def create_plot(name):
    p = figure(x_axis_type="datetime", title=name)
    p.border_fill_color = "whitesmoke"
    p.grid.grid_line_alpha = 0.3
    p.width = 1600
    p.height = 1000
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    return p


def create_chart_nbu():
    data_to_show_nbu = pd.read_csv("nbu.csv")
    data_to_show_ukrsib = pd.read_csv("ukrsib.csv")
    data_to_show_dou = pd.read_csv("dou.csv")

    def datetime_personal(x):
        return np.array(x, dtype=np.datetime64)

    # NBU
    p1 = create_plot("NBU")
    p1.line(datetime_personal(list(data_to_show_nbu["h_t"])), list(data_to_show_nbu["e"]),
            color='#A6CEE3', line_width=3, legend_label='Euro')
    p1.line(datetime_personal(list(data_to_show_nbu["h_t"])), list(data_to_show_nbu["d"]),
            color='#B2DF8A', line_width=3, legend_label='Dollar')
    p1.legend.location = "top_left"
    p1.legend.click_policy = "hide"

    # UKRSIB
    p2 = create_plot("Ukrsib")
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["e_b"]),
            color='yellow', line_width=3, legend_label='Euro Buy')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["e_s"]),
            color='yellow', line_dash="dashed", line_width=3, legend_label='Euro Sell')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["d_b"]),
            color='green', line_width=3, legend_label='Dollar Buy')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["d_s"]),
            color='green', line_dash="dashed", line_width=3, legend_label='Dollar Sell')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["e_card_s"]),
            color='red', line_width=3, legend_label='Euro Card Buy')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["e_card_b"]),
            color='red', line_dash="dashed", line_width=3, legend_label='Euro Card Sell')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["d_card_s"]),
            color='brown', line_width=3, legend_label='Dollar Card Buy')
    p2.line(datetime_personal(list(data_to_show_ukrsib["h_t"])), list(data_to_show_ukrsib["d_card_b"]),
            color='brown', line_dash="dashed", line_width=3, legend_label='Dollar Card Sell')
    p2.legend.location = "top_left"
    p2.legend.click_policy = "hide"

    # DOU
    def random_color():
        return tuple(np.random.randint(256, size=3))

    p3 = create_plot("Dou")
    p3.yaxis.axis_label = "Number"
    for item in data_to_show_dou.columns.values.tolist()[2:]:
        p3.line(datetime_personal(list(data_to_show_dou["h_t"])), list(data_to_show_dou[item]),
                color=random_color(), line_width=3, legend_label=item)
    p3.legend.location = "top_left"
    p3.legend.click_policy = "hide"

    output_file("current_data.html")
    show(gridplot([[p1], [p2], [p3]]))


create_chart_nbu()

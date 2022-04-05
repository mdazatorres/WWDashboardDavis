#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 17:37:42 2022

@author: marialuisa
"""

# import pandas as pd
import numpy as np
# import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import trim_mean, pearsonr
from sklearn.linear_model import LinearRegression


fontsize = 14


def plotN(city_data, loc_data, log, opt, size_window, center, lag):  # normalizado
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    nn = loc_data.SampleDate.shape[0]
    mm = city_data.SampleDate.shape[0]
    x = loc_data.SampleDate[:nn - lag]
    name = 'N/PMMoV (influent)'  # + ' (' + str(city_data.Type.unique()[0]) + ')'
    name_ = 'City-wide average N/PMMoV (influent)'
    cases = False
    size_loc=25
    if opt == 'Moving average':
        fig.add_trace(go.Scatter(name=name, mode='lines', x=x,
                                 y=loc_data['NormalizedConc'].rolling(window=size_window, center=center).mean()[ :nn - lag],
                                 line=dict(color='black', width=3)), secondary_y=False, )

        fig.add_trace(go.Scatter(name=name_, mode='lines', x=city_data.SampleDate[:mm - lag],
                                 y=city_data['NormalizedConc'].rolling(window=size_window, center=center).mean()[:mm - lag]/size_loc, line=dict(color='gray', width=3)), secondary_y=False, )
        if cases:
            fig.add_trace(go.Scatter(name='Cases', mode='lines', x=x, y=loc_data['positives'].rolling(window=size_window, center=center).mean()[lag:],
                                     line=dict(color='gray', width=3)), secondary_y=True, )

    elif opt == 'Trimmed average':  # .apply(lambda x: trim_mean(x, 0.2))
        fig.add_trace(go.Scatter(name=name, mode='lines', x=x,
                                 y=loc_data['NormalizedConc'][:nn - lag].rolling(window=size_window, center=center).apply(lambda x: trim_mean(x, 1 / size_window)),
                                 line=dict(color='black', width=3)), secondary_y=False, )
        fig.add_trace(go.Scatter(name=name_, mode='lines', x=city_data.SampleDate[:mm - lag], y=city_data['NormalizedConc'][:mm - lag].rolling(window=size_window, center=center).apply(
                                     lambda x: trim_mean(x, 1 / size_window))/size_loc, line=dict(color='gray', width=3)), secondary_y=False, )
        if cases:
            fig.add_trace(go.Scatter(name='Cases', mode='lines', x=x, y=loc_data['positives'][lag:].rolling(window=size_window, center=center).apply(
                                         lambda x: trim_mean(x, 1 / size_window)), line=dict(color='gray', width=3)), secondary_y=True, )
    else:
        fig.add_trace(go.Scatter(name=name, mode='lines+markers', x=x, y=loc_data['NormalizedConc'][:nn - lag],
                                 marker=dict(color='black', size=8), line=dict(color='black', width=3)),
                      secondary_y=False, )
        fig.add_trace(go.Scatter(name=name_, mode='lines+markers', x=city_data.SampleDate[:mm - lag], y=city_data['NormalizedConc'][:mm - lag]/size_loc,
                                 marker=dict(color='gray', size=8), line=dict(color='gray', width=3)),
                      secondary_y=False, )
        # city_data['NormalizedConc_crude'][:nn - lag]
        # fig.update_layout(showlegend=False)
        if cases:
            fig.add_trace(go.Scatter(name='Cases', mode='lines', x=x, y=loc_data['positives'][lag:],
                                     line=dict(color='gray', width=3)), secondary_y=True, )

    if log:
        fig.update_yaxes(type="log")
        fig.update_layout(yaxis=dict(title="Log-Scale"))
    if cases:
        fig.update_yaxes(title_text="Cases", secondary_y=True)
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template="plotly_white",
                      legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.5))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
                      yaxis=dict(title='N/PMMoV'))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    fig.layout.showlegend = True
    # fig.update_layout(font_color='white', title_font_color='white')

    return fig



def plotN1N2(city_data, log, opt, size_window, center):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if opt == 'Moving average':
        fig.add_trace(go.Scatter(name='N1 gene', mode='lines', x=city_data.SampleDate,
                                 y=city_data['N1_Concentration_Merged'].rolling(window=size_window, center=center).mean(),
                                 line=dict(color='blue', width=3)), secondary_y=False,)
        fig.add_trace(go.Scatter(name='N2 gene', mode='lines', x=city_data.SampleDate,
                                 y=city_data['N2_Concentration_Merged'].rolling(window=size_window, center=center).mean(),
                                 line=dict(color='red', width=3)), secondary_y=False, )
    elif opt == 'Trimmed average':  # .apply(lambda x: trim_mean(x, 0.2))
        fig.add_trace(go.Scatter(name='N1 gene', mode='lines', x=city_data.SampleDate,
                                 y=city_data['N1_Concentration_Merged'].rolling(window=size_window, center=center).apply(
                                     lambda x: trim_mean(x, 1 / size_window)), line=dict(color='blue', width=3)), secondary_y=False, )
        fig.add_trace(go.Scatter(name='N2 gene', mode='lines', x=city_data.SampleDate,
                                 y=city_data['N2_Concentration_Merged'].rolling(window=size_window,center=center).apply(
                                     lambda x: trim_mean(x, 1 / size_window)), line=dict(color='red', width=3)), secondary_y=False, )
    else:
        fig.add_trace(go.Scatter(name='N1 gene', mode='lines+markers', x=city_data.SampleDate, y=city_data['N1_Concentration_Merged'],
                       line=dict(color='blue', width=3),marker=dict(color='blue', size=5)), secondary_y=False, )

        fig.add_trace(go.Scatter(name='N2 gene', mode='lines+markers', x=city_data.SampleDate, y=city_data['N2_Concentration_Merged'],
                       line=dict(color='red', width=3),marker=dict(color='red', size=5)), secondary_y=False, )
    if log:
        fig.update_yaxes(type="log")
        fig.update_layout(yaxis=dict(title="Logarithmic Scale"))
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template="plotly_white",
                      legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
                      yaxis=dict(title='gc/ml wastewater'))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    #fig.update_layout(font_color='white', title_font_color='white')
    return fig





def plotPMMoV(city_data, log, opt, size_window, center):
    # city_data=city_data[(city_data['SampleDate']>=start_date)&(city_data['SampleDate']<=end_date)]
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    name = 'PMMoV gc/g dry weight (influent)'

    if opt == 'Moving average':
        fig.add_trace(go.Scatter(name=name, mode='lines', x=city_data.SampleDate,
                                 y=city_data['PV_Concentration_Merged'].rolling(window=size_window, center=center).mean(),
                                 line=dict(color='green', width=3)), secondary_y=False, )
    elif opt == 'Trimmed average':
        fig.add_trace(go.Scatter(name=name, mode='lines', x=city_data.SampleDate,
                                 y=city_data['PV_Concentration_Merged'].rolling(window=size_window, center=center).apply(lambda x: trim_mean(x, 1 / size_window)),
                                 line=dict(color='green', width=3)), secondary_y=False, )
    else:

        fig.add_trace(go.Scatter(name=name, mode='lines+markers', x=city_data.SampleDate, y=city_data['PV_Concentration_Merged'], line=dict(color='green', width=3),marker = dict(color='green', size=5)), secondary_y=False, )
    if log:
        fig.update_yaxes(type="log")
        fig.update_layout(yaxis=dict(title="Log-Scale"))
    fig.layout.showlegend = True
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template="plotly_white",
                      legend_font_size=14, legend_title_font_size=fontsize)
    # fig.update_layout(autosize=False,width=500,height=250, margin=dict(l=0,r=0,b=10,t=10,pad=4),xaxis=dict(title="Date"))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.9))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4), yaxis=dict(title="gc/ml wastewater")) #"gc/ml wastewater"
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    #fig.update_layout(font_color='white', title_font_color='white')
    return fig




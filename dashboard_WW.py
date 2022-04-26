#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:51:08 2022

@author: marialuisa
"""
import pandas as pd
import numpy as np
import streamlit as st
from plot_conc import plotN1N2, plotPMMoV, plotN
from aux_function import is_authenticated, generate_login_block, clean_blocks, login


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title=None, page_icon=None)

data_ww_Davis = pd.read_csv('data_ww_Davis_loc.csv', index_col=0)
data_ww = pd.read_csv('data_ww_cases_full.csv')
localities = list(data_ww_Davis.Location.unique())[:-1]

def data_loc(loc):
    city_data = data_ww_Davis[data_ww_Davis['Location'] == loc]
    city_data = city_data.groupby('SampleDate').sum()
    city_data = city_data.reset_index()
    return city_data

def data_city(city, data_ww):
    city_data = data_ww[data_ww['City'] == city]
    city_data = city_data.reset_index()
    return city_data

city_data = data_city('Davis', data_ww)
city_data['SampleDate'] = pd.to_datetime(city_data['SampleDate'])


pc = st.get_option('theme.primaryColor')
bc = st.get_option('theme.backgroundColor')
sbc = st.get_option('theme.secondaryBackgroundColor')
tc = st.get_option('theme.textColor')

st.markdown(""" <style> .font {font-size:50px ; font-family: 'Source Sans Pro'; color: #FFFFFF;} </style> """, unsafe_allow_html=True)
st.markdown(""" <style> .font2 {font-size:20px ; font-family: 'Source Sans Pro'; color: #FFFFFF;} </style> """, unsafe_allow_html=True)


def main():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    st.markdown('<p class="font">Neighborhood Wastewater Data</p>', unsafe_allow_html=True)
    #st.header('Neighborhood Wastewater Data')
    st.sidebar.markdown('<p class="font2">SELECT A LOCATION</p>', unsafe_allow_html=True)  # --------('<p class="font">SELECT A LOCATION</p>', unsafe_allow_html=True)
    loc = st.sidebar.selectbox('', localities)
    loc_data = data_loc(loc)

    loc_data['SampleDate'] = pd.to_datetime(loc_data['SampleDate'])
    start_date = city_data['SampleDate'].min().to_pydatetime()
    end_date = city_data['SampleDate'].max().to_pydatetime()

    #st.sidebar.header('PLOT DETAILS')
    st.sidebar.markdown('<p class="font2">PLOT DETAILS</p>', unsafe_allow_html=True)
    col1, col2 = st.sidebar.columns([1, 0.51])
    #smooth = col1.selectbox('Smoothing function', ['Trimmed average', 'Moving average', 'None'], index=1)
    smooth = col1.selectbox('Smoothing function', ['Trimmed average', 'Moving average', 'None'], index=1)

    if smooth != 'None':
        size_window = col2.selectbox('Size window', [5, 7], index=1)
        center = col1.checkbox('Center')
    else:
        size_window = 0
        center = False

    log = st.sidebar.checkbox('Log transformation')
    col1, _ = st.sidebar.columns([1, 0.1])
    lag =0 # col1.slider('Lag', min_value=0, max_value=14)

   #  -------------------- Main -----------------
    col1, _= st.columns([4, 0.1])

    sl_init, sl_end = col1.slider('', min_value=start_date, max_value=end_date, value=(start_date, end_date),format='MMM DD, YYYY')

    loc_data_ = loc_data[(loc_data['SampleDate'] >= sl_init) & (loc_data['SampleDate'] <= sl_end)]
    city_data_ = city_data[(city_data['SampleDate'] >= sl_init) & (city_data['SampleDate'] <= sl_end)]
    #st.write(city_data_)

    fig1 = plotN(city_data_, loc_data_, log, smooth, size_window, center, lag=lag)
    fig2 = plotPMMoV(loc_data_, log, smooth, size_window, center)
    fig3 = plotN1N2(loc_data_, log, smooth, size_window, center)

    col1.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns([2, 2])
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

    st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
        </style>""", unsafe_allow_html=True, )


login_blocks = generate_login_block()
password = login(login_blocks)

if is_authenticated(password):
    clean_blocks(login_blocks)
    main()
elif password:
    st.info("Please enter a valid password")








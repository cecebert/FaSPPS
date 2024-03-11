import streamlit as st
import numpy as np
import pandas as pd
from functions import *


mw_tbtu=321.08
mw_hobt=135.12
mw_dipea=129.25
rho_dipea=0.76

st.set_page_config(layout="wide")

aa_df=pd.read_csv('AA table.csv')
st.header('Available aminoacids')
selected_aa=st.selectbox('Choose the aminoacid', options=aa_df['Aminoacid'])

mw_aa=aa_df[aa_df['Aminoacid']==selected_aa]['MW'].values[0]
st.write('The molecular weight (g/mol) of the aminoacid is:  ' + str(mw_aa))

st.subheader('Reactor data')

tare_syr=st.number_input('Reactor Tare (g)', min_value=0.00001, value=1., format='%.5f')
brutto_syr=st.number_input('Reactor Brutto (g)', min_value=0.00001, value=2., format='%.5f')

resin_mass_empty=brutto_syr-tare_syr

if tare_syr==brutto_syr:
    st.warning('Tare and brutto of the reactor cannot be identical, please verify your values')
else:
    
    st.success('The net mass of the resin is: '+str(resin_mass_empty)+' g')
    brutto_loaded_syr=st.number_input('Reactor Brutto after loading (g)', min_value=0.00001, value=3., format='%.5f')

    if brutto_loaded_syr==brutto_syr:
        
        st.warning('Loaded mass and brutto of the reactor cannot be identical. If they are identical something has gone wrong, please verify your values')
    else:
        resin_mass_loaded=brutto_loaded_syr-tare_syr
        st.success('The net mass of the aminoacid-loaded resin is: '+str(resin_mass_loaded)+' g')

        loading_per_g, total_loading=gravimetric_load(brutto_loaded_syr, brutto_syr, tare_syr, mw_aa)

        
        if loading_per_g<=0:
            st.warning('The loading is either zero or negative, please check your numbers')
            st.divider()
        else:
            st.write('The loading in mmol/g is : ' +str(np.round(loading_per_g, 4)))
            st.write('The total loaded mmols are : ' + str(np.round(total_loading, 4)))
            st.divider()

            st.header('Next aminoacid')
            selected_aa2=st.selectbox('Choose the aminoacid to load', options=aa_df['Aminoacid'], key='2')
            equivalents=st.number_input('Equivalents of aminoacid to load',min_value=0.01, value=1.5)

            mass_aa=equivalents*total_loading*aa_df[aa_df['Aminoacid']==selected_aa2]['MW'].values[0]
            mass_tbtu=equivalents*total_loading*mw_tbtu
            mass_hobt=equivalents*total_loading*mw_hobt
            mass_dipea=equivalents*3*total_loading*mw_dipea
            vol_dipea=mass_dipea/rho_dipea

            data_aa=np.array([mass_aa, mass_tbtu, mass_hobt, vol_dipea])
            column_names=['Mass AA (mg)', 'Mass TBTU (mg)', 'Mass HOBT (mg)', 'Volume DIPEA (ul)']
            data_df=pd.DataFrame([data_aa], columns=column_names)
            st.table(data_df)
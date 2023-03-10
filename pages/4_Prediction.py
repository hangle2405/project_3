import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(page_title='Customer Segmentation', page_icon='🍘')

kmeans_model = pickle.load(open('kmeans_model.pkl','rb'))

# GUI
st.title("Customer Segmentation Project")

st.subheader('Prediction')
with st.form('Prediction form', clear_on_submit=True):
    recency = st.number_input('Ngày mua hàng gần nhất', format = '%d', step = 1)
    frequency = st.number_input('Tổng số lần mua hàng', format = '%d', step = 1)
    monetary = st.number_input('Tổng số tiền chi tiêu ($)')
    new_df_2 = pd.DataFrame({
        'Recency' : recency,
        'Frequency' : frequency,
        'Monetary' : monetary}, index = [0])
    st.dataframe(new_df_2)
    submitted = st.form_submit_button('Predict')

    if submitted:
        st.write('#### Prediction')
        new_df = new_df_2
        y_pred = kmeans_model.predict(new_df)
        st.code("khách hàng thuộc nhóm " + str(y_pred))

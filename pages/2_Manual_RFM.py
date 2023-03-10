import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

st.set_page_config(page_title='Customer Segmentation', page_icon='🍘')

columns = ['customer_id','date','quantity','spend']
df = pd.read_fwf('CDNOW_master.txt', header=None, names=columns)
df_rfm = pd.read_csv('Data_RFM.csv')


# GUI
# Command
st.title("Customer Segmentation Project")

st.subheader('Manual FRM Analysis')
st.write('Phân nhóm thủ công dựa trên nghiệp vụ')
'---'
st.write('1. Dữ liệu thô của doanh nghiệp')
st.dataframe(df.head(5))

st.write('2. Dữ liệu sau khi biến đổi RFM ')
st.dataframe(df_rfm.head(5))

st.write('Dựa trên các giá trị RFM của từng khách hàng, ta sẽ tính điểm RFM cho khách hàng đó. Sau đó, dựa vào kiến thức nghiệp vụ tiến hành phân cụm khách hàng vào các nhóm tương ứng')

# create labels for recency, frequency and monetary
r_labels = range(4,0,-1)
f_labels = range(1,5)
m_labels = range(1,5)

# assign these labels to 4 equal percentile groups
r_groups = pd.qcut(df_rfm['Recency'].rank(method='first'), q=4, labels=r_labels)
f_groups = pd.qcut(df_rfm['Frequency'].rank(method='first'), q=4, labels=f_labels)
m_groups = pd.qcut(df_rfm['Monetary'].rank(method='first'), q=4, labels=m_labels)

# create R, F, M columns
df_rfm = df_rfm.assign(R=r_groups.values, F=f_groups.values, M=m_groups.values)

# tính toán rfm score
df_rfm['RFM_score'] = df_rfm[['R','F','M']].sum(axis=1)

def rfm_level(df):
    if (df['RFM_score'] == 12) :
        return 'STARS'
    
    elif (df['R'] == 4 and df['F'] ==1 and df['M'] == 1):
        return 'NEW'
    
    else:     
        if df['M'] == 4:
            return 'BIG SPENDER'
        
        elif df['F'] == 4:
            return 'LOYAL'
        
        elif df['R'] == 4:
            return 'ACTIVE'
        
        elif df['R'] == 1:
            return 'LOST'
        
        elif df['M'] == 1:
            return 'LIGHT'
        
        return 'REGULARS'
    
# create a new column RFM_level
df_rfm['RFM_level'] = df_rfm.apply(rfm_level, axis=1)

st.write('3. Dữ liệu sau khi đã tính điểm RFM và phân cụm')
st.dataframe(df_rfm.head(5))

# calculate average values for each RFM_level and return a size of each segment
rfm_agg = df_rfm.groupby('RFM_level').agg({
    'Recency':'mean',
    'Frequency':'mean',
    'Monetary':['mean','count']
}).round(0)
rfm_agg.columns = rfm_agg.columns.droplevel()
rfm_agg.columns = ['RecencyMean','FrequencyMean','MonetaryMean','Count']
rfm_agg['Percent'] = round((rfm_agg['Count']/rfm_agg.Count.sum())*100,2)

# reset the index
rfm_agg = rfm_agg.reset_index()
rfm_agg = rfm_agg.sort_values(by='Count', ascending=False)

st.write('4. Tính giá trị trung bình cho mỗi RFM_level và kích thước của từng phân cụm')
st.dataframe(rfm_agg)

#st.subheader('Biểu đồ kích thước nhóm khách hàng theo phân cụm')
#c = alt.Chart(rfm_agg).mark_bar().encode(x=alt.X('RFM_level', sort=None), y='Count')
#st.altair_chart(c, use_container_width=True)

st.subheader('Biểu đồ')
tab_chart = st.radio('Chọn biểu đồ',['Kích thước theo từng phân cụm khách hàng','Scatter plot RFM','3d Scatter plot RFM'])
if tab_chart == 'Kích thước theo từng phân cụm khách hàng':
    c = alt.Chart(rfm_agg).mark_bar().encode(x=alt.X('RFM_level', sort=None), y='Count')
    st.altair_chart(c, use_container_width=True)
elif tab_chart == 'Scatter plot RFM':
    fig1 = px.scatter(rfm_agg, x='RecencyMean', y='MonetaryMean', size='FrequencyMean', color='RFM_level', hover_name='RFM_level', size_max=100)
    st.plotly_chart(fig1)
else:
    fig2 = px.scatter_3d(df_rfm, x='Recency', y='Frequency', z='Monetary', color='RFM_level', opacity=0.5)
    fig2.update_traces(maker=dict(size=5), selector=dict(mode='makers'))
    st.plotly_chart(fig2)

st.write()

st.subheader('Kết luận')
st.write('''Dựa vào kiến thức nghiệp vụ ta chia khách hàng thành 8 nhóm:
- STARS: nhóm khách hàng có Recency rất gần, Frequency cao và Monetary cao, đây cũng là nhóm khách hàng có giá trị nhất đối vs doanh nghiệp
- BIG SPENDER: nhóm khách hàng có Monetary cao, Freqency và Monetary trung bình
- LOYAL: nhóm khách hàng có Frequency cao
- ACTIVE: nhóm khách hàng có Recency gần đây, Frequency và Monetary trung bình
- LIGHT: nhóm khách hàng có Monetary thấp
- NEW: nhóm khách hàng có Recency rất gần, Frequency và Monetary thấp
- LOST: nhóm khách hàng có Recency cách đây rất lâu
- REGULARS: nhóm khách hàng có tất cả chỉ số ở mức trung bình
''')

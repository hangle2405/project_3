import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
from sklearn.cluster import KMeans
import pickle

st.set_page_config(page_title='Customer Segmentation', page_icon='🍘')

# GUI
st.title("Customer Segmentation Project")

st.subheader('KMeans algorithm')
st.write('Phân cụm bằng thuật toán KMeans')
'---'
df_rfm = pd.read_csv('Data_RFM.csv')
df_rfm = df_rfm[['Recency','Frequency','Monetary']]
st.write('Dữ liệu đã xử lý RFM ')
st.dataframe(df_rfm.head(5))

st.subheader('KMeans clusters with the Elbow method')

st.write('1. Hopkins test')
st.code('''hopkins = hopkins(df_now, df_now.shape[0])
hopkins = 0.0028477600060840776''')
st.write('Giá trị cho thấy có thể phân cụm')

sse = {}
for k in range(1, 20):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_rfm)
    sse[k] = kmeans.inertia_
fig1 = plt.figure(figsize=(10,4))
plt.title('The Elbow Method')
plt.xlabel('k')
plt.ylabel('SSE')
sns.pointplot(x=list(sse.keys()), y=list(sse.values()))
st.pyplot(fig1)

st.write('Ta chọn k = 4')

# build model with k=4
model = KMeans(n_clusters=4, random_state=42)
model.fit(df_rfm)
model.labels_.shape

# Calculate average values for each RFM_Level, and return a size of each segment 
df_rfm['Cluster'] = model.labels_
rfm_agg2 = df_rfm.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']}).round(0)

rfm_agg2.columns = rfm_agg2.columns.droplevel()
rfm_agg2.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
rfm_agg2['Percent'] = round((rfm_agg2['Count']/rfm_agg2.Count.sum())*100, 2)

# Reset the index
rfm_agg2 = rfm_agg2.reset_index()

# Change thr Cluster Columns Datatype into discrete values
rfm_agg2['Cluster'] = 'Cluster '+ rfm_agg2['Cluster'].astype('str')
rfm_agg2 = rfm_agg2.sort_values(by='Count', ascending=False)

st.write('2. Huấn luyện mô hình KMeans Cluster vs k = 4 ta có được 4 nhóm khách hàng theo bảng bên dưới')
st.dataframe(rfm_agg2)

st.subheader('Biểu đồ phân cụm khách hàng theo KMeans Cluster')
#st.write('1. Biểu đồ TreeMap')
#st.write('2. Biểu đồ Scatter Plot')
#st.write('2. Biểu đồ 3d Scatter Plot')

tab_chart = st.radio('Chọn biểu đồ',['Kích thước theo từng phân cụm khách hàng','Chi tiêu trung bình theo phân cụm khách hàng','Scatter plot RFM','3d Scatter plot RFM'])
if tab_chart == 'Kích thước theo từng phân cụm khách hàng':
    fig1 = alt.Chart(rfm_agg2).mark_bar().encode(x=alt.X('Cluster', sort=None), y='Count')
    st.altair_chart(fig1, use_container_width=True)
elif tab_chart == 'Chi tiêu trung bình theo phân cụm khách hàng':
    fig2 = alt.Chart(rfm_agg2).mark_bar().encode(x=alt.X('Cluster', sort=None), y='MonetaryMean')
    st.altair_chart(fig2, use_container_width=True)
elif tab_chart == 'Scatter plot RFM':
    fig3 = px.scatter(rfm_agg2, x='RecencyMean', y='MonetaryMean', size='FrequencyMean', color='Cluster', hover_name='Cluster', size_max=100)
    st.plotly_chart(fig3)
else:
    fig4 = px.scatter_3d(df_rfm, x='Recency', y='Frequency', z='Monetary', color='Cluster', opacity=0.5)
    fig4.update_traces(maker=dict(size=5), selector=dict(mode='makers'))
    st.plotly_chart(fig4)

st.write('''Dựa vào kết quả phân cụm của thuật toán KMeans, ta có thể chia các nhóm khách hàng như sau:
- Cluster 3 - VIP: nhóm khách hàng có Recency rất gần, Frequency cao và Monetary cao. Đây là nhóm khách hàng có mức chi tiêu cao nhưng lại chiếm số lượng khá ít
- Cluster 2 - REGULAR: nhóm khách hàng có Recency gần đây, Frequency trung bình và Monetary trung bình 
- Cluster 1 - COLD: nhóm khách hàng có Recency lâu hơn, Frequency thấp và Monetary thấp
- Cluster 0 - CHURN: nhóm khách hàng có Recency rất lâu, Frequency và Monetary rất thấp
''')

st.subheader('Kết luận')
st.write(''' Kết quả phân cụm của thuật toán KMeans hợp lý và có thể giải thích dễ dàng. Do đó ta chọn và lưu model của thuật toán KMeans để dùng cho việc dự đoán.
''')

pickle.dump(model, open('kmeans_model.pkl','wb'))
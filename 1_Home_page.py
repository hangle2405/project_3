import streamlit as st

st.set_page_config(page_title='Customer Segmentation', page_icon='🍘')

st.title("Customer Segmentation Project")

st.subheader('1. Mục tiêu dự án')
st.write(''' Xây dựng thuật toán phân cụm khách hàng nhằm tìm ra các nhóm khách hàng tương đồng nhau dựa trên dữ liệu mà doanh nghiệp có như ngày phát sinh giao dịch, số lượng đơn hàng, chi tiêu của khách hàng.
Việc phân cụm khách hàng có thể giúp doanh ngiệp hiểu rõ hơn về nhu cầu và mong muốn của từng nhóm khách hàng, từ đó đưa ra các chiến lược kinh doanh phù hợp để thu hút và giữ chân khách hàng.
''')
st.image('customer_segmentation.jpg')

st.subheader('2. Hướng tiếp cận')
st.write('''Dự án tiếp cận vấn đề bằng phương pháp RFM (Recency-Frequency-Monetary). Phương pháp này được sử dụng để phân tích và phân nhóm khách hàng dựa trên ba yếu tố chính:

1. Recency (lần mua gần đây): thời gian kể từ lần mua hàng gần nhất của khách hàng. Khách hàng càng gần đây mua hàng, thì giá trị RFM của họ sẽ càng cao.
2. Frequency (tần suất mua hàng): số lần mua hàng của khách hàng trong một khoảng thời gian nhất định. Khách hàng càng mua nhiều, thì giá trị RFM của họ sẽ càng cao.
3. Monetary (giá trị đơn hàng trung bình): giá trị trung bình của mỗi đơn hàng của khách hàng. Khách hàng càng chi tiêu nhiều tiền, thì giá trị RFM của họ sẽ càng cao.
''')
st.write('''Sau đó, dựa trên các giá trị RFM của khách hàng, chúng ta có thể phân nhóm thủ công dựa trên nghiệp vụ hoặc bằng các thuật toán máy học trên Python như KMeans, Hierarchical và DBSCAN.
''')
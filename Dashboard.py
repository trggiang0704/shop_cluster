# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Cấu hình trang
# st.set_page_config(page_title="Dashboard Khách hàng & Gợi ý Bundle", layout="wide")

# # Đọc dữ liệu
# @st.cache_data
# def load_data():
#     customers = pd.read_csv('data/processed/customer_clusters_from_rules.csv')
#     rules = pd.read_csv('data/processed/rules_fpgrowth_filtered.csv')
#     return customers, rules

# customers, rules = load_data()

# # Tiêu đề đẹp
# st.title('🌟 Dashboard Phân tích Cụm Khách hàng & Gợi ý Bundle/Cross-sell')
# st.markdown("---")

# # Sidebar
# st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
# st.sidebar.header('🔍 Bộ lọc')

# # Định nghĩa tên cụm đẹp (mapping từ số cụm sang tên mô tả)
# cluster_names = {
#     0: "Occasional Shoppers",          # Cụm 0: mua ít, giá trị thấp hoặc không thường xuyên
#     1: "High-Value Loyal Customers"    # Cụm 1: mua nhiều, tần suất cao, giá trị lớn
# }

# # Tạo danh sách tùy chọn cho selectbox: hiển thị tên đẹp, nhưng giá trị vẫn là số cụm
# cluster_options = ['Tất cả'] + sorted(customers['cluster'].unique().tolist())
# # Tạo danh sách hiển thị: "Tất cả", "Cụm 0 - Occasional Shoppers", "Cụm 1 - High-Value Loyal Customers"
# display_options = ['Tất cả'] + [f"Cụm {c} - {cluster_names[c]}" for c in sorted(customers['cluster'].unique())]

# # Selectbox với tên hiển thị đẹp
# selected_display = st.sidebar.selectbox('Chọn cụm khách hàng', options=display_options)

# # Xác định cụm thực tế được chọn (nếu không phải "Tất cả")
# if selected_display == 'Tất cả':
#     selected_cluster = 'Tất cả'
#     cluster_label = "Toàn bộ khách hàng"
# else:
#     # Trích xuất số cụm từ chuỗi hiển thị, ví dụ: "Cụm 0 - Occasional Shoppers" → 0
#     selected_cluster = int(selected_display.split()[1])  # Lấy số sau "Cụm"
#     cluster_label = cluster_names[selected_cluster]

# # Lọc dữ liệu theo cụm đã chọn
# if selected_cluster != 'Tất cả':
#     filtered_customers = customers[customers['cluster'] == selected_cluster]
# else:
#     filtered_customers = customers

# # Hiển thị thông tin ở sidebar
# st.sidebar.markdown("---")
# st.sidebar.caption(f"📊 Tổng số khách hàng: {len(customers):,}")
# st.sidebar.caption(f"👥 Khách hàng đang xem: {len(filtered_customers):,}")
# st.sidebar.caption(f"🎯 Cụm đang chọn: **{cluster_label}**")
# # Layout chính: 3 cột
# col1, col2, col3 = st.columns([1, 1, 1])

# with col1:
#     st.metric(label="Số khách hàng", value=f"{len(filtered_customers):,}")
# with col2:
#     st.metric(label="Doanh thu trung bình", value=f"{filtered_customers['Monetary'].mean():,.0f} $")
# with col3:
#     st.metric(label="Tần suất mua trung bình", value=f"{filtered_customers['Frequency'].mean():.1f}")

# st.markdown("---")

# # Tab layout để tổ chức nội dung đẹp hơn
# tab1, tab2, tab3 = st.tabs(["📈 Thống kê RFM theo Cụm", "🔗 Top Quy tắc Liên kết", "🎁 Gợi ý Bundle & Cross-sell"])

# with tab1:
#     st.subheader(f'Thống kê RFM - {cluster_label}')
    
#     col_a, col_b = st.columns(2)
    
#     with col_a:
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.histplot(filtered_customers['Recency'], kde=True, color='#FF6B6B', ax=ax)
#         ax.set_title('Phân bố Recency (Ngày kể từ lần mua cuối)')
#         st.pyplot(fig)
    
#     with col_b:
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.scatterplot(data=filtered_customers, x='Frequency', y='Monetary', hue='cluster', palette='deep', ax=ax)
#         ax.set_title('Frequency vs Monetary')
#         st.pyplot(fig)
    
#     st.markdown("#### Bảng tóm tắt RFM")
#     rfm_summary = filtered_customers[['Recency', 'Frequency', 'Monetary']].describe().round(2)
#     st.dataframe(rfm_summary.style.background_gradient(cmap='Blues'))

# with tab2:
#     st.subheader('Top Quy tắc Liên kết (Association Rules)')
    
#     col_sort1, col_sort2 = st.columns([1, 1])
#     with col_sort1:
#         sort_metric = st.selectbox('Sắp xếp theo', ['lift', 'confidence', 'support'], index=0)
#     with col_sort2:
#         top_n = st.slider('Số lượng quy tắc hiển thị', 5, 50, 15)
    
#     top_rules = rules.sort_values(by=sort_metric, ascending=False).head(top_n)
    
#     # Chỉ hiển thị các cột quan trọng, đẹp mắt
#     display_rules = top_rules[['rule_str', 'support', 'confidence', 'lift']].copy()
#     display_rules['support'] = display_rules['support'].round(4)
#     display_rules['confidence'] = (display_rules['confidence'] * 100).round(1).astype(str) + '%'
#     display_rules['lift'] = display_rules['lift'].round(2)
    
#     st.dataframe(display_rules.style.background_gradient(cmap='Greens', subset=['lift']))

# with tab3:
#     st.subheader('🎁 Gợi ý Sản phẩm Bundle & Cross-sell')
#     st.info("💡 Các quy tắc dưới đây giúp gợi ý: Khi khách mua sản phẩm bên trái → nên gợi ý sản phẩm bên phải (dựa trên lift và confidence cao)")

#     high_lift_rules = rules[rules['lift'] > 10].sort_values('lift', ascending=False)
    
#     tab_bundle, tab_cross = st.tabs(["📦 Bundle (Mua nhiều → Gợi ý thêm)", "➕ Cross-sell (Mua 1 → Gợi ý thêm)"])
    
#     with tab_bundle:
#         bundle_rules = high_lift_rules[high_lift_rules['antecedents_str'].str.contains(',')]
#         if len(bundle_rules) == 0:
#             st.warning("Không có bundle mạnh (nhiều sản phẩm antecedents) trong top rules.")
#         else:
#             bundle_display = bundle_rules[['antecedents_str', 'consequents_str', 'confidence', 'lift']].head(20)
#             bundle_display['confidence'] = (bundle_display['confidence'] * 100).round(1).astype(str) + '%'
#             bundle_display['lift'] = bundle_display['lift'].round(2)
#             st.dataframe(bundle_display.style.background_gradient(cmap='Oranges', subset=['lift']))
    
#     with tab_cross:
#         cross_rules = high_lift_rules[~high_lift_rules['antecedents_str'].str.contains(',')].head(30)
#         cross_display = cross_rules[['antecedents_str', 'consequents_str', 'confidence', 'lift']]
#         cross_display['confidence'] = (cross_display['confidence'] * 100).round(1).astype(str) + '%'
#         cross_display['lift'] = cross_display['lift'].round(2)
#         st.dataframe(cross_display.style.background_gradient(cmap='Purples', subset=['lift']))

# # Footer
# st.markdown("---")
# st.caption("Dashboard được xây dựng bằng Streamlit • Dữ liệu từ phân tích RFM & FP-Growth")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang
st.set_page_config(page_title="Dashboard Khách hàng & Gợi ý Bundle", layout="wide")

# Đọc dữ liệu
@st.cache_data
def load_data():
    customers = pd.read_csv('data/processed/customer_clusters_from_rules.csv')
    rules = pd.read_csv('data/processed/rules_fpgrowth_filtered.csv')
    return customers, rules

customers, rules = load_data()

# Tiêu đề đẹp
st.title('🌟 Dashboard Phân tích Cụm Khách hàng & Gợi ý Bundle/Cross-sell')
st.markdown("---")

# Sidebar
st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
st.sidebar.header('🔍 Bộ lọc')

# Định nghĩa tên cụm đẹp (mapping từ số cụm sang tên mô tả)
cluster_names = {
    0: "Occasional Shoppers",
    1: "High-Value",
    2: "Niche Repeat Buyer",
    3: "Recent Focused Buyers"
}

# Tạo danh sách tùy chọn cho selectbox: hiển thị tên đẹp, nhưng giá trị vẫn là số cụm
cluster_options = sorted(customers['cluster'].unique().tolist())
display_options = ['Tất cả'] + [f"Cụm {c} - {cluster_names.get(c, 'Unknown')}" for c in cluster_options]

# Selectbox với tên hiển thị đẹp
selected_display = st.sidebar.selectbox('Chọn cụm khách hàng', options=display_options)

# Xác định cụm thực tế được chọn (nếu không phải "Tất cả")
if selected_display == 'Tất cả':
    selected_cluster = 'Tất cả'
    cluster_label = "Toàn bộ khách hàng"
else:
    # Trích xuất số cụm từ chuỗi hiển thị, ví dụ: "Cụm 0 - Occasional Shoppers" → 0
    selected_cluster = int(selected_display.split()[1])  # Lấy số sau "Cụm"
    cluster_label = cluster_names.get(selected_cluster, 'Unknown')

# Lọc dữ liệu theo cụm đã chọn
if selected_cluster != 'Tất cả':
    filtered_customers = customers[customers['cluster'] == selected_cluster]
else:
    filtered_customers = customers

# Hiển thị thông tin ở sidebar
st.sidebar.markdown("---")
st.sidebar.caption(f"📊 Tổng số khách hàng: {len(customers):,}")
st.sidebar.caption(f"👥 Khách hàng đang xem: {len(filtered_customers):,}")
st.sidebar.caption(f"🎯 Cụm đang chọn: **{cluster_label}**")

# Layout chính: 3 cột
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric(label="Số khách hàng", value=f"{len(filtered_customers):,}")
with col2:
    st.metric(label="Doanh thu trung bình", value=f"{filtered_customers['Monetary'].mean():,.0f} $")
with col3:
    st.metric(label="Tần suất mua trung bình", value=f"{filtered_customers['Frequency'].mean():.1f}")

st.markdown("---")

# Tab layout để tổ chức nội dung đẹp hơn
tab1, tab2, tab3 = st.tabs(["📈 Thống kê RFM theo Cụm", "🔗 Top Quy tắc Liên kết", "🎁 Gợi ý Bundle & Cross-sell"])

with tab1:
    st.subheader(f'Thống kê RFM - {cluster_label}')
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(filtered_customers['Recency'], kde=True, color='#FF6B6B', ax=ax)
        ax.set_title('Phân bố Recency (Ngày kể từ lần mua cuối)')
        st.pyplot(fig)
    
    with col_b:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=filtered_customers, x='Frequency', y='Monetary', hue='cluster', palette='deep', ax=ax)
        ax.set_title('Frequency vs Monetary')
        st.pyplot(fig)
    
    st.markdown("#### Bảng tóm tắt RFM")
    rfm_summary = filtered_customers[['Recency', 'Frequency', 'Monetary']].describe().round(2)
    st.dataframe(rfm_summary.style.background_gradient(cmap='Blues'))

with tab2:
    st.subheader('Top Quy tắc Liên kết (Association Rules)')
    
    col_sort1, col_sort2 = st.columns([1, 1])
    with col_sort1:
        sort_metric = st.selectbox('Sắp xếp theo', ['lift', 'confidence', 'support'], index=0)
    with col_sort2:
        top_n = st.slider('Số lượng quy tắc hiển thị', 5, 50, 15)
    
    top_rules = rules.sort_values(by=sort_metric, ascending=False).head(top_n)
    
    # Chỉ hiển thị các cột quan trọng, đẹp mắt
    display_rules = top_rules[['rule_str', 'support', 'confidence', 'lift']].copy()
    display_rules['support'] = display_rules['support'].round(4)
    display_rules['confidence'] = (display_rules['confidence'] * 100).round(1).astype(str) + '%'
    display_rules['lift'] = display_rules['lift'].round(2)
    
    st.dataframe(display_rules.style.background_gradient(cmap='Greens', subset=['lift']))

with tab3:
    st.subheader('🎁 Gợi ý Sản phẩm Bundle & Cross-sell')
    st.info("💡 Các quy tắc dưới đây giúp gợi ý: Khi khách mua sản phẩm bên trái → nên gợi ý sản phẩm bên phải (dựa trên lift và confidence cao)")

    high_lift_rules = rules[rules['lift'] > 10].sort_values('lift', ascending=False)
    
    tab_bundle, tab_cross = st.tabs(["📦 Bundle (Mua nhiều → Gợi ý thêm)", "➕ Cross-sell (Mua 1 → Gợi ý thêm)"])
    
    with tab_bundle:
        bundle_rules = high_lift_rules[high_lift_rules['antecedents_str'].str.contains(',')]
        if len(bundle_rules) == 0:
            st.warning("Không có bundle mạnh (nhiều sản phẩm antecedents) trong top rules.")
        else:
            bundle_display = bundle_rules[['antecedents_str', 'consequents_str', 'confidence', 'lift']].head(20)
            bundle_display['confidence'] = (bundle_display['confidence'] * 100).round(1).astype(str) + '%'
            bundle_display['lift'] = bundle_display['lift'].round(2)
            st.dataframe(bundle_display.style.background_gradient(cmap='Oranges', subset=['lift']))
    
    with tab_cross:
        cross_rules = high_lift_rules[~high_lift_rules['antecedents_str'].str.contains(',')].head(30)
        cross_display = cross_rules[['antecedents_str', 'consequents_str', 'confidence', 'lift']]
        cross_display['confidence'] = (cross_display['confidence'] * 100).round(1).astype(str) + '%'
        cross_display['lift'] = cross_display['lift'].round(2)
        st.dataframe(cross_display.style.background_gradient(cmap='Purples', subset=['lift']))

# Footer
st.markdown("---")
st.caption("Dashboard được xây dựng bằng Streamlit • Dữ liệu từ phân tích RFM & FP-Growth")
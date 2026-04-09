import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Premium Data Dashboard", layout="wide")

# =========================
# PREMIUM UI STYLE
# =========================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background: #ffffff;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🚀 Premium Data Dashboard")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # =========================
    # FILTERS
    # =========================
    st.subheader("🔍 Filters")

    category_cols = df.select_dtypes(include=['object']).columns

    if len(category_cols) > 0:
        filter_col = st.selectbox("Select column to filter", category_cols)
        selected_value = st.selectbox("Select value", df[filter_col].unique())

        df = df[df[filter_col] == selected_value]

    # =========================
    # KPI CARDS
    # =========================
    st.subheader("📊 Key Metrics")

    numeric_cols = df.select_dtypes(include=['int64','float64']).columns

    if len(numeric_cols) > 0:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", len(df))
        col2.metric("Average Value", round(df[numeric_cols[0]].mean(),2))
        col3.metric("Max Value", df[numeric_cols[0]].max())

    # =========================
    # CHARTS
    # =========================
    st.subheader("📈 Visualizations")

    col1, col2 = st.columns(2)

    # BAR CHART
    with col1:
        st.markdown("### 📊 Bar Chart")
        x_axis = st.selectbox("X Axis", df.columns)
        y_axis = st.selectbox("Y Axis", numeric_cols)

        fig, ax = plt.subplots()
        df.groupby(x_axis)[y_axis].sum().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    # PIE CHART
    with col2:
        st.markdown("### 🥧 Pie Chart")
        pie_col = st.selectbox("Pie Column", category_cols)

        pie_data = df[pie_col].value_counts()

        fig2, ax2 = plt.subplots()
        ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    # =========================
    # LINE CHART
    # =========================
    st.subheader("📈 Trend Analysis")

    if len(numeric_cols) > 0:
        line_col = st.selectbox("Select column for trend", numeric_cols)
        st.line_chart(df[line_col])

else:
    st.info("Upload a CSV file to start")
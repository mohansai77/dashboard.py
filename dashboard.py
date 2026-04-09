import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mini Data Dashboard", layout="wide")

# -------------------------
# TITLE
# -------------------------
st.title("📊 Mini Data Dashboard")

st.write("Upload your dataset and explore insights instantly.")

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())

    # -------------------------
    # COLUMN SELECTION
    # -------------------------
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    category_cols = df.select_dtypes(include=['object']).columns

    if len(numeric_cols) > 0 and len(category_cols) > 0:

        col1, col2 = st.columns(2)

        # -------------------------
        # BAR CHART
        # -------------------------
        with col1:
            st.subheader("📊 Bar Chart")

            x_axis = st.selectbox("Select Category", category_cols)
            y_axis = st.selectbox("Select Numeric", numeric_cols)

            fig, ax = plt.subplots()
            df.groupby(x_axis)[y_axis].sum().plot(kind='bar', ax=ax)
            st.pyplot(fig)

        # -------------------------
        # PIE CHART
        # -------------------------
        with col2:
            st.subheader("🥧 Pie Chart")

            pie_col = st.selectbox("Select Column for Pie", category_cols)

            pie_data = df[pie_col].value_counts()

            fig2, ax2 = plt.subplots()
            ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
            st.pyplot(fig2)

    else:
        st.warning("Dataset needs at least one numeric and one categorical column")

else:
    st.info("Upload a CSV file to start")
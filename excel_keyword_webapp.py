import streamlit as st
import pandas as pd
import io
import os

st.title("🔍 Excel Keyword Search Tool")

# List Excel files in current directory
def list_excel_files():
    return [f for f in os.listdir() if f.endswith('.xlsx')]

excel_files = list_excel_files()

selected_file = st.selectbox("Select an Excel file from the current directory:", excel_files)

if selected_file:
    df = pd.read_excel(selected_file)
    st.success(f"Loaded file: {selected_file}")

    st.write("### Preview of Data:")
    st.dataframe(df.head())

    columns = list(df.columns)
    selected_columns = st.multiselect("Select columns to search (or leave blank to search all):", columns)
    keyword_input = st.text_input("Enter keywords (comma-separated):")

    if st.button("Search") and keyword_input:
        keywords = [k.strip().lower() for k in keyword_input.split(',') if k.strip()]
        cols_to_search = selected_columns if selected_columns else columns

        mask = df[cols_to_search].apply(
            lambda row: row.astype(str).str.lower().str.contains('|'.join(keywords)).any(), axis=1
        )
        filtered_df = df[mask]

        st.write(f"### 🔎 Found {len(filtered_df)} matching rows:")
        st.dataframe(filtered_df)

        # Download filtered results
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Original', index=False)
            filtered_df.to_excel(writer, sheet_name='Filtered', index=False)
        st.download_button(
            label="📥 Download Results as Excel",
            data=output.getvalue(),
            file_name="filtered_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

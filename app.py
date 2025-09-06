import streamlit as st
import os

# 设置网页标题
st.title("「数字小世界」数据报告下载")

# 扫描 reports 目录下所有文件
reports_dir = "reports"
files = [f for f in os.listdir(reports_dir) if os.path.isfile(os.path.join(reports_dir, f))]

st.write("#### 可下载文件列表：")

for filename in files:
    file_path = os.path.join(reports_dir, filename)
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    st.download_button(
        label=f"下载 {filename}",
        data=file_bytes,
        file_name=filename,
        mime="application/pdf" if filename.lower().endswith(".pdf") else "application/octet-stream"
    )

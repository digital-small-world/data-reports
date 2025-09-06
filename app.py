import streamlit as st

# 设置网页标题
st.title("PDF文件下载")

# 文件路径
pdf_path = "reports/GlobalEVOutlook2024.pdf"

# 读取PDF文件内容
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# 下载按钮
st.download_button(
    label="下载 OECD 2025 展望.pdf",
    data=pdf_bytes,
    file_name="OECD 2025 展望.pdf",
    mime="application/pdf"
)

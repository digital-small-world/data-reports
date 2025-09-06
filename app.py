import streamlit as st
import streamlit as st
import os

# 设置浅色调舒适主题和背景
st.markdown(
    """
    <style>
    body {
        background-color: #f7f9fa;
    }
    .stApp {
        background: linear-gradient(135deg, #f7f9fa 0%, #e3eaf2 100%);
        color: #222;
    }
    /* 修复按钮默认背景为黑色问题，覆盖所有按钮类 */
    button {
        background-color: #e3eaf2 !important;
        color: #222 !important;
        border-radius: 8px !important;
        border: 1px solid #d1dbe6 !important;
        padding: 0.5em 1.2em !important;
        font-size: 1em !important;
        transition: background 0.2s !important;
    }
    button:hover {
        background-color: #c7d6e6 !important;
        color: #222 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #2a3a4d;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import os

# 设置网页标题
st.title("「数字小世界」数据报告下载")

# 扫描 reports 目录下所有文件
reports_dir = "reports"

# 获取文件及其创建/移动时间
file_infos = []
for f in os.listdir(reports_dir):
    file_path = os.path.join(reports_dir, f)
    if os.path.isfile(file_path):
        ctime = os.path.getctime(file_path)
        file_infos.append((f, ctime))

# 按ctime倒序排序
file_infos.sort(key=lambda x: x[1], reverse=True)

st.write("#### 可下载文件列表：")

for filename, _ in file_infos:
    file_path = os.path.join(reports_dir, filename)
    file_size = os.path.getsize(file_path)
    # 文件大小格式化为 MB 或 KB
    if file_size >= 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{file_size / 1024:.0f} KB"
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    filename_parts = filename.split('.')
    st.download_button(
        label=f"{filename_parts[0]}（{filename_parts[-1]}，{size_str}）",
        data=file_bytes,
        file_name=filename,
        mime="application/pdf" if filename.lower().endswith(".pdf") else "application/octet-stream"
    )

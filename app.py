import streamlit as st
import streamlit as st
import os
import datetime
import json

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

file_times_path = "data/file_times.json"
file_infos = []

# 本地运行时，记录mtime到json文件
if not (os.environ.get("STREAMLIT_CLOUD") or os.environ.get("GITHUB_WORKSPACE")):
    file_times = {}
    for f in os.listdir(reports_dir):
        file_path = os.path.join(reports_dir, f)
        if os.path.isfile(file_path):
            mtime = os.path.getmtime(file_path)
            file_times[f] = mtime
    os.makedirs("data", exist_ok=True)
    with open(file_times_path, "w", encoding="utf-8") as fw:
        json.dump(file_times, fw)
    file_infos = [(f, file_times[f]) for f in file_times]
else:
    # 云端运行时，直接读取json文件
    if os.path.exists(file_times_path):
        with open(file_times_path, "r", encoding="utf-8") as fr:
            file_times = json.load(fr)
        file_infos = [(f, file_times[f]) for f in file_times]
    else:
        file_infos = []

import datetime
st.write(datetime.datetime.fromtimestamp(1758639287.1847126))
st.write(file_infos)


# 按mtime倒序排序
file_infos.sort(key=lambda x: x[1], reverse=True)

st.write("#### 可下载文件列表：")

for filename, file_time in file_infos:
    file_path = os.path.join(reports_dir, filename)
    file_size = os.path.getsize(file_path)
    # 文件大小格式化为 MB 或 KB
    if file_size >= 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{file_size / 1024:.0f} KB"

    # Debug 输出，查看时间戳
    # st.write(filename, file_time, datetime.datetime.fromtimestamp(file_time))

    # 显示本地记录的mtime
    show_time = datetime.datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M")
    # show_time = datetime.datetime.fromtimestamp(1758639287.1847126).strftime("%Y-%m-%d %H:%M")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    filename_parts = filename.split('.')
    st.download_button(
        label=f"{filename_parts[0]}（{filename_parts[-1]}，{size_str}，{show_time}）",
        data=file_bytes,
        file_name=filename,
        mime="application/pdf" if filename.lower().endswith(".pdf") else "application/octet-stream"
    )

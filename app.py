import streamlit as st
import streamlit as st
import os
import datetime

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

def is_local():
    # 通过隐藏文件判定本地环境
    return os.path.exists(".local_env")

if is_local():
    # 本地运行时，按mtime排序
    file_infos = []
    for f in os.listdir(reports_dir):
        file_path = os.path.join(reports_dir, f)
        if os.path.isfile(file_path):
            mtime = os.path.getmtime(file_path)
            file_infos.append((f, mtime))
else:
    # 云端运行时，按git last_commit_date排序
    import subprocess
    from pathlib import Path
    file_infos = []
    for file_path in Path(reports_dir).rglob('*'):
        if file_path.is_file():
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ci', '--', str(file_path)],
                capture_output=True, text=True
            )
            commit_date = result.stdout.strip() if result.stdout.strip() else None
            if commit_date:
                try:
                    dt = datetime.datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S %z")
                    ts = dt.timestamp()
                except Exception:
                    ts = 0
                file_infos.append((file_path.name, ts))
            else:
                file_infos.append((file_path.name, 0))


# 按时间倒序排序
file_infos.sort(key=lambda x: x[1], reverse=True)

st.write("#### 可下载文件列表：")

for filename, file_time in file_infos:
    file_path = os.path.join(reports_dir, filename)
    file_size = os.path.getsize(file_path)

    # 文件大小格式转化为 MB 或 KB
    if file_size >= 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{file_size / 1024:.0f} KB"

    # 显示文件下载按钮，包括文件相关信息
    show_time = datetime.datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    filename_parts = filename.split('.')
    st.download_button(
        label=f"{filename_parts[0]}（{filename_parts[-1]}，{size_str}，{show_time}）",
        data=file_bytes,
        file_name=filename,
        mime="application/pdf" if filename.lower().endswith(".pdf") else "application/octet-stream"
    )

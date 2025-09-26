#!/usr/bin/env python3
"""
获取reports目录下所有文件的文件名和最后提交日期
"""

import subprocess
from pathlib import Path


def get_files_commit_dates(reports_dir="reports"):
    """
    获取reports目录下所有文件的文件名和最后提交日期
    
    Args:
        reports_dir: reports目录路径
        
    Returns:
        包含文件名和最后提交日期的列表
    """
    files_info = []
    
    for file_path in Path(reports_dir).rglob('*'):
        if file_path.is_file():
            # 获取最后提交日期
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ci', '--', str(file_path)],
                capture_output=True, text=True
            )
            
            commit_date = result.stdout.strip() if result.stdout.strip() else "No commits"
            
            files_info.append({
                'filename': file_path.name,
                'last_commit_date': commit_date
            })
    
    return files_info


def print_files_info(files_info):
    """打印文件信息"""
    for info in files_info:
        print(f"{info['filename']:<30} {info['last_commit_date']}")


if __name__ == "__main__":
    files = get_files_commit_dates()
    print_files_info(files)
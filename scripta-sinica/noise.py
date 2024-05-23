import os
import re


def is_chinese_char(char):
    # 判断是否为中文字符
    return '\u4e00' <= char <= '\u9fff'


def count_chars_and_noise(file_path, stats):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        stats['total_chars'] += len(content)

        for char in content:
            if is_chinese_char(char):
                stats['chinese_chars'] += 1
            elif char.isalnum():
                stats['noise_chars'] += 1


def traverse_folder(folder_path):
    stats = {
        'total_chars': 0,
        'chinese_chars': 0,
        'noise_chars': 0
    }

    print(f"开始遍历文件夹: {folder_path}")

    for root, dirs, files in os.walk(folder_path):
        print(f"当前文件夹: {root}")
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"正在处理文件: {file_path}")
                count_chars_and_noise(file_path, stats)

    total_chars = stats['total_chars']
    noise_chars = stats['noise_chars']
    noise_ratio = noise_chars / total_chars if total_chars > 0 else 0

    print("---")
    print("遍历完成!")
    print(f"总字符数: {total_chars}")
    print(f"总中文字符数: {stats['chinese_chars']}")
    print(f"总噪声字符数: {noise_chars}")
    print(f"总噪声比例: {noise_ratio:.2%}")


# 指定要遍历的文件夹路径
folder_path = "02儒藏-0370部"

# 开始遍历文件夹
traverse_folder(folder_path)
import os
import re

def is_chinese_char(char):
    # Check if the character is a Chinese character
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

    print(f"Start traversing folder: {folder_path}")

    for root, dirs, files in os.walk(folder_path):
        print(f"Current folder: {root}")
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                count_chars_and_noise(file_path, stats)

    total_chars = stats['total_chars']
    noise_chars = stats['noise_chars']
    noise_ratio = noise_chars / total_chars if total_chars > 0 else 0

    print("---")
    print("Traversal completed!")
    print(f"Total characters: {total_chars}")
    print(f"Total Chinese characters: {stats['chinese_chars']}")
    print(f"Total noise characters: {noise_chars}")
    print(f"Noise ratio: {noise_ratio:.2%}")


# Specify the folder path to traverse
folder_path = "02儒藏-0370部"

# Start traversing the folder
traverse_folder(folder_path)

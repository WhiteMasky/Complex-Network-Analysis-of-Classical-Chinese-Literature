import os
import shutil
from jiayan import load_lm
from jiayan import CRFPunctuator


def add_punctuation(text_path, punct_path):
    # 读取文本内容
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 检查文本中是否已有标点
    if any(char in '。，！？：；' for char in text):
        print(f"{text_path} already has punctuation, renaming and copying...")
        # 直接复制文件并重命名
        shutil.copy(text_path, punct_path)
        return False
    else:
        print(f"Adding punctuation to {text_path}...")

        # 使用甲言进行自动标点
        lm = load_lm('../jiayan_models/jiayan_models/jiayan.klm')
        punctuator = CRFPunctuator(lm, '../jiayan_models/jiayan_models/cut_model')
        punctuator.load('../jiayan_models/jiayan_models/punc_model')
        punctuated_text = punctuator.punctuate(text)

        # 将标点后的文本写入新文件
        with open(punct_path, 'w', encoding='utf-8') as f:
            f.write(punctuated_text)

        return True


def process_folder(folder_path, output_folder):
    # 遍历文件夹下的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查是否为txt文件
            if file.endswith('.txt'):
                text_path = os.path.join(root, file)

                # 构建输出文件路径,将原路径中folder_path部分替换为output_folder,并在文件名后加上_punct
                output_path = os.path.join(output_folder, os.path.relpath(root, folder_path), file[:-4] + '_punct.txt')

                # 添加标点,如果原文件已有标点则只重命名复制
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                add_punctuation(text_path, output_path)


# 指定要处理的文件夹路径
folder_path = '02儒藏-0370部-简体'
output_folder = '02儒藏-0370部-简体-标点'

# 开始处理
process_folder(folder_path, output_folder)
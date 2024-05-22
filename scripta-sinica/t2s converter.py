import os
import opencc
import shutil

def contains_traditional(text):
    """Check if the text contains Traditional Chinese characters."""
    converter = opencc.OpenCC('t2s')

    simplified_text = converter.convert(text)

    return simplified_text != text


def convert_file_to_simplified(source_file_path, destination_file_path):
    """Convert the content of a file from Traditional Chinese to Simplified Chinese and save it to a new file."""
    converter = opencc.OpenCC('t2s')

    with open(source_file_path, 'r', encoding='utf-8') as file:
        traditional_text = file.read()

    if contains_traditional(traditional_text):
        print(f"Detected Traditional Chinese characters in {source_file_path}")

    simplified_text = converter.convert(traditional_text)

    with open(destination_file_path, 'w', encoding='utf-8') as file:
        file.write(simplified_text)


def convert_directory_to_simplified(source_directory, destination_directory):
    """Recursively convert all .txt files in the given directory to Simplified Chinese and save them in a new directory."""
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    total_files = sum(len(files) for _, _, files in os.walk(source_directory))
    processed_files = 0

    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.txt'):
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_file_path, source_directory)
                destination_file_path = os.path.join(destination_directory, relative_path)

                destination_file_dir = os.path.dirname(destination_file_path)
                if not os.path.exists(destination_file_dir):
                    os.makedirs(destination_file_dir)

                print(f"Converting: {source_file_path} to {destination_file_path}")
                convert_file_to_simplified(source_file_path, destination_file_path)

                processed_files += 1
                print(f"Progress: {processed_files}/{total_files} files converted")


if __name__ == "__main__":
    source_directory = "02儒藏-0370部"
    destination_directory = "02儒藏-0370部-简体"
    convert_directory_to_simplified(source_directory, destination_directory)
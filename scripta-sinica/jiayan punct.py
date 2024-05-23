import os
import shutil
from jiayan import load_lm
from jiayan import CRFPunctuator

def add_punctuation(text_path, punct_path):
    # Read the content of the text file
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Check if the text already has punctuation
    if any(char in '。，！？：；' for char in text):
        print(f"{text_path} already has punctuation, renaming and copying...")
        # Copy the file and rename it
        shutil.copy(text_path, punct_path)
        return False
    else:
        print(f"Adding punctuation to {text_path}...")

        # Use Jiayan for automatic punctuation
        lm = load_lm('../jiayan_models/jiayan_models/jiayan.klm')
        punctuator = CRFPunctuator(lm, '../jiayan_models/jiayan_models/cut_model')
        punctuator.load('../jiayan_models/jiayan_models/punc_model')
        punctuated_text = punctuator.punctuate(text)

        # Write the punctuated text to a new file
        with open(punct_path, 'w', encoding='utf-8') as f:
            f.write(punctuated_text)

        return True


def process_folder(folder_path, output_folder):
    # Traverse all files and subfolders in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a txt file
            if file.endswith('.txt'):
                text_path = os.path.join(root, file)

                # Build the output file path by replacing the folder_path part with output_folder
                # and adding _punct to the file name
                output_path = os.path.join(output_folder, os.path.relpath(root, folder_path), file[:-4] + '_punct.txt')

                # Add punctuation, if the original file already has punctuation, only rename and copy it
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                add_punctuation(text_path, output_path)


# Specify the folder path to process
folder_path = '02儒藏-0370部-简体'
output_folder = '02儒藏-0370部-简体-标点'

# Start the processing
process_folder(folder_path, output_folder)

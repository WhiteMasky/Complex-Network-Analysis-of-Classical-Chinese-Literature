import os
import json
from jiayan import CharHMMTokenizer, WordNgramTokenizer, load_lm

print("Loading Jiayan language model...")
lm = load_lm('../jiayan_models/jiayan_models/jiayan.klm')

print("Initializing tokenizers...")
char_tokenizer = CharHMMTokenizer(lm)
word_tokenizer = WordNgramTokenizer()

print("Initializing CCN and CSN...")
ccn = {}
csn = {}

corpus_folder = '02儒藏-0370部-简体-标点'
output_folder = '02儒藏-0370部-简体-标点-分词'

print(f"Traversing corpus folder: {corpus_folder}")
for root, dirs, files in os.walk(corpus_folder):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            print("Tokenizing text...")
            char_tokens = list(char_tokenizer.tokenize(text))
            word_tokens = list(word_tokenizer.tokenize(text))

            output_path = os.path.join(output_folder, os.path.relpath(root, corpus_folder), f'tokenized_{file}')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"Saving tokenized text to: {output_path}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(' '.join(char_tokens))

            print("Constructing CCN...")
            for i in range(len(char_tokens) - 1):
                node1 = char_tokens[i]
                node2 = char_tokens[i + 1]
                if node1 not in ccn:
                    ccn[node1] = {}
                if node2 not in ccn[node1]:
                    ccn[node1][node2] = 0
                ccn[node1][node2] += 1

            print("Constructing CSN...")
            for sentence in text.split('。'):
                sentence_tokens = word_tokenizer.tokenize(sentence)
                for node1 in sentence_tokens:
                    if node1 not in csn:
                        csn[node1] = {}
                    for node2 in sentence_tokens:
                        if node1 != node2:
                            if node2 not in csn[node1]:
                                csn[node1][node2] = 0
                            csn[node1][node2] += 1

print("Saving constructed CCN and CSN...")
with open('ccn.json', 'w', encoding='utf-8') as f:
    json.dump(ccn, f, ensure_ascii=False)
with open('csn.json', 'w', encoding='utf-8') as f:
    json.dump(csn, f, ensure_ascii=False)

print("Done!")
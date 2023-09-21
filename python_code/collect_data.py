import os
import csv
import json
import re

import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Directory containing the datas
root_directory = "/media/sau/TRAVAIL/ubuntu-proj/Articles"

# Create a list to store folder data
data_list = []

# Function to count words and sentences in a text
def count_words_sentences(text):
    words = len(text.split())
    sentences = len(re.split(r'[.!?]', text))
    return words, sentences

# Function to extract the latest year from folder names
def extract_latest_year(folder_name):
    years = re.findall(r"_?(\d{4})_?", folder_name)
    if years:
        return max(map(int, years))
    else:
        return None

# Function to extract the latest year from folder names
def extract_first_year(folder_name):
    years = re.findall(r"_?(\d{4})_?", folder_name)
    if years:
        return min(map(int, years))
    else:
        return None
    
# List of common words and stopwords to be removed
common_words = ["quelques", "semestre", "pdf","tome","er", "eme", "fascicule"]
stop_words_fr = set(stopwords.words("french"))
stop_words_en = set(stopwords.words("english"))
months_fr = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "aout", "septembre", "octobre", "novembre", "décembre", "decembre", "années", "année"
]


noise_word = ["ke","lez", "dez", "ez", "vur", "ve", "ui", "led", "ua", "dea", "lea",
              "von", "gu", "ke", "ef", "leu", "deu", "paa", "ila",
              "dex", "pag", "cea", "el", "dui", "ka", 
              "noua", "ue", "ie", "ur", "ed", "dana", "ari", "jà", "àl"]

import spacy 
nlp = spacy.load("fr_core_news_sm")

for word in noise_word:
    nlp.vocab[word].is_stop = True

for word in stop_words_en:
    nlp.vocab[word].is_stop = True
    
for word in stop_words_fr:
    nlp.vocab[word].is_stop = True
    
# Function to preprocess the filename
def preprocess_filename(filename):
    # filename = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("utf-8")  # Remove non-ASCII characters
    filename = re.sub(r"[^a-zA-Zœéèàçê\s]", " ", filename) # Replace non-alphabet characters with spaces, keep French characters
    filename = re.sub(r"\d+", "", filename)  # Remove numbers
    filename = re.sub(r"viêt", "viet", filename)
    filename = re.sub(r"\b\w\b", "", filename)  # Remove single letters
    filename = re.sub(r"\bviet-nam\b", "vietnam", filename, flags=re.IGNORECASE)  # Replace "viet-nam" with "vietnam" 
    filename = re.sub(r"\b[IVXLCDM]+\b", "", filename, flags=re.IGNORECASE)  # Remove Roman numerals
    # doc=nlp(filename)
    # lemma_filename = " ".join([token.lemma_ for token in doc])
    words = [word for word in word_tokenize(filename) if word.lower() not in stop_words_fr and word.lower() not in common_words and word.lower() not in months_fr]
    return " ".join(words)

# Function to preprocess the text
def preprocess_text(text):
    # print(text[:3000])
    text = text.lower()
    text = text.replace("-\n", "") # restituer mots coupe a la fin de la ligne
    
    # text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")  # Remove non-ASCII characters
    text = re.sub(r"[^a-zA-Zœéèàçêî.\s]", " ", text)  # Replace non-alphabet characters with spaces, keep French char
    # Replace multiple spaces or newlines with a single space
    text = re.sub(r'[\s\n]+', ' ', text)
    # Replace multiple consecutive dots with a single dot
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r"\d+", "", text)  # Remove numbers
    # Remove single letters except 'a' using a regular expression
    text = re.sub(r'\b[^a]\b', ' ', text)
    text = re.sub(r"viêt", "viet", text)
    text = re.sub(r"ldochinoise", "indochinoise", text)
    text = re.sub(r"eulture", "culture", text)
    text = re.sub(r"rruxelle", "bruxelle", text)
    text = re.sub(r"lournal", "journal", text)
    text = re.sub(r"dournal", "journal", text) 
    text = re.sub(r"airea", "aires", text)
    text = re.sub(r"ingochin", "indochin", text)
    text = re.sub(r"concoura", "concours", text)
    text = re.sub(r"cclui", "celui", text)
    # text = re.sub(r"biên[ -]?hoà", "biênhoà", text) airea ingochinoise concoura viê œuyre cclui: 160
    text = re.sub(r"œuyre", "œuvre", text)
    text = re.sub(r"viê", "vie", text)
    text = re.sub(r"rordeaux", "bordeuax", text)
    text = re.sub(r"rerlin", "berlin", text)
    text = re.sub(r"relge", "belge", text)
    text = re.sub(r"randu", "rendu", text)
    text = re.sub(r"ned", '', text)
    text = re.sub(r"lvon","lyon",text)
    text = re.sub(r"faris","paris",text)
    text = re.sub(r"societe","société",text)
    text = re.sub(r"sociêté","société",text)
    text = re.sub(r"asiatie","asiatique",text)
    text = re.sub(r"sgigon","saigon",text)
    text = re.sub(r"diblio","biblio",text)
    text = re.sub(r"etude","étude",text)

    text = re.sub(r'\b[bcdfghjklmnpqrstvwxyz]+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r"\bviet-nam\b", "vietnam", text, flags=re.IGNORECASE)  # Replace "viet-nam" with "vietnam" 
    text = re.sub(r"\b[IVXLCDM]+\b", "", text, flags=re.IGNORECASE)  # Remove Roman numerals
    tokens=nlp(text)
    tokens = [token for token in tokens if not token.is_stop] #RESERVE STOPWORDS REMOVAL FOR JUPYTER NOTEBOOK
    tokens = [token.lemma_ for token in tokens]
    
    lemma_text = " ".join(tokens)
    
    return  lemma_text #" ".join(tokens)


# Function to recursively traverse the directory and collect data
def collect_data(directory):
    article_id=0
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            print(article_id)
            folder_path = os.path.join(root, dir_name)
            text_data = []
            total_words = 0
            total_sentences = 0

            for file_name in os.listdir(folder_path):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        
                        words, sentences = count_words_sentences(text)
                        print(words, sentences,len(text))
                        
                        text= preprocess_text(text)
                        text_data.append(text)
                        # words, sentences = count_words_sentences(text)
                        # print(words, sentences,len(text))
                        
                        total_words += words
                        total_sentences += sentences
                        # break

            latest_year = extract_latest_year(dir_name)
            first_year = extract_first_year(dir_name)
            processed_filename = preprocess_filename(dir_name[:-7])
            if text_data:
                data_list.append({
                    "FolderName": dir_name,
                    "Title": processed_filename,
                    "Words": total_words,
                    "Sentences": total_sentences,
                    "FirstYear": first_year,
                    "LatestYear": latest_year,
                    "ArticleID":article_id,
                    "TextData": "\n".join(text_data)
                })
            article_id = article_id + 1
            # break
            
# Call the function to collect data
collect_data(root_directory)

# Specify the output file format (CSV or JSON)
output_format = "json"

if output_format == "csv":
    # Save data to a CSV file
    csv_file = "output_cleaned_lemma.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["FolderName", "TextData", "Words", "Sentences", "LatestYear"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
    print(f"Data saved to {csv_file}")

elif output_format == "json":
    # Save data to a JSON file
    json_file = "data_final_stopword_lemma.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4)
    print(f"Data saved to {json_file}")

else:
    print("Invalid output format. Please choose 'csv' or 'json'.")

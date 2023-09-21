# BSEI_Indochina

This repository showcases the source code associated with my master's thesis at the Ecole nationale des chartes in Paris. Its primary goal is to explore a prestigious collection of bulletins from the Society of Study in Indochina, containing over 1000 articles gathered between 1880 and 1975.

The source code includes a Python file **kraken_code.py** for extracting textual data from images using the Kraken OCR, as well as a Python script for preprocessing and formatting the corpus **collection_data.py** into JSON format. We leverage Jupyter Notebook for text processing and various techniques in corpus exploration.

The primary work is organized into separate files:

1. **exploration_title.ipynb**: This notebook focuses on basic exploration of document titles. It aims to discover vocabulary, popular word collocations, and visualizations such as word clouds and co-occurrence graphs. Additionally, it explores the distribution of documents over the years.

2. **exploration_corpus.ipynb**: In this notebook, we delve into the text data within the corpus. Our goal is to identify popular vocabulary, n-grams, and the frequency of key terms within the corpus.

3. **top2vec.ipynb**: This notebook is dedicated to training a Top2Vec model for creating topic models of the corpus. It also includes visualizations of the results for further discussion.

4. **word2vec.ipynb**: Here, we train a Word2Vec model to generate a set of keywords related to specific themes. These keywords are then combined with a Top2Vec model to identify related documents. The results are visualized for discussion.

5. **LDA.ipynb**: This notebook implements a Latent Dirichlet Allocation (LDA) topic modeling over our corpus. The result is used for comparing the modeling efficiency against Top2Vec model.

In summary, this repository contains the source code and notebooks used for exploring and analyzing the valuable collection of Indochina bulletins, offering insights into the content and topics covered during the period from 1880 to 1975.

The workflow of the technique implementation is presented in the following image :
![image](https://github.com/giangpen/B.S.E.I./assets/92431494/e8a18d62-abf2-462b-8a5b-aee53fe0e157)

To obtain a comprehensive grasp of the project, I kindly direct your attention to the full thesis available within this PDF document.

import math
import sys
import nltk
from PyQt5.QtWidgets import *
from Gui import *
import networkx as nx
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
from rouge import Rouge

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

title_words = []
sentences = []
processed_sentences = []
score_sentences = []
theme_words = []
similarity_th = 0.0
score_th = 0.0
summary = ""

def browseFile():
    ui.textBrowseFile_summary.setPlainText("")
    ui.label_rouge.setText("")
    ui.lineEdit_scoreTh.setText("")
    ui.lineEdit_similarityTh.setText("")

    global title_words, sentences, processed_sentences, summary
    filename = QFileDialog.getOpenFileName()
    file = filename[0]
    title_words = []
    sentences = []
    processed_sentences = []
    paragraphs = []
    document_text = ""
    text = ""
    control = -1
    document = Document(file)

    for prg in document.paragraphs:
        paragraphs.append(prg.text)

    for i in paragraphs:
        if i == "":
            document_text += "\n\n"
        else:
            document_text += i + " "

    for i in paragraphs:
        if "Örnek Doküman" in i:
            control = 0  # Örnek Metin
            continue
        if "Örnek Özet" in i:
            control = 1  # Beklenen Özet
            continue

        if control == 0:
            if i != "":
                text += i + " "
        if control == 1:
            if i != "":
                summary += i + " "

    sentences = nltk.sent_tokenize(text)
    ui.textBrowseFile.setPlainText("" + document_text)

    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip()
        processed_sentences.append(preprocess_text(sentences[i]))

    # Başlıktaki kelimeler
    title_words = processed_sentences[0].split()

    sentences.remove(sentences[0])
    processed_sentences.remove(processed_sentences[0])

def preprocess_text(text):
    # Noktalama işaretlerini kaldır
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Küçük harfe çevir
    text = text.lower()

    # Metni kelimelere ayır
    words = text.split()

    # Stop-word'leri çıkar
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Stemming işlemi uygula
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    word = ""

    for i in stemmed_words:
        word += i + " "

    return word.strip()

def visualize_graph(words):
    # Boş bir graf oluştur
    graph = nx.Graph()

    # Her kelime için düğüm ekle
    for i in range(len(words)):
        graph.add_node(words[i])

        # Her iki ardışık kelime arasına bir kenar ekle
        if i < len(words) - 1:
            graph.add_edge(words[i], words[i+1])

    # Grafı çiz
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos)
    plt.show()

def visualize_doc_button_clicked():
    sentence = ui.textBrowseFile.toPlainText()
    if sentence == "":
        warning_message("Please select a document!")
    else:
        processed_words = preprocess_text(sentence)
        visualize_graph(processed_words.split())

def summary_button_clicked():
    global similarity_th, score_th, score_sentences, theme_words
    sentence = ui.textBrowseFile.toPlainText()

    if sentence == "" or ui.lineEdit_similarityTh.text() == "" or ui.lineEdit_scoreTh.text() == "":
        warning_message("Please fill all fields correctly!")
    else:
        try:
            similarity_th = float(ui.lineEdit_similarityTh.text())
            score_th = float(ui.lineEdit_scoreTh.text())
            score_sentences = []
            theme_words = []

            word_tfidf = calculate_tfidf()
            big_to_small = sorted(word_tfidf.keys(), key=lambda x: (word_tfidf[x], x), reverse=True)

            for i in range(int(len(word_tfidf) / 10)):
                theme_words.append(big_to_small[i])

            for i in range(len(processed_sentences)):
                score_sentences.append(calculate_sentence_score(str(processed_sentences[i]), i))

            visualize_graph(score_sentences)
            text = ""
            for i in range(len(score_sentences)):
                if score_sentences[i] > score_th:
                    text += sentences[i] + " "

            if text == "":
                ui.textBrowseFile_summary.setPlainText("Could not create summary of the document! Enter a lower threshold value.")
            else:
                ui.textBrowseFile_summary.setPlainText("" + text.strip())

            score = int(calculate_rouge_score(summary, text)*100)
            ui.label_rouge.setText(str(score))

        except Exception as e:
            print(str(e))
            warning_message("Please enter a float value!")

            ui.lineEdit_similarityTh.setText("")
            ui.lineEdit_scoreTh.setText("")

def calculate_sentence_score(sentence, i):
    global theme_words
    sentence_len = len(sentence.split())

    # P1: Cümle özel isim kontrolü
    named_entity_count = sum(1 for word in sentences[i].split() if word.istitle()) - 1
    p1 = named_entity_count / len(sentences[i].split())

    # P2: Cümlede numerik veri kontrolü
    numeric_data_count = sum(1 for word in sentences[i].split() if isDigital(word))
    p2 = numeric_data_count / len(sentences[i].split())

    # P3: Cümle benzerliği threshold'unu geçen node'ların bulunması
    relevant_nodes = sum(1 for link in sentence_similarity(sentence) if link > similarity_th)
    p3 = relevant_nodes / (len(processed_sentences) - 1)

    # P4: Cümlede başlıktaki kelimelerin kontrolü
    title_word_count = sum(1 for word in sentence.split() if word in title_words)
    p4 = title_word_count / sentence_len

    # P5: Her kelimenin TF-IDF değerinin hesaplanması
    theme_word_count = sum(1 for word in sentence.split() if word in theme_words)
    p5 = theme_word_count / sentence_len

    # Cümle skoru hesaplama
    sentence_score = p1 + p2 + p3 + p4 + p5

    return sentence_score

def sentence_similarity(sentence):
    list = []
    for i in range(len(processed_sentences)):
        if sentence != str(processed_sentences[i]):
            sentence2 = str(processed_sentences[i])

            # Cümleleri vektörlere dönüştürmek için CountVectorizer kullanın
            vectorizer = CountVectorizer().fit_transform([sentence, sentence2])

            # Kosinüs benzerliği hesaplayın
            similarity = cosine_similarity(vectorizer[0], vectorizer[1])

            list.append(similarity[0][0])

    return list

def isDigital(word):
    for char in word:
        if char.isdigit():
            return True
    return False

def calculate_tf(word):
    text = ""
    for i in processed_sentences:
        text += i + " "
    text.strip()
    word_list = text.split()
    word_count = len(word_list)
    frequency = word_list.count(word)
    return frequency / word_count

def calculate_idf(word):
    total_sentences = len(processed_sentences)
    sentences_with_word = 0

    for sentence in processed_sentences:
        if word in sentence:
            sentences_with_word += 1

    return math.log10(total_sentences / (1 + sentences_with_word))

def calculate_tfidf():
    word_tfidf = {}
    text = ""

    for i in processed_sentences:
        text += i + " "
    text.strip()

    for word in text.split():
        if word not in word_tfidf:
            word_tfidf[word] = calculate_tf(word) * calculate_idf(word)

    return word_tfidf

def calculate_rouge_score(example, summary):
    if summary == "":
        score = 0
    else:
        rouge = Rouge()
        scores = rouge.get_scores(summary, example)
        score = scores[0]['rouge-l']['f']

    return score

def warning_message(warning):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Warning)
    message_box.setWindowTitle("Warning")
    message_box.setText(warning)
    message_box.setStandardButtons(QMessageBox.Ok)
    message_box.exec_()

ui.pushButton_browsefile.clicked.connect(browseFile)
ui.pushButton_visualize.clicked.connect(visualize_doc_button_clicked)
ui.pushButton_summary.clicked.connect(summary_button_clicked)

sys.exit(uygulama.exec_())

import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import filedialog
import os
from sentiment_methods import create_rounded_rectangle
import pickle
import pandas as pd
import re
from pythainlp.corpus.common import thai_stopwords
thai_stopwords = list(thai_stopwords())
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize
from sklearn.feature_extraction.text import CountVectorizer
from imblearn.over_sampling import SMOTE
import cleantext
#from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from datetime import datetime
import csv
import time
from tqdm import tqdm

file_name_path = "null"
data = []

def checkbox_balance():
    selected_value = check_var.get()
    global bal_selected

    if selected_value == 1:
        bal_selected = True
    else:
        bal_selected = False

def checkbox_weighting():
    global tf_selected
    global bool_selected
    if not tf_weight.get() and not bool_weight.get():
        messagebox.showwarning("Warning", "โปรดเลือกอย่างน้อย 1 ตัวเลือก \nPlease select at least one.")
        # tf_weight.set(1)
        tf_selected = False
        bool_selected = False
    else:
        if(tf_weight.get() == 1 & bool_weight.get() == 1):
            tf_selected = True
            bool_selected = True
            
        elif(bool_weight.get() == 1):
            tf_selected = False
            bool_selected = True

        else:
            tf_selected = True
            bool_selected = False

def checkbox_algorithm():
    global knn_selected
    global nai_selected
    if not knn_al.get() and not nai_al.get():
        messagebox.showwarning("Warning", "โปรดเลือกอย่างน้อย 1 ตัวเลือก \nPlease select at least one.")
        # knn_al.set(1)
        knn_selected = False
        nai_selected = False
    else:
        if(knn_al.get() == 1 & nai_al.get() == 1):
            knn_selected = True
            nai_selected = True
        elif(nai_al.get() == 1):
            knn_selected = False
            nai_selected = True
        else:
            knn_selected = True
            nai_selected = False

def direct_all_model():
    root.destroy()
    subprocess.run(['python', 'adminAllModel.py'])

def radio_selection():
    global selected_value
    selected_value = selected_option.get()

def add_details(selected_value,bal_selected,weight,algo):
    details = ""
    if selected_value == "0.40":
        details = "60_40"
    elif selected_value == "0.30":
        details = "70_30"
    else:
        details = "80_20"
    
    if bal_selected:
        details = details + "-Blance"
    
    if weight == "tf":
        details = details + "-tf"
    else:
        details = details + "-Boolean"
    
    if algo == "knn":
        details = details + "-KNN"
    else:
        details = details + "-Naive Bayes"
    return details

def open_file():
    global file_name_path
    global file_name
    file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if file_path:
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension != '.csv':
            tk.messagebox.showwarning("เกิดข้อผิดพลาด", "โปรดเลือกไฟล์ประเภท .csv เท่านั้น")
            return  
        else:
            file_name = os.path.basename(file_path)
            file_name_path = file_path
            file_label.config(text=f"{file_name}")

def balance_selected(X,Y):
    ROS = SMOTE()
    X, Y = ROS.fit_resample(X, Y)
    return X,Y

def knn(X,Y,selected_value,bal_selected,weight,dataVector):
    # if bal_selected:
    #     X, Y = balance_selected(X,Y)
        
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=float(selected_value), random_state=42)
    modelknn = KNeighborsClassifier(n_neighbors=4)
    modelknn.fit(X_train,Y_train)
    test_predictions = modelknn.predict(X_test)
    report = classification_report(Y_test, test_predictions,digits=2)
    now = datetime.now()
    dt_string = now.strftime("_%d-%m-%Y_%H-%M-%S")
    detail = add_details(selected_value,bal_selected,weight,"knn")
    file_name_without_extension = os.path.splitext(file_name)[0]
    path_model = file_name_without_extension + dt_string + detail + '.pkl'
    vector_model = file_name_without_extension + "vector" + dt_string + detail + '.pkl'
    data = [[file_name_without_extension + dt_string, detail, report, path_model,"not_active",vector_model]]
    pickle.dump(modelknn, open('selectModel/'+path_model,'wb'))
    pickle.dump(dataVector, open('selectModel/'+vector_model,'wb'))
    with open('createModel.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)


def naive(X,Y,selected_value,bal_selected,weight,dataVector):
    #print(Counter(Y))
    # if bal_selected:
    #     X, Y = balance_selected(X,Y)
        #print(Counter(Y))
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=float(selected_value), random_state=42)
    naive_bayes_classifier = GaussianNB()
    naive_bayes_classifier.fit(X_train, Y_train)
    test_predictions = naive_bayes_classifier.predict(X_test)
    report = classification_report(Y_test,test_predictions,digits=2)
    now = datetime.now()
    dt_string = now.strftime("_%d-%m-%Y_%H-%M-%S")
    detail = add_details(selected_value,bal_selected,weight,"naive")
    file_name_without_extension = os.path.splitext(file_name)[0]
    path_model = file_name_without_extension + dt_string + detail + '.pkl'
    vector_model = file_name_without_extension + "vector" + dt_string + detail + '.pkl'
    data = [[file_name_without_extension + dt_string, detail, report, path_model,"not_active",vector_model]]
    pickle.dump(naive_bayes_classifier, open('selectModel/'+path_model,'wb'))
    pickle.dump(dataVector, open('selectModel/'+vector_model,'wb'))
    with open('createModel.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)

def tfweight(doc_tokens):
    vectorizer = CountVectorizer(tokenizer=lambda x: x, preprocessor= lambda x: x, token_pattern=None)
    data = vectorizer.fit_transform(doc_tokens)
    dataVector = pd.DataFrame(data.toarray(), columns=vectorizer.get_feature_names_out())
    #print(dataVector)
    return dataVector

def boolweight(doc_tokens):
    vectorizer = CountVectorizer(tokenizer=lambda x: x, preprocessor= lambda x: x, binary=True, token_pattern=None) 
    data = vectorizer.fit_transform(doc_tokens)
    dataVector = pd.DataFrame(data.toarray(), columns=vectorizer.get_feature_names_out())
    #print(dataVector)
    return dataVector

def create_model():
    if(file_name_path != "null"):
        try:
            file_list = os.listdir("selectModel/")
            for file_name in file_list:
                file_path = os.path.join("selectModel/", file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            messagebox.showwarning("",f"Error deleting files: {e}")
        
        if (knn_al.get() or nai_al.get()) and (tf_weight.get() or bool_weight.get()):
            popup_window = tk.Toplevel(root)
            popup_window.title("Model Processing กรุณาอย่าปิดหน้าต่างนี้")
            popup_window.resizable(False, False)
            popup_window.geometry("500x100")
            center_window(popup_window)

            try:
                if file_name_path:
                    df = pd.read_csv(file_name_path, names=['text', 'sentiment'],usecols = [0,1])
                    df = df.dropna()
                    texts = df['text'].values.tolist()
                    pbar = tqdm(texts, bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:10}{r_bar}')
                    label = df['sentiment'].values.tolist()
                    label_tk = tk.Label(popup_window, font=('TH SarabunPSK', 14))
                    label_tk.pack(padx=20, pady=20)
                    doc_tokens = []
                    pattern = re.compile(u"[^\u0E00-\u0E7F' ]|^'|'$|''")
                    for text in pbar:
                        #text = str(text).replace("\n", "")
                        text = cleantext.clean(text,clean_all=True)
                        text = pattern.sub("", text)
                        tokens = word_tokenize(text, engine="newmm", keep_whitespace=False)
                        tokens = [w for w in tokens if w not in thai_stopwords]
                        #tokens = [w for w in tokens if not re.match(r'[a-zA-Z0-9 ]', w, re.I)]
                        tokens = [w for w in tokens if len(w) > 1]
                        tokens = [w for w in tokens if normalize(w)]

                        doc_tokens.append(tokens)
                        label_tk.config(text=pbar)
                        popup_window.update()
                        time.sleep(0.5)
                    
                    # for i in doc_tokens:
                    #     print(i)

                    with open('createModel.csv', 'w', newline='') as csv_file:
                            pass

                    if tf_selected:
                        dataVector = tfweight(doc_tokens)
                        X = dataVector.values[:,:]
                        Y = label
                        #print("before tf",Counter(Y))
                        if bal_selected:
                            X, Y = balance_selected(X,Y)
                        #print("tf",Counter(Y))
                        
                        if knn_selected:
                            label_tk.config(text="กำลังประมวลผล TF, KNN")
                            popup_window.update()
                            knn(X,Y,selected_value,bal_selected,"tf",dataVector)
                            
                        if nai_selected:
                            label_tk.config(text="กำลังประมวลผล TF, NAIVE BAYES")
                            popup_window.update()
                            naive(X,Y,selected_value,bal_selected,"tf",dataVector)
                            
                    if bool_selected:
                        dataVector = boolweight(doc_tokens)
                        X = dataVector.values[:,:]
                        Y = label
                        #print("before bool",Counter(Y))
                        if bal_selected:
                            X, Y = balance_selected(X,Y)
                        #print("bool",Counter(Y))
                        
                        if knn_selected:
                            label_tk.config(text="กำลังประมวลผล BOOLEAN, KNN")
                            popup_window.update()
                            knn(X,Y,selected_value,bal_selected,"bool",dataVector)
                            
                        if nai_selected:
                            label_tk.config(text="กำลังประมวลผล BOOLEAN, NAIVE BAYES")
                            popup_window.update()
                            naive(X,Y,selected_value,bal_selected,"bool",dataVector)

                    label_tk.config(text="กรุณารอสักครู่")
                    popup_window.update()
                    popup_window.destroy()
                    root.destroy()
                    subprocess.run(['python', 'adminSelectModel.py'])

            except Exception as e:
                messagebox.showwarning("Warning",f"{e}")
        else:
            messagebox.showwarning("Warning", "โปรดเลือกอย่างน้อย 1 ตัวเลือก \nPlease select at least one.")
    else:
        tk.messagebox.showwarning("เกิดข้อผิดพลาด", "กรุณาเลือกไฟล์")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def back():
    root.destroy()
    subprocess.run(["python", "userChooseFile.py"])

root = tk.Tk()
root.title("Admin Algorithm Choices")
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.config(bg="#faf9f5")
root.resizable(False, False)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg = "#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#408ef3')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: open_file())
text = canvas.create_text(60, 20, text="เลือกไฟล์", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: open_file())
canvas.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

file_label = tk.Label(root, text="", bg="#faf9f5",font=("TH SarabunPSK", 16, 'bold'))
file_label.place(relx=0.59, rely=0.02)

label1 = tk.Label(root, text="File: csv เท่านั้น", bg="#faf9f5",font=("TH SarabunPSK", 25))
label1.place(relx=0.5, rely=0.12, anchor=tk.CENTER)

label2 = tk.Label(root, text="*ข้อแนะนำ ข้อความในไฟล์ควรเป็นคอลลัมเดียว และข้อความ1ประโยคควรอยู่ใน1เซล/ช่อง", bg="#faf9f5",font=("TH SarabunPSK", 16))
label2.place(relx=0.5, rely=0.16, anchor=tk.CENTER)

label3 = tk.Label(root, text="ตัวอย่างไฟล์ csv", bg="#faf9f5",font=("TH SarabunPSK", 16))
label3.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

label4 = tk.Label(root, text="--------------------------------------------------", bg="#faf9f5",font=("TH SarabunPSK", 16))
label4.place(relx=0.5, rely=0.42, anchor=tk.CENTER)

image_path = "image/exampleAdmin.png"
image = tk.PhotoImage(file=image_path)
image_label = tk.Label(root, image=image, bg="#faf9f5")
image_label.image = image
image_label.place(relx=0.5, rely=0.31, anchor=tk.CENTER)

label5 = tk.Label(root, text="Train / Test" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold'))
label5.place(relx=0.5, rely=0.46, anchor=tk.CENTER)

selected_value = "0.30"
selected_option = tk.StringVar()
selected_option.set("0.30")

label4 = tk.Label(root, text="--------------------------------------------------", bg="#faf9f5",font=("TH SarabunPSK", 16))
label4.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

radio_button1 = tk.Radiobutton(root, text="60:40", font=("TH SarabunPSK", 16), variable=selected_option, value="0.40", command=radio_selection,bg="#faf9f5")
radio_button1.place(relx=0.4, rely=0.51, anchor=tk.CENTER)

radio_button2 = tk.Radiobutton(root, text="70:30", font=("TH SarabunPSK", 16), variable=selected_option, value="0.30", command=radio_selection,bg="#faf9f5")
radio_button2.place(relx=0.5, rely=0.51, anchor=tk.CENTER)

radio_button3 = tk.Radiobutton(root, text="80:20", font=("TH SarabunPSK", 16), variable=selected_option, value="0.20", command=radio_selection,bg="#faf9f5")
radio_button3.place(relx=0.6, rely=0.51, anchor=tk.CENTER)

bal_selected = False
check_var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Balance", variable=check_var, onvalue=1, offvalue=0, command=checkbox_balance, bg="#faf9f5",font=("TH SarabunPSK", 18))
checkbox.place(relx=0.5, rely=0.59, anchor=tk.CENTER)

label4 = tk.Label(root, text="--------------------------------------------------", bg="#faf9f5",font=("TH SarabunPSK", 16))
label4.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

tf_weight = tk.IntVar()
bool_weight = tk.IntVar()

label5 = tk.Label(root, text="Weighting" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold'))
label5.place(relx=0.5, rely=0.67, anchor=tk.CENTER)

tf_selected = True
bool_selected = False

tf_weight.set(1)
checkbox2 = tk.Checkbutton(root, text="tf", variable=tf_weight, onvalue=1, offvalue=0, command=checkbox_weighting, bg="#faf9f5", font=("TH SarabunPSK", 16))
checkbox2.place(relx=0.45, rely=0.718, anchor=tk.CENTER)
checkbox3 = tk.Checkbutton(root, text="boolean", variable=bool_weight, onvalue=1, offvalue=0, command=checkbox_weighting, bg="#faf9f5", font=("TH SarabunPSK", 16))
checkbox3.place(relx=0.55, rely=0.718, anchor=tk.CENTER)

label4 = tk.Label(root, text="--------------------------------------------------", bg="#faf9f5",font=("TH SarabunPSK", 16))
label4.place(relx=0.5, rely=0.753, anchor=tk.CENTER)

label5 = tk.Label(root, text="Algorithm" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold'))
label5.place(relx=0.5, rely=0.79, anchor=tk.CENTER)

knn_al = tk.IntVar()
nai_al = tk.IntVar()

knn_selected = True
nai_selected = False

knn_al.set(1)
checkbox4 = tk.Checkbutton(root, text="KNN", variable=knn_al, onvalue=1, offvalue=0, command=checkbox_algorithm, bg="#faf9f5", font=("TH SarabunPSK", 16))
checkbox4.place(relx=0.45, rely=0.84, anchor=tk.CENTER)
checkbox5 = tk.Checkbutton(root, text="Naive Bayes", variable=nai_al, onvalue=1, offvalue=0, command=checkbox_algorithm, bg="#faf9f5", font=("TH SarabunPSK", 16))
checkbox5.place(relx=0.55, rely=0.84, anchor=tk.CENTER)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#742b86')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: direct_all_model())
text = canvas.create_text(60, 20, text="ดูโมเดลทั้งหมด", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: direct_all_model())
canvas.place(relx=0.35, rely=0.91, anchor=tk.CENTER)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#44ae9b')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: create_model())
text = canvas.create_text(60, 20, text="สร้างโมเดล", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: create_model())
canvas.place(relx=0.5, rely=0.91, anchor=tk.CENTER)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#ae4444')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
text = canvas.create_text(60, 20, text="กลับหน้าผู้ใช้", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: back())
canvas.place(relx=0.65, rely=0.91, anchor=tk.CENTER)

root.mainloop()
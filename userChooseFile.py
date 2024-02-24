import tkinter as tk
from sentiment_methods import create_rounded_rectangle
from tkinter import filedialog
import os
import subprocess
import pandas as pd
import pickle
from datetime import datetime
import shutil
import time
import re
from pythainlp.corpus.common import thai_stopwords
thai_stopwords = list(thai_stopwords())
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize
from tqdm import tqdm
import csv

if __name__ == '__main__':
      
    file_name_path = "null"

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

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def choose_model():
        if(file_name_path != "null"):
            popup_window = tk.Toplevel(root)
            popup_window.title("Programme is Processing กรุณาอย่าปิดหน้าต่างนี้")
            popup_window.resizable(False, False)
            popup_window.geometry("500x100")
            center_window(popup_window)

            for filename in os.listdir('textprepare/'):
                file_path = os.path.join('textprepare/', filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    tk.messagebox.showwarning("",f"Failed to delete {file_path}. Error: {e}")
            try:
                if file_name_path:
                    df = pd.read_csv(file_name_path, names=['text'],usecols = [0])
                    pattern_df = re.compile("[\u0E00-\u0E7F]")
                    df = df[df['text'].str.contains(pattern_df)]
                    df = df.dropna()
                    texts = df['text'].values.tolist()
                    pbar = tqdm(texts, bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:10}{r_bar}')
                    label_tk = tk.Label(popup_window, font=('TH SarabunPSK', 14))
                    label_tk.pack(padx=20, pady=20)
                    pattern = re.compile(u"[^\u0E00-\u0E7F' ]|^'|'$|''")
                    doc_tokens = []  
                    for text in pbar:
                        #text = text.replace("\n", "") 
                        #text = cleantext.clean(text,clean_all=True)
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
                        
                    
                    now = datetime.now()
                    dt_string = now.strftime("_%d-%m-%Y_%H-%M-%S")
                    file_name_without_extension = os.path.splitext(file_name)[0]
                    save_file_name = file_name_without_extension + dt_string + '.pkl'
                    pickle.dump(doc_tokens, open('textprepare/'+save_file_name,'wb'))
                    with open('data_file.csv', 'w') as csv_file:
                        pass
                    with open('data_file.csv', 'a', newline='', encoding="utf-8") as csv_file:
                        csv_writer = csv.writer(csv_file)
                        for text in df['text']:
                            csv_writer.writerow([text])
                    with open("textprepare/word_tokens.txt", "w") as f:
                        f.write(save_file_name)
                    popup_window.destroy()
                    root.destroy()
                    subprocess.run(["python", "userChooseModel.py"])
            except Exception as e:
                tk.messagebox.showwarning("",f"{e}")
        else:
            tk.messagebox.showwarning("เกิดข้อผิดพลาด", "กรุณาเลือกไฟล์")
        
    def direct_to_login():
        root.destroy()
        subprocess.run(["python", "adminLogin.py"])

    root = tk.Tk()
    root.title("User Choose File")
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
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#faf9f5')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: direct_to_login())
    text = canvas.create_text(60, 20, text="สำหรับผู้ดูแลระบบ", fill='black', font=('TH SarabunPSK', 12, 'bold', 'underline'))
    canvas.tag_bind(text, '<Button-1>', lambda event: direct_to_login())
    canvas.place(relx=0.93, rely=0.04, anchor=tk.CENTER)

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg = "#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#408ef3')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: open_file())
    text = canvas.create_text(60, 20, text="เลือกไฟล์", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: open_file())
    canvas.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

    file_label = tk.Label(root, text="", bg="#faf9f5",font=("TH SarabunPSK", 16, 'bold'))
    file_label.place(relx=0.59, rely=0.15)

    label1 = tk.Label(root, text="File: csv เท่านั้น", bg="#faf9f5",font=("TH SarabunPSK", 25))
    label1.place(relx=0.5, rely=0.26, anchor=tk.CENTER)

    label2 = tk.Label(root, text="*ข้อแนะนำ ข้อความในไฟล์ควรเป็นคอลลัมเดียว และข้อความ1ประโยคควรอยู่ใน1เซล/ช่อง", bg="#faf9f5",font=("TH SarabunPSK", 16))
    label2.place(relx=0.5, rely=0.31, anchor=tk.CENTER)

    label3 = tk.Label(root, text="ตัวอย่างไฟล์ csv", bg="#faf9f5",font=("TH SarabunPSK", 16))
    label3.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    image_path = "image/exampleUser.png"
    image = tk.PhotoImage(file=image_path)
    smaller_image = image.subsample(2, 2)
    image_label = tk.Label(root, image=smaller_image, bg="#faf9f5")
    image_label.image = smaller_image
    image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    canvas = tk.Canvas(root, width=160, height=60, highlightthickness=0, bg = "#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 135, 55, radius=10, fill='#44ae9b')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: choose_model())
    text = canvas.create_text(70, 30, text="เลือกโมเดล", fill='white', font=('TH SarabunPSK', 20, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: choose_model())
    canvas.place(relx=0.5, rely=0.69, anchor=tk.CENTER)

    root.mainloop()
import tkinter as tk
from sentiment_methods import create_rounded_rectangle,ScrollableFrame
import csv
import subprocess
from tkinter import messagebox
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import os
import re
import time

if __name__ == '__main__':

    select_model = ""
    select_cv = ""
    previous_canvas = ""
    def choose_model(event, i, canvas, rounded_rect):
        global previous_canvas
        global select_model
        global select_cv
        current_color = canvas.itemcget(rounded_rect, 'fill')
        #if current color is equal to gray the new color will be green
        #if current color is not equal to gray the new color wil be gray
        new_color = '#44ae9b' if current_color == '#696868' else '#696868'
        canvas.itemconfig(rounded_rect, fill=new_color)
        if previous_canvas != "" and previous_canvas != canvas:
            previous_canvas.itemconfig(rounded_rect, fill='#696868')
        previous_canvas = canvas
        #if not gray is green
        if current_color != '#696868':
            select_model = ""
        else:
            select_model = rows[i][3]
            select_cv = rows[i][5]
    
    def back():
        root.destroy()
        subprocess.run(['python', 'userChooseFile.py'])

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    predict_result = []
    def confirm_model():
        try:
            class_result = ""
            if select_model == "":
                messagebox.showwarning("Warning", "โปรดเลือกอย่างน้อย 1 โมเดล")
            else: 
                popup_window = tk.Toplevel(root)
                popup_window.title("Model is Processing กรุณาอย่าปิดหน้าต่างนี้")
                popup_window.resizable(False, False)
                popup_window.geometry("500x100")
                center_window(popup_window)
                label_tk = tk.Label(popup_window, font=('TH SarabunPSK', 14))
                label_tk.pack(padx=20, pady=20)
                label_tk.config(text="กำลังประมวลผล")
                popup_window.update()

                word_token_lines = ""
                # with open('predictedResult.csv', 'w', newline='') as csv_file:
                #     pass
                with open("textprepare\word_tokens.txt", "r") as f:
                    word_token_lines = f.readlines()
                # split_result = word_token_lines[0].split(',')
                # file_name = split_result[0]
                # data_file_path = split_result[1]

                file_path_m = os.path.join("allModels", select_model)
                m = pickle.load(open(file_path_m, 'rb'))

                file_path_cv = os.path.join("allModels", select_cv)
                cv = pickle.load(open(file_path_cv, 'rb'))
                vectorizer = CountVectorizer(vocabulary=cv)

                file_path_text = os.path.join("textprepare", word_token_lines[0])
                doc_tokens = pickle.load(open(file_path_text, 'rb'))
                
                df = pd.read_csv("data_file.csv", names=['text'],usecols = [0])  
                df = df.dropna()  
                
                counting_dot = 0
                for doc in doc_tokens:
                    data2 = vectorizer.transform(pd.Series(str(doc)))
                    dataVector2 = pd.DataFrame(data2.toarray(), columns=vectorizer.get_feature_names_out())
                    X2 = dataVector2.values[:,:]
                    my_predictions = m.predict(X2)
                    if str(my_predictions) == "['pos']":
                        class_result = "positive"
                    elif str(my_predictions) == "['neg']":
                        class_result = "negative"
                    elif str(my_predictions) == "['neu']":
                        class_result = "neutral"
                    predict_result.append(class_result)
                    counting_dot += 1
                    if counting_dot == 1:
                        label_tk.config(text="กำลังประมวลผล")
                        popup_window.update()
                    elif counting_dot == 2:
                        label_tk.config(text="กำลังประมวลผล.")
                        popup_window.update()
                    elif counting_dot == 3:
                        label_tk.config(text="กำลังประมวลผล..")
                        popup_window.update()
                    elif counting_dot == 4:
                        counting_dot = 0
                        label_tk.config(text="กำลังประมวลผล...")
                        popup_window.update()
                    time.sleep(0.3)
                result_df = pd.DataFrame({'text': df['text'], 'class': predict_result})
                result_df.to_excel('predictedResult.xlsx', index=False)
                # with open('predictedResult.csv', 'a', newline='', encoding="utf-8") as csv_file:
                #     csv_writer = csv.writer(csv_file)
                #     write_row = df['text'][index],class_result
                #     csv_writer.writerow(write_row)
                popup_window.destroy()
                messagebox.showinfo("","วิเคราะห์เสร็จเรียบร้อย")
                root.destroy()
                subprocess.run(['python', 'userResult.py'])
        except Exception as e:
            tk.messagebox.showwarning("",f"{e}")
    
    root = tk.Tk()
    root.title("User Choose Model")
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.config(bg="#faf9f5")
    root.resizable(False, False)

    rows = []
    try: 
        with open('allModels.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                rows.append(row)
    except:
        messagebox.showwarning("ผิดพลาด","ไม่มีโมเดล. โปรดติดต่อแอดมิน")
        root.destroy()
        subprocess.run(['python', 'userChooseFile.py'])

    
    head_text = tk.Label(root, text="เลือกโมเดล" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold'))
    head_text.place(relx=0.5, rely=0.04, anchor=tk.CENTER)

    rounded_frame = tk.Frame(root, width=720, height=500, bg="#faf9f5")
    rounded_frame.place(relx=0.5, rely=0.48, anchor=tk.CENTER)

    frame = ScrollableFrame(rounded_frame, width=720, height=500, hscroll=True, vscroll=True)
    frame.pack(fill="both", expand=True)

    translation_table = str.maketrans({'_': ':', '-': ','})
    translation_filename = str.maketrans({'_': ' ', '-': ':'}) 

    index = 0
    index_row = 0
    index_column = 0

    while index < len(rows):
        if rows[index][4] == "active":
            inner_frame = tk.Canvas(frame, width=360, height=260, bg="#d0d5e7")
            inner_frame.grid(row=index_row, column=index_column)

            row_lines = rows[index][2].split('\n')
            non_empty_lines = [line.strip() for line in row_lines if line.strip()]
            # row_text = '\n'.join(non_empty_lines)

            # label_report1 = tk.Label(inner_frame, text=row_text, bg="#d0d5e7",font=("TH SarabunPSK", 13),justify='right')
            # label_report1.place(relx=0.5, rely=0.53, anchor= tk.CENTER)

            line_rely = 0.26
            line_relx = 0.55
            for index_line in range(len(non_empty_lines)):
                if index_line == 0:
                    new_string = re.sub(r'\s+', '  ', non_empty_lines[index_line])
                    label_report1 = tk.Label(inner_frame, text=new_string, bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                    label_report1.place(relx=0.64, rely=line_rely, anchor= tk.CENTER)
                elif index_line <=3 :
                    label_report1 = tk.Label(inner_frame, text=non_empty_lines[index_line], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                    label_report1.place(relx=0.57, rely=line_rely, anchor= tk.CENTER)
                elif index_line == 4:
                    new_string = re.sub(r'\s+', '      ', non_empty_lines[index_line])
                    label_report1 = tk.Label(inner_frame, text=new_string, bg="#d0d5e7",font=("TH SarabunPSK", 15,"bold"),justify='right')
                    label_report1.place(relx=line_relx+0.10, rely=line_rely, anchor= tk.CENTER)
                elif index_line == 5:
                    label_report1 = tk.Label(inner_frame, text=non_empty_lines[index_line], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                    label_report1.place(relx=line_relx-0.04, rely=line_rely, anchor= tk.CENTER)
                else:
                    label_report1 = tk.Label(inner_frame, text=non_empty_lines[index_line], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                    label_report1.place(relx=line_relx-0.06, rely=line_rely, anchor= tk.CENTER)

                line_rely = line_rely+0.09

            label = tk.Label(inner_frame, text=(str)(rows[index][1]).translate(translation_table), bg="#d0d5e7", fg = "#1c36ad",font=("TH SarabunPSK", 18, "bold"), padx=5)
            label.place(relx=0.5, rely=0.16, anchor= tk.CENTER)

            label = tk.Label(inner_frame, text=(str)(rows[index][0]).translate(translation_filename), bg="#d0d5e7",font=("TH SarabunPSK", 13), padx=5)
            label.place(relx=0.5, rely=0.06, anchor= tk.CENTER)

            canvas = tk.Canvas(inner_frame, width=120, height=40, highlightthickness=0, bg = "#d0d5e7")
            canvas.pack()

            rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#696868')
            canvas.tag_bind(rounded_rect, '<Button-1>', lambda event, i=index, c=canvas, r=rounded_rect: choose_model(event, i, c, r))

            text = canvas.create_text(60, 20, text="เลือก", fill='white', font=('TH SarabunPSK', 14, 'bold'))
            canvas.tag_bind(text, '<Button-1>', lambda event, i=index, c=canvas, r=rounded_rect: choose_model(event, i, c, r))

            canvas.place(relx=0.5, rely=0.91, anchor=tk.CENTER)

            if index_column != 0:
                index_row = index_row + 1
                index_column = 0
            else:
                index_column = 1

        index += 1

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#44ae9b')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: confirm_model())
    text = canvas.create_text(60, 20, text="ยืนยันโมเดล", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: confirm_model())
    canvas.place(relx=0.42, rely=0.94, anchor=tk.CENTER)

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#d63852')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
    text = canvas.create_text(60, 20, text="กลับหน้าแรก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: back())
    canvas.place(relx=0.57, rely=0.94, anchor=tk.CENTER)

    root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import *
import csv
from tkinter import messagebox
import subprocess
import shutil
import os
import re
from sentiment_methods import create_rounded_rectangle

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Admin Select Algorithms")
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
    with open('createModel.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            rows.append(row)
            
    rounded_frame = tk.Frame(root, width=700, height=580, bg="#faf9f5")
    rounded_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    style = ttk.Style()
    style.configure("Custom.TCheckbutton", background="#d0d5e7", padding=10)

    checkboxes_select = []
    vector_select = []
    def checkbox_selection(checkbox_number):
        if checkbox_vars[checkbox_number].get():
            checkboxes_select.append(rows[checkbox_number][3])
            vector_select.append(rows[checkbox_number][5])
        else:
            checkboxes_select.pop(checkboxes_select.index(rows[checkbox_number][3]))
            vector_select.append(vector_select.index(rows[checkbox_number][5]))

    def find_file_name_index(my_list, target):
        for i, row in enumerate(my_list):
            for j, element in enumerate(row):
                if element == target:
                    return i 
        return -1 

    def save_algo():
        if checkboxes_select != []:
            for x in range(len(checkboxes_select)):
                shutil.move('selectModel/'+checkboxes_select[x],'allModels/'+checkboxes_select[x])
                shutil.move('selectModel/'+vector_select[x],'allModels/'+vector_select[x])
                detail_result = find_file_name_index(rows,checkboxes_select[x])
                data = [rows[detail_result]]
                with open('allModels.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    for row in data:
                        csv_writer.writerow(row)   

            for filename in os.listdir('selectModel/'):
                file_path = os.path.join('selectModel/', filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    tk.messagebox.showwarning("Warning",f"Failed to delete {file_path}. Error: {e}")

            with open('createModel.csv', 'w', newline='') as csv_file:
                pass
            tk.messagebox.showinfo("","บันทึกสำเร็จ \nSaved Successfully")
            root.destroy()
            subprocess.run(['python', 'adminAllModel.py'])
        else:
            tk.messagebox.showwarning("Warning", "โปรดเลือกอย่างน้อย 1 ตัวเลือก \nPlease select at least one.")

    def back():
        for filename in os.listdir('selectModel/'):
                file_path = os.path.join('selectModel/', filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    messagebox.showwarning("Warning",f"Failed to delete {file_path}. Error: {e}")
        with open('createModel.csv', 'w', newline='') as csv_file:
                pass
        root.destroy()
        subprocess.run(['python', 'adminCreateModel.py'])

    checkbox_vars = [tk.IntVar() for _ in range(len(rows))]

    checkboxes = []
    translation_table = str.maketrans({'_': ':', '-': ','})
    for i in range(len(rows)):
        row = i // 2
        col = i % 2
        
        framex = 0.25 + col * 0.50
        framey = 0.22 + row * 0.45

        inner_frame = tk.Frame(rounded_frame, bg="#d0d5e7", bd=0, highlightthickness=0)
        inner_frame.place(relx=framex, rely=framey, anchor=tk.CENTER, width=330, height=245)
        
        row_lines = rows[i][2].split('\n')
        non_empty_lines = [line.strip() for line in row_lines if line.strip()]
        #row_text = '\n'.join(non_empty_lines)

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
                label_report1.place(relx=line_relx+0.11, rely=line_rely, anchor= tk.CENTER)
            elif index_line == 5:
                label_report1 = tk.Label(inner_frame, text=non_empty_lines[index_line], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                label_report1.place(relx=line_relx-0.04, rely=line_rely, anchor= tk.CENTER)
            else:
                label_report1 = tk.Label(inner_frame, text=non_empty_lines[index_line], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
                label_report1.place(relx=line_relx-0.06, rely=line_rely, anchor= tk.CENTER)

            line_rely = line_rely+0.09

        label = tk.Label(inner_frame, text=(str)(rows[i][1]).translate(translation_table), bg="#d0d5e7",font=("TH SarabunPSK", 20, "bold"), padx=5)
        label.place(relx=0.5, rely=0.1, anchor= tk.CENTER)
        
        checkbox = ttk.Checkbutton(inner_frame, text="", variable=checkbox_vars[i], onvalue=1, offvalue=0, style="Custom.TCheckbutton", command=lambda i=i: checkbox_selection(i))
        checkbox.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

        checkboxes.append(checkbox)

    canvas = tk.Canvas(rounded_frame, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#44ae9b')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: save_algo())
    text = canvas.create_text(60, 20, text="บันทึก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: save_algo())
    canvas.place(relx=0.41, rely=0.94, anchor=tk.CENTER)

    canvas = tk.Canvas(rounded_frame, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#6f5184')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
    text = canvas.create_text(60, 20, text="ย้อนกลับ", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: back())
    canvas.place(relx=0.59, rely=0.94, anchor=tk.CENTER)

    root.mainloop()
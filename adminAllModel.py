import tkinter as tk
import csv
from tkinter import messagebox
import subprocess
import os
from sentiment_methods import create_rounded_rectangle,ScrollableFrame
import re

if __name__ == '__main__':
    
    active_algos = []
    def active_algo(event, i, canvas, rounded_rect, text_item):

        current_color = canvas.itemcget(rounded_rect, 'fill')
        current_text = canvas.itemcget(text_item, 'text')

        if current_color == '#44ae9b' and current_text == "กำลังใช้งาน":
            canvas.itemconfig(rounded_rect, fill='#696868')
            canvas.itemconfig(text_item, text="ไม่ถูกใช้งาน")
            if rows[i][3] in active_algos:
                active_algos.pop(active_algos.index(rows[i][3])) 
        else:
            canvas.itemconfig(rounded_rect, fill='#44ae9b')
            canvas.itemconfig(text_item, text="กำลังใช้งาน")
            if rows[i][3] not in active_algos:
                active_algos.append(rows[i][3]) 

    remove_algos = []
    remove_vector = []
    def remove_algo(event, i, canvas, rounded_rect):
        current_color = canvas.itemcget(rounded_rect, 'fill')
        new_color = '#d63852' if current_color == '#696868' else '#696868'
        canvas.itemconfig(rounded_rect, fill=new_color)
        if current_color == '#696868':
            if rows[i][3] not in remove_algos:
                remove_algos.append(rows[i][3])
                remove_vector.append(rows[i][5])
        else:
            if rows[i][3] in remove_algos:
                remove_algos.pop(remove_algos.index(rows[i][3])) 
                remove_vector.pop(remove_vector.index(rows[i][5])) 
          
    def find_file_name_index(my_list, target):
        for i, row in enumerate(my_list):
            for j, element in enumerate(row):
                if element == target:
                    return i 
        return -1 
    
    def save_algo():
        isActive = False
        for algo in remove_algos:
            if algo in active_algos:
                isActive = True
                break
                    
        if isActive:
            messagebox.showwarning("Warning", "ไม่สามารถลบโมเดลที่ถูกใช้งานอยู่ได้")
        else:
            with open('allModels.csv', 'w', newline='') as active_file:
                pass
            active_rows = []
            for x in range(len(active_algos)):
                detail_result = find_file_name_index(rows,active_algos[x])
                active_rows.append(detail_result)
            
            for i in range(len(rows)):
                if i in active_rows:
                    rows[i][4] = "active"
                else:
                    rows[i][4] = "not_active"

            remove_rows = []
            for x in range(len(remove_algos)):
                remove_result = find_file_name_index(rows,remove_algos[x])
                remove_rows.append(remove_result)

            data = [row for i, row in enumerate(rows) if i not in remove_rows]
            with open('allModels.csv', 'a', newline='') as active_file:
                active_writer = csv.writer(active_file)
                for row in data:
                    active_writer.writerow(row)

            try:
                file_list = os.listdir("allModels/")

                for file_name in file_list:
                    file_path = os.path.join("allModels/", file_name)
                    if os.path.isfile(file_path) and file_name in remove_algos:
                        os.remove(file_path)
                    if os.path.isfile(file_path) and file_name in remove_vector:
                        os.remove(file_path)
                    
            except Exception as e:
                messagebox.showwarning("",f"Error deleting files: {e}")

            messagebox.showinfo("","บันทึกสำเร็จ \nSaved Successfully")
            root.destroy()
            subprocess.run(['python', 'adminAllModel.py'])

    def back():
        root.destroy()
        subprocess.run(['python', 'userChooseFile.py'])

    def direct_to_create_model():
        root.destroy()
        subprocess.run(['python', 'adminCreateModel.py'])

    root = tk.Tk()
    root.title("All Algorithms")
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.config(bg="#faf9f5")
    root.resizable(False, False)

    head_text = tk.Label(root, text="โมเดลทั้งหมด" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold',"underline"))
    head_text.place(relx=0.5, rely=0.04, anchor=tk.CENTER)

    rows = [] 
    with open('allModels.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            rows.append(row)

    for algo in range(len(rows)):
        if rows[algo][4] == "active":
            active_algos.append(rows[algo][3])


    rounded_frame = tk.Frame(root, width=720, height=500, bg="#faf9f5")
    rounded_frame.place(relx=0.5, rely=0.48, anchor=tk.CENTER)

    frame = ScrollableFrame(rounded_frame, width=720, height=500, hscroll=True, vscroll=True)
    frame.pack(fill="both", expand=True)

    translation_table = str.maketrans({'_': ':', '-': ','})
    translation_filename = str.maketrans({'_': ' ', '-': ':'}) 

    index = 0
    index_row = 0
    index_column = 0
    canvas_list = []
    rounded_rect_list = []
    text_list = []
    canvas_delete_list = []
    rounded_rect_delete_list = []

    while index < len(rows):

        inner_frame = tk.Canvas(frame, width=360, height=260, bg="#d0d5e7")
        inner_frame.grid(row=index_row, column=index_column)
        
        row_lines = rows[index][2].split('\n')
        non_empty_lines = [line.strip() for line in row_lines if line.strip()]
        #row_text = '\n'.join(non_empty_lines)

        # label_report1 = tk.Label(inner_frame, text=row_text, bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='right')
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

        label = tk.Label(inner_frame, text=(str)(rows[index][1]).translate(translation_table), bg="#d0d5e7", fg = "#1c36ad",font=("TH SarabunPSK", 19, "bold"), padx=5)
        label.place(relx=0.5, rely=0.16, anchor= tk.CENTER)

        label = tk.Label(inner_frame, text=(str)(rows[index][0]).translate(translation_filename), bg="#d0d5e7",font=("TH SarabunPSK", 13), padx=5)
        label.place(relx=0.5, rely=0.06, anchor= tk.CENTER)

        canvas = tk.Canvas(inner_frame, width=105, height=40, highlightthickness=0, bg="#d0d5e7")
        canvas.pack()

        rounded_rect = create_rounded_rectangle(canvas, 5, 5, 100, 35, radius=10, fill='#696868') #c2c2c2

        if rows[index][4] == "active":
            text_value = "กำลังใช้งาน"
            canvas.itemconfig(rounded_rect, fill="#44ae9b")
        else:
            text_value = "ไม่ถูกใช้งาน" 

        try:
            text = canvas.create_text(55, 20, text=text_value, fill='white', font=('TH SarabunPSK', 16, 'bold'))
        except NameError:
            pass

        canvas.tag_bind(rounded_rect, '<Button-1>', lambda event, i=index, c=canvas, r=rounded_rect, t=text: active_algo(event, i, c, r, t))
        canvas.tag_bind(text, '<Button-1>', lambda event, i=index, c=canvas, r=rounded_rect, t=text: active_algo(event, i, c, r, t))

        canvas.place(relx=0.4, rely=0.91, anchor=tk.CENTER)

        canvas_list.append(canvas)
        rounded_rect_list.append(rounded_rect)
        text_list.append(text)

        canvas_delete = tk.Canvas(inner_frame, width=75, height=40, highlightthickness=0, bg="#d0d5e7")
        canvas_delete.pack()

        rounded_rect_delete = create_rounded_rectangle(canvas_delete, 5, 5, 70, 35, radius=10, fill='#696868')
        canvas_delete.tag_bind(rounded_rect, '<Button-1>', lambda event, i=index, c=canvas_delete, r=rounded_rect_delete: remove_algo(event, i, c, r))

        text_delete = canvas_delete.create_text(40, 20, text="ลบ", fill='white', font=('TH SarabunPSK', 16, 'bold'))
        canvas_delete.tag_bind(text, '<Button-1>', lambda event, i=index, c=canvas_delete, r=rounded_rect_delete: remove_algo(event, i, c, r))

        canvas_delete.place(relx=0.64, rely=0.91, anchor=tk.CENTER)

        canvas_delete_list.append(canvas_delete)
        rounded_rect_delete_list.append(rounded_rect_delete)

        if index % 2 != 0:
            index_row = index_row + 1
            index_column = 0
        else:
            index_column = 1

        index += 1

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#44ae9b')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: save_algo())
    text = canvas.create_text(60, 20, text="บันทึก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: save_algo())
    canvas.place(relx=0.35, rely=0.94, anchor=tk.CENTER)

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#6f5184')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: direct_to_create_model())
    text = canvas.create_text(60, 20, text="สร้างโมเดล", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: direct_to_create_model())
    canvas.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#ae4444')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
    text = canvas.create_text(60, 20, text="กลับหน้าผู้ใช้", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: back())
    canvas.place(relx=0.65, rely=0.94, anchor=tk.CENTER)

    root.mainloop()


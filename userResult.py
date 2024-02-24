import tkinter as tk
from sentiment_methods import create_rounded_rectangle,ScrollableFrame
import subprocess
import pandas as pd
from tkinter import filedialog
import os

if __name__ == '__main__':
    
    root = tk.Tk()
    root.title("User Result")
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.config(bg="#faf9f5")
    root.resizable(False, False)

    excel_df = pd.read_excel('predictedResult.xlsx')
    excel_df['texts'] = excel_df['text'].apply(lambda x: (x.replace('\n', ' '))[:55] + '...' if len(x) > 55 else x.replace('\n', ' '))
    
    class_counts = excel_df['class'].value_counts()
    total_samples = len(excel_df)
    class_percentages = (class_counts / total_samples) * 100
    formatted_percentages = {}
    for class_label in ['positive', 'neutral', 'negative']:
        try:
            percentage = class_percentages[class_label]
        except KeyError:
            percentage = 0
        formatted_percentages[class_label] = f"{percentage:.0f}%"

    with open("textprepare\word_tokens.txt", "r") as f:
        word_token_lines = f.readlines()
    # split_result = word_token_lines[0].split(',')
    file_name = word_token_lines[0].replace('.pkl', '')
    # file_path = split_result[1]

    head_text = tk.Label(root, text="ผลการวิเคราะห์" ,bg="#faf9f5",font=("TH SarabunPSK", 20, 'bold'))
    head_text.place(relx=0.5, rely=0.12, anchor=tk.CENTER)

    pos_image = tk.PhotoImage(file="image/positive.png")

    pos_emoji = tk.Label(root, image=pos_image,bg="#faf9f5")
    pos_emoji.place(relx=0.245, rely=0.265, anchor=tk.CENTER)

    pos_text_label_perc = tk.Label(root, text=formatted_percentages['positive'] ,bg="#faf9f5",font=("TH SarabunPSK", 32, 'bold'))
    pos_text_label_perc.place(relx=0.3, rely=0.2, anchor=tk.CENTER)

    pos_text_label = tk.Label(root, text="Positive" ,bg="#faf9f5",font=("TH SarabunPSK", 18, 'bold'))
    pos_text_label.place(relx=0.3, rely=0.27, anchor=tk.CENTER)

    neu_image = tk.PhotoImage(file="image/neutral.png")

    neu_emoji = tk.Label(root, image=neu_image,bg="#faf9f5")
    neu_emoji.place(relx=0.445, rely=0.265, anchor=tk.CENTER)

    neu_text_label_perc = tk.Label(root, text=formatted_percentages['neutral'] ,bg="#faf9f5",font=("TH SarabunPSK", 32, 'bold'))
    neu_text_label_perc.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    neu_text_label = tk.Label(root, text="Neutral" ,bg="#faf9f5",font=("TH SarabunPSK", 18, 'bold'))
    neu_text_label.place(relx=0.5, rely=0.27, anchor=tk.CENTER)

    neg_image = tk.PhotoImage(file="image/negative.png")

    neg_emoji = tk.Label(root, image=neg_image,bg="#faf9f5")
    neg_emoji.place(relx=0.64, rely=0.265, anchor=tk.CENTER)

    neg_text_label_perc = tk.Label(root, text=formatted_percentages['negative'] ,bg="#faf9f5",font=("TH SarabunPSK", 32, 'bold'))
    neg_text_label_perc.place(relx=0.7, rely=0.2, anchor=tk.CENTER)

    neg_text_label = tk.Label(root, text="Negative" ,bg="#faf9f5",font=("TH SarabunPSK", 18, 'bold'))
    neg_text_label.place(relx=0.7, rely=0.27, anchor=tk.CENTER)

    rounded_frame = tk.Frame(root, width=500, height=360, bg="#32a8a8")
    rounded_frame.place(relx=0.5, rely=0.59, anchor=tk.CENTER)

    frame = ScrollableFrame(rounded_frame, width=500, height=360, hscroll=True, vscroll=True)
    frame.pack(fill="both", expand=True)

    index = 0
    index_row = 0
    button_dict = {} 
    imgs = []

    while index < len(excel_df):

        inner_frame = tk.Canvas(frame, width=280, height=40, bg="#d0d5e7")
        inner_frame.grid(row=index_row, column=0, ipadx=60)

        label_text = tk.Label(inner_frame, text=excel_df['texts'][index], bg="#d0d5e7",font=("TH SarabunPSK", 15),justify='left')
        label_text.place(relx=0.05, rely=0.5, anchor='w')

        inner_frame_label = tk.Canvas(frame, width=90, height=40, bg="#faf9f5")
        inner_frame_label.grid(row=index_row, column=1)

        imgs.append(tk.PhotoImage(file=os.path.join("image", f"{excel_df['class'][index]}.png")))

        label_label = tk.Label(inner_frame_label, image=imgs[-1], bg="#faf9f5")
        label_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        index += 1
        index_row += 1

    
    def save_file(content, file_name):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                                initialfile=file_name)
        if file_path:
            try:
                result_df = pd.DataFrame({'text': content['texts'], 'class': content['class']})
                result_df.to_excel(file_path, index=False)

                tk.messagebox.showinfo("",f"File saved successfully at: {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#408ef3')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: save_file(excel_df,file_name))
    text = canvas.create_text(60, 20, text="บันทึก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: save_file(excel_df,file_name))
    canvas.place(relx=0.36, rely=0.94, anchor=tk.CENTER)

    def re_model():
        root.destroy()
        subprocess.run(["python", "userChooseModel.py"])

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#d1c649')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: re_model())
    text = canvas.create_text(60, 20, text="เลือกโมเดลใหม่", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: re_model())
    canvas.place(relx=0.51, rely=0.94, anchor=tk.CENTER)

    def back():
        root.destroy()
        subprocess.run(['python', 'userChooseFile.py'])

    canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg="#faf9f5")
    canvas.pack()
    rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#d63852')
    canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
    text = canvas.create_text(60, 20, text="กลับหน้าแรก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
    canvas.tag_bind(text, '<Button-1>', lambda event: back())
    canvas.place(relx=0.66, rely=0.94, anchor=tk.CENTER)

    root.mainloop()
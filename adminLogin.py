import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
from sentiment_methods import create_rounded_rectangle

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "aa":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        root.destroy()
        subprocess.run(["python", "adminCreateModel.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def back():
    root.destroy()
    subprocess.run(["python", "userChooseFile.py"])

root = tk.Tk()
root.title("Login Admin")
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.config(bg="#faf9f5")
style = ttk.Style()
root.resizable(False, False)

login_frame = tk.Frame(root, width=700, height=580, bg="#faf9f5")
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

label1 = tk.Label(login_frame, text="เข้าสู่ระบบสำหรับผู้ดูแลระบบ", bg="#faf9f5",font=("TH SarabunPSK", 20))
label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
username_label = tk.Label(login_frame, text="ชื่อผู้ใช้:", font=("TH SarabunPSK", 20), bg="#faf9f5")
username_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

username_entry = tk.Entry(login_frame, width=30)
username_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

password_label = tk.Label(login_frame, text="รหัสผ่าน:", font=("TH SarabunPSK", 20), bg="#faf9f5")
password_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg = "#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#44ae9b')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: validate_login())
text = canvas.create_text(60, 20, text="เข้าสู่ระบบ", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: validate_login())
canvas.place(relx=0.4, rely=0.655, anchor=tk.CENTER)

canvas = tk.Canvas(root, width=120, height=40, highlightthickness=0, bg = "#faf9f5")
canvas.pack()
rounded_rect = create_rounded_rectangle(canvas, 5, 5, 115, 35, radius=10, fill='#ae4444')
canvas.tag_bind(rounded_rect, '<Button-1>', lambda event: back())
text = canvas.create_text(60, 20, text="กลับหน้าแรก", fill='white', font=('TH SarabunPSK', 18, 'bold'))
canvas.tag_bind(text, '<Button-1>', lambda event: back())
canvas.place(relx=0.6, rely=0.65, anchor=tk.CENTER)

root.mainloop()

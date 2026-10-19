import tkinter as tk
import tkinter.messagebox as msg
top=tk.Tk()
CheckVar1=tk.StringVar()
C=tk.Checkbutton(top,text="Gender, check kalau laki2",
                variable=CheckVar1,
                onvalue="Mr. ",offvalue="Ms. ",height=5)
C.pack()
L1=tk.Label(top,text="Nama: ")
L1.pack()
E1=tk.Entry(top,bd=5)
E1.pack()
def helloCallback():
    msg.showinfo("Belajar GUI","Assalamu'alaikum! "
                +CheckVar1.get()+E1.get())
w1=tk.Button(top,text="Klik Saya!", command=helloCallback)
w1.pack()
top.mainloop()
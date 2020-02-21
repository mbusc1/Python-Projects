from tkinter import *

root = Tk()
root.title('Widget Tester')
main = Frame(root)
main.pack(side=TOP,anchor=W)

o_var = StringVar()
o_var.set('Choose Option')
om = OptionMenu(main, o_var, 'option1','option2','option3')
om.grid(row=1,column=1)
om.config(width = 10)

e = Entry(main) 
e.grid(row=2,column=2)

def option_to_entry(option,entry):
    entry.delete(0,END)
    entry.insert(0,option.get())    
b= Button(main,text='Show Chosen Option',command=lambda : option_to_entry(o_var,e))
b.grid(row=1,column=2)

root.mainloop()
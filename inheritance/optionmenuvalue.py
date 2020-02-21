from tkinter import *

#OptionMenuToEntry: with title,linked_entry, and option_tuple
#get is a pull function to get the option selected
class OptionMenuValue(OptionMenu):
    def __init__(self,parent,title,*option_tuple,**configs):
        self.result = StringVar()
        self.result.set(title)
        self.original_title = title
        OptionMenu.__init__(self,parent,self.result,*option_tuple,**configs)

    def reset(self):
        self.result.set(self.original_title)
        
    def get(self):
        value = self.result.get()
        return value if value != self.original_title else 'None'


root = Tk()
root.title('Widget Tester')
main = Frame(root)
main.pack(side=TOP,anchor=W)

om = OptionMenuValue(main, 'Choose Option', 'option1','option2','option3')
om.grid(row=1,column=1)
om.config(width = 10)

e = Entry(main) 
e.grid(row=2,column=2)

def option_to_entry(option,entry):
    entry.delete(0,END)
    entry.insert(0,option.get())    
b= Button(main,text='Show Chosen Option',command=lambda : option_to_entry(om,e))
b.grid(row=1,column=2)

b = Button(main,text='Reset Option',command=om.reset)
b.grid(row=1,column=3)

root.mainloop()

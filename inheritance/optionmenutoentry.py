from tkinter import *

# OptionMenuValue: with title and option_tuple
# get is a pull function to get the option selected
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


#OptionMenuToEntry: with title, linked_entry, and option_tuple
#get is an inherited pull function; put is a push function, pushing
#  the selected option into the linked_entry (replacing what is there)

class OptionMenuToEntry(OptionMenuValue):
    def __init__(self,parent,title,linked_entry,*option_tuple,**configs):
        self.entry = linked_entry
        OptionMenuValue.__init__(self,parent,title,*option_tuple,command=self.put,**configs)
  
    def reset(self):
        OptionMenuValue.reset(self)
        self.put('','white')
        
    def put(self,option,bg='green'):
        self.entry.delete(0,len(self.entry.get()))
        self.entry.insert(0,option)
        self.entry.config(bg=bg)


root = Tk()
root.title('Widget Tester')
main = Frame(root)
main.pack(side=TOP,anchor=W)

e = Entry(main) 
e.grid(row=2,column=2)

omte = OptionMenuToEntry(main, 'Choose Option', e, 'option1','option2','option3')
omte.grid(row=1,column=1)
omte.config(width = 10)

b= Button(main,text='Show Chosen Option',command=lambda : omte.put(omte.get(),'white'))
b.grid(row=1,column=2)

b = Button(main,text='Reset Option',command=omte.reset)
b.grid(row=1,column=3)

root.mainloop()
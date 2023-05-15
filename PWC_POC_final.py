# Turning PDfs into Text
import PyPDF2
import os
folder_path =" Mian"
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        pdf_file = open(folder_path + filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for i in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[i].extract_text().strip()
        name = filename.replace('.pdf','')
        txt_path = 'lawfiles\\textfiles\\{name}.txt'
    with open(txt_path,'w',encoding = 'utf8') as taxfile:
        taxfile.write(text)


from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
loader = DirectoryLoader('lawfiles\\textfiles\\', glob="**/*.txt",show_progress=True)
from langchain.indexes import VectorstoreIndexCreator


index = VectorstoreIndexCreator().from_loaders([loader])



from tkinter import *

BG_GRAY = "#FFA07A"
BG_COLOR = "#A9DFBF"
TEXT_COLOR = "#000000"

FONT = ("Helvetica 14",10)
FONT_BOLD = ("Helvetica 13 bold",10)

class chatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()
    
    def _setup_main_window(self):
        self.window.title("Tax Laws Chat Box")  
        self.window.resizable(width = False,height = False)
        self.window.configure(width = 470,height = 550,bg = '#999932')

        head_label = Label(self.window, 
                           bg = '#3A5A40', 
                           fg = '#FFFFFF',
                           text = "Welcome",
                           font = FONT_BOLD,
                           pady = 10)
        
        head_label.place(relwidth = 1)

        #tiny divider

        line = Label(self.window,width = 450, bg = '#FFFFFF')
        line.place(relwidth=1, rely = 0.07, relheight = 0.012)

        #text widget
        self.text_widget = Text(self.window,width = 20,height = 2, bg = BG_COLOR,wrap = WORD, fg= TEXT_COLOR,font=FONT,padx = 5, pady = 5)
        self.text_widget.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.text_widget.configure(cursor = 'arrow',state = DISABLED)

        #Scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight = 1,relx = 0.974)
        scrollbar.configure(command =  self.text_widget.yview)

        #bottom_label 
        bottom_label = Label(self.window, bg= '#344E41',height = 80)
        bottom_label.place(relwidth = 1, rely = 0.825)
        

        #message entry box
        self.msg_entry = Entry(bottom_label,bg = '#DAD7CD',fg = TEXT_COLOR, font = FONT)
        self.msg_entry.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        #Send Button
        send_button = Button(bottom_label,text = 'Send',font = FONT, width = 20,fg = '#FFFFFF',bg = '#999932',
                             command = lambda: self._on_enter_pressed(None))
        send_button.place(relx = 0.77, rely = 0.008, relheight = 0.06,relwidth = 0.22,)

    def _on_enter_pressed(self,event):
        msg = self.msg_entry.get()
        self._insert_message(msg,"YOU")

    def _insert_message(self,msg,sender):
        if not msg:
            return
            
        self.msg_entry.delete(0,END)
        bot_message = index.query(msg)
        msg1 = f"{sender}:{msg}\n\n"
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state = DISABLED)
        
      
        msg2 = f"Dynapt_AI:{bot_message}\n\n"
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state = DISABLED)

        self.text_widget.see(END) #scroll to the end so we can see the last message

if __name__ == "__main__":
    app = chatApplication()
    app.run()

from tkinter import *
from sercli import *

class App:
    def __init__(self, master=None):
        self.cCons = Frame(master, bg="#505050")
        self.cCons.pack(side=LEFT, fill=BOTH)

        self.cMens = Frame(master, bg="#606060", padx=10)
        self.cMens.pack(side=LEFT, fill=BOTH, expand=1)

        self.cMenRecv = Frame(self.cMens, bg="#606060", pady=10)
        self.cMenRecv.pack(fill=BOTH, expand=1)
        
        self.cMenstyle = Frame(self.cMenRecv, bg="#707070", padx=4)
        self.cMenstyle.pack(fill=BOTH, expand=1)
        
        self.cRecv = Frame(self.cMenstyle, bg="#606060")
        self.cRecv.pack(fill=BOTH, expand=1)

        self.cEnv = Frame(self.cMens, bg="#606060", padx=10, pady=10)
        self.cEnv.pack(fill=BOTH)
        
        self.listaconexao = Listbox(self.cCons, bg="#505050", activestyle="none", justify=CENTER,font=("Verdana", "20"), fg="white", borderwidth=0, selectbackground="#606060", highlightthickness=0)
        self.listaconexao.bind("<<ListboxSelect>>", self.printMsg)
        self.listaconexao.insert(END, "Yin")
        self.listaconexao.insert(END, "BETA")
        self.listaconexao.pack(fill=BOTH,expand=1)
        
        self.smen = Scrollbar(self.cRecv)
        self.caixademensagens = Text(self.cRecv, state="disabled", cursor="arrow", font=("Verdana", "15"), bg="#606060", fg="#FFFFFF", relief="flat")
        self.smen.pack(side=RIGHT, fill=Y)
        self.caixademensagens.pack(fill=BOTH, expand=1)
        self.smen.config(command=self.caixademensagens.yview)
        self.caixademensagens.config(yscrollcommand=self.smen.set)

        self.caixadeenvio = Text(self.cEnv, height=1, insertbackground="#FFFFFF", bg="#707070", relief="flat", font=("Verdana", "15"), fg="white")
        self.caixadeenvio.bind("<Return>", self.printMsg)
        self.caixadeenvio.bind("<Shift-Return>", self.aumentar)
        self.caixadeenvio.pack(fill=BOTH)
        
        pass

    def printMsg(self,event):
        msg = self.caixadeenvio.get(0.0,INSERT)
        self.caixadeenvio.delete(0.0,END)
        self.caixadeenvio.configure(height=1)
        self.caixademensagens.configure(state="normal")
        self.caixademensagens.insert(END, msg)
        self.caixademensagens.configure(state="disabled")
        self.caixademensagens.see("end")

    def aumentar(self,event):
        self.caixadeenvio.configure(height=2)

root = Tk()
App(root)
root.mainloop()

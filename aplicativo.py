from tkinter import *
from PIL import Image, ImageTk
import requests, json, io, socket, threading

class Login:
    def __init__(self):
        self.root = Tk()
        self.root.title("Chat - Login")
        #self.root.iconbitmap("icon.ico")
        self.root.resizable(0, 0)
        self.root.configure(bg="#505050", pady=20, padx=20)

        self.clLogin = Frame(self.root, bg="#505050")
        self.clLogin.pack()

        self.login = ImageTk.PhotoImage(Image.open("Login.png"))
        self.lLogin = Label(self.clLogin, font=("Verdana", "30"), bg="#505050", fg="#FFFFFF", image=self.login, height=100)
        self.lLogin.pack()

        self.autenticado = Frame(self.root, bg="#505050")
        self.autenticado.pack()

        self.lautenticar = Label(self.autenticado, bg="#505050", fg="#FFFFFF")
        self.lautenticar.pack()

        self.ccredenciais = Frame(self.root, bg="#505050")
        self.ccredenciais.pack()

        self.cllcredenciais = Frame(self.ccredenciais, bg="#505050")
        self.cllcredenciais.pack(side=LEFT)

        self.lmatricula = Label(self.cllcredenciais, font=("Verdana", "18"), bg="#505050", fg="#FFFFFF")
        self.lmatricula["text"] = "Matrícula:"
        self.lmatricula.pack()

        self.lSenha = Label(self.cllcredenciais, font=("Verdana", "18"), bg="#505050", fg="#FFFFFF")
        self.lSenha["text"] = "Senha:"
        self.lSenha.pack()

        self.ceecredenciais = Frame(self.ccredenciais, bg="#505050", pady=5)
        self.ceecredenciais.pack()

        self.matricula = Entry(self.ceecredenciais, width=20, bg="#707070", borderwidth=0, font=("Verdana", "15"), insertbackground="#FFFFFF", fg="white")
        self.matricula.bind("<Return>", self.autenticacao)
        self.matricula.pack()

        self.senha = Entry(self.ceecredenciais, width=20, bg="#707070", borderwidth=0, show="●", font=("Verdana", "15"), insertbackground="#FFFFFF", fg="white")
        self.senha.bind("<Return>", self.autenticacao)
        self.senha.pack(pady=(8,0))

        self.cAutenticar = Frame(self.root, bg="#505050")
        self.cAutenticar.pack(pady=(15,0))

        self.autenticar = Button(self.cAutenticar, width=15, bg="#707070", borderwidth=0, font=("Verdana", "18"), fg="white")
        self.autenticar["text"] = "Autenticar"
        self.autenticar.bind("<Button-1>", self.autenticacao)
        self.autenticar.pack()

        self.root.mainloop()

    def token(self):
        matricula = self.matricula.get()
        senha = self.senha.get()
        url_token = "https://suap.ifrn.edu.br/api/v2/autenticacao/token/"
        credenciais = {
            "username":matricula,
            "password":senha
        }
        response = requests.post(url_token, data=credenciais)
        if response.status_code == 200:
            tokenDir = json.loads(response.content.decode("utf-8"))
            return tokenDir["token"]
        else:
            return None

    def autenticacao(self, event):
        if self.token() == None:
            self.matricula.delete(0,END)
            self.senha.delete(0,END)
            self.lautenticar["text"] = "Usuário e/ou senha inválidos!"
            
        else:
            self.recuperaDados()

    def recuperaDados(self):
        cabecalho = {"Authorization":"JWT {}".format(self.token())}
        url_dados = "https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"
        self.dadosDir = requests.get(url_dados, headers=cabecalho)
        self.dadosDir = json.loads(self.dadosDir.content.decode("utf-8"))
        self.imagem = requests.get("https://suap.ifrn.edu.br" + self.dadosDir["url_foto_75x100"])
        self.imagem = self.imagem.content
        self.imagem = io.BytesIO(self.imagem)
        self.imagemopen = Image.open(self.imagem)
        self.foto = ImageTk.PhotoImage(self.imagemopen)
        self.reformular()

    def reformular(self):
        self.clLogin.destroy()
        self.lLogin.destroy()
        self.autenticado.destroy()
        self.lautenticar.destroy()
        self.ccredenciais.destroy()
        self.cllcredenciais.destroy()
        self.lmatricula.destroy()
        self.lSenha.destroy()
        self.ceecredenciais.destroy()
        self.matricula.destroy()
        self.senha.destroy()
        self.cAutenticar.destroy()
        self.autenticar.destroy()
        
        self.root.title("Chat - Cliente")
        self.root.configure(bg="#404040", padx=20)

        self.cliente()

        self.D = {}

        self.cCons = Frame(self.root, bg="#606060")
        self.cCons.pack(side=LEFT, fill=BOTH)

        self.cMens = Frame(self.root, bg="#606060", padx=10)

        self.cMenRecv = Frame(self.cMens, bg="#606060", pady=10)
        self.cMenRecv.pack(fill=BOTH, expand=1)
        
        self.cMenstyle = Frame(self.cMenRecv, bg="#707070", padx=4)
        self.cMenstyle.pack(fill=BOTH, expand=1)
        
        self.cRecv = Frame(self.cMenstyle, bg="#606060")
        self.cRecv.pack(fill=BOTH, expand=1)

        self.cEnv = Frame(self.cMens, bg="#606060", padx=10, pady=10)
        self.cEnv.pack(fill=BOTH)

        self.cIdentificacao = Frame(self.cCons, bg="#606060", padx=5, pady=5)
        self.cIdentificacao.pack(fill=X)

        self.cIFoto = Frame(self.cIdentificacao, bg="#505050", padx=3, pady=3)
        self.cIFoto.pack(side=LEFT)

        self.iIdentificacao = Label(self.cIFoto, image=self.foto, borderwidth=0)
        self.iIdentificacao.pack()

        self.ccIdentificacao = Frame(self.cIdentificacao)
        self.ccIdentificacao.pack(side=LEFT, fill=X)
        
        self.l1Identificacao = Label(self.ccIdentificacao, text="Nome:", bg="#606060", fg="#FFFFFF", font=("Verdana", "8", "bold"), anchor=W)
        self.l1Identificacao.pack(fill=X)

        self.l2Identificacao = Label(self.ccIdentificacao, text="Matrícula:", bg="#606060", fg="#FFFFFF", font=("Verdana", "8", "bold"), anchor=W)
        self.l2Identificacao.pack(fill=X)

        self.l3Identificacao = Label(self.ccIdentificacao, text="Email:", bg="#606060", fg="#FFFFFF", font=("Verdana", "8", "bold"), anchor=W)
        self.l3Identificacao.pack(fill=X)

        self.l4Identificacao = Label(self.ccIdentificacao, text="Curso:", bg="#606060", fg="#FFFFFF", font=("Verdana", "8", "bold"), anchor=W)
        self.l4Identificacao.pack(fill=X)

        self.l5Identificacao = Label(self.ccIdentificacao, text="Vínculo:", bg="#606060", fg="#FFFFFF", font=("Verdana", "8", "bold"), anchor=W)
        self.l5Identificacao.pack(fill=X)

        self.cccIdentificacao = Frame(self.cIdentificacao, pady=5, bg="#606060")
        self.cccIdentificacao.pack(fill=X)

        self.ll1Identificacao = Label(self.cccIdentificacao, text=self.dadosDir["vinculo"]["nome"], bg="#606060", fg="#FFFFFF", font=("Verdana", "8"), anchor=W)
        self.ll1Identificacao.pack(fill=X)

        self.ll2Identificacao = Label(self.cccIdentificacao, text=self.dadosDir["vinculo"]["matricula"], bg="#606060", fg="#FFFFFF", font=("Verdana", "8"), anchor=W)
        self.ll2Identificacao.pack(fill=X)

        self.ll3Identificacao = Label(self.cccIdentificacao, text=self.dadosDir["email"], bg="#606060", fg="#FFFFFF", font=("Verdana", "8"), anchor=W)
        self.ll3Identificacao.pack(fill=X)

        self.ll4Identificacao = Label(self.cccIdentificacao, text=self.dadosDir["vinculo"]["curso"], bg="#606060", fg="#FFFFFF", font=("Verdana", "8"), anchor=W)
        self.ll4Identificacao.pack(fill=X)

        self.ll5Identificacao = Label(self.cccIdentificacao, text=self.dadosDir["tipo_vinculo"], bg="#606060", fg="#FFFFFF", font=("Verdana", "8"), anchor=W)
        self.ll5Identificacao.pack(fill=X)

        self.cIStyle = Frame(self.cCons, bg="#707070", height=4, width=350)
        self.cIStyle.pack()
        
        self.listaconexao = Listbox(self.cCons, bg="#505050", activestyle="none", justify=CENTER,font=("Verdana", "20"), fg="white", borderwidth=0, selectbackground="#606060", highlightthickness=0, state="disabled")
        self.listaconexao.pack(fill=BOTH,expand=1)

        self.add = Button(self.cCons, text="Adicionar Amigo", borderwidth=0, bg="#707070", fg="#FFFFFF", font=("Verdana", "18"))
        self.add.bind("<Button-1>", self.adicionarAmigo)
        self.add.pack(fill=X)
        
        self.smen = Scrollbar(self.cRecv)
        self.caixademensagens = Text(self.cRecv, state="disabled", cursor="arrow", font=("Verdana", "15"), bg="#606060", fg="#FFFFFF", relief="flat")
        self.smen.pack(side=RIGHT, fill=Y)
        self.caixademensagens.pack(fill=BOTH, expand=1)
        self.smen.config(command=self.caixademensagens.yview)
        self.caixademensagens.config(yscrollcommand=self.smen.set)

        self.caixadeenvio = Text(self.cEnv, height=1, insertbackground="#FFFFFF", bg="#707070", relief="flat", font=("Verdana", "15"), fg="white")
        self.caixadeenvio.bind("<Return>", self.enviandoMensagem)
        self.caixadeenvio.bind("<Shift-Return>", self.aumentar)
        self.caixadeenvio.pack(fill=BOTH)

    def enviandoMensagem(self, event):
            msg = {"flag":"MSG", "content":None}
            content = self.caixadeenvio.get(0.0,INSERT)
            msg["content"] = {"matricula":self.dadosDir["vinculo"]["matricula"], "msg":content, "grupo":None}
            nome = self.listaconexao.get(self.listaconexao.curselection()[0])
            for matricula in self.D.keys():
                if self.D[matricula]["nome"] == nome:
                    msg["content"]["grupo"] = self.D[matricula]["grupo"]
            msg = json.dumps(msg)
            msg = msg.encode("utf-8")
            self.s.send(msg)
            self.caixadeenvio.delete(0.0,END)
            self.caixadeenvio.configure(height=1)

    def recebendo(self):
        while True:
            msg = self.s.recv(512)
            msg = msg.decode("utf-8")
            msg = json.loads(msg)
            if msg["rflag"] == "MSG":
                self.printMSG(msg["rcontent"])
            elif msg["rflag"] == "CST":
                self.respAmigo(msg["rcontent"])
            elif msg["rflag"] == "SLA1":
                self.recebeGrupo(msg["rcontent"])
            elif msg["rflag"] == "SLA2":
                self.recebeMensagens(msg["rcontent"])

    def printMSG(self, msg):
        msg["mensagem"] = msg["mensagem"].replace("\n", "\n\t")
        self.caixademensagens.configure(state="normal")
        if msg["nome"] == self.dadosDir["vinculo"]["nome"]:
            if msg["mensagem"][0] == "\n":
                self.caixademensagens.insert(END, "\nVocê:\n" + str(msg["mensagem"][1:]))
            else:
                msg["mensagem"] = "\t" + msg["mensagem"]
                self.caixademensagens.insert(END, "\nVocê:\n" + str(msg["mensagem"]))
        else:
            if msg["mensagem"][0] == "\n":
                self.caixademensagens.insert(END, "\n{}:\n".format(msg["nome"]) + str(msg["mensagem"][1:]))
            else:
                msg["mensagem"] = "\t" + msg["mensagem"]
                self.caixademensagens.insert(END, "\n{}:\n".format(msg["nome"]) + str(msg["mensagem"]))
        self.caixademensagens.configure(state="disabled")
        self.caixademensagens.see("end")

    def respAmigo(self, resp):
        if resp["nome"] == "" and resp["matricula"] == "":
            self.lladd.configure(text="Usuário Não Encontrado!")
        else:
            self.D[resp["matricula"]] = {"nome":resp["nome"], "grupo": None}
            self.listaconexao.configure(state="normal")
            self.listaconexao.bind("<<ListboxSelect>>", self.selecionarAmigo)
            self.listaconexao.insert(END, resp["nome"])
            self.add.destroy()

    def recebeGrupo(self, resp):
        self.D[resp["matricula_destino"]]["grupo"]= resp["grupo"]

    def recebeMensagens(self, resp):
        self.caixademensagens.configure(state="normal")
        self.caixademensagens.delete(0.0,END)
        for mensagem in resp:
            mensagem[1] = mensagem[1].replace("\n", "\n\t")
            if mensagem[0] == self.dadosDir["vinculo"]["nome"]:
                if mensagem[1][0] == "\n":
                    self.caixademensagens.insert(END, "\nVocê:\n" + str(mensagem[1][1:]))
                else:
                    mensagem[1] = "\t" + mensagem[1]
                    self.caixademensagens.insert(END, "\nVocê:\n" + str(mensagem[1]))
            else:
                if mensagem[1][0] == "\n":
                    self.caixademensagens.insert(END, "\n{}:\n".format(mensagem[0]) + str(mensagem[1][1:]))
                else:
                    mensagem[1] = "\t" + mensagem[1]
                    self.caixademensagens.insert(END, "\n{}:\n".format(mensagem[0]) + str(mensagem[1]))
            self.caixademensagens.configure(state="disabled")
            self.caixademensagens.see("end")
    
    def cliente(self):
        reg = {"flag":"REG", "content":None}
        content = {"nome":self.dadosDir["vinculo"]["nome"], "matricula":self.dadosDir["vinculo"]["matricula"]}
        reg["content"] = content
        reg = json.dumps(reg)
        reg = reg.encode("utf-8")
        
        host = "localhost"
        port = 5000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.s.send(reg)
        threading.Thread(target=self.recebendo).start()

    def aumentar(self,event):
        self.caixadeenvio.configure(height=2)

    def adicionarAmigo(self, event):
        self.add = Toplevel()
        #self.add.iconbitmap("icon.ico")
        self.add.title("Chat - Adicionar Amigo")
        self.add.configure(bg="#505050", padx = 20, pady=20)
        self.add.resizable(0, 0)

        cladd = Frame(self.add, bg="#505050")
        cladd.pack()

        ladd = Label(cladd, font=("Verdana", "18"), text="Adicionar Amigo", bg="#505050", fg="#FFFFFF")
        ladd.pack()

        self.lladd = Label(cladd, font=("Verdana"), text="", bg="#505050", fg="#FFFFFF")
        self.lladd.pack()

        cadd = Frame(self.add, bg="#505050")
        cadd.pack()

        cladd = Frame(cadd, bg="#505050")
        cladd.pack(side=LEFT)

        lmatriculaadd = Label(cladd, font=("Verdana", "15"), text="Matrícula:", bg="#505050", fg="#FFFFFF")
        lmatriculaadd.pack(pady=(6,0))

        ceadd = Frame(cadd, bg="#505050")
        ceadd.pack()

        self.ematriculaadd = Entry(ceadd, width=20, bg="#707070", borderwidth=0, font=("Verdana", "15"), insertbackground="#FFFFFF", fg="white")
        self.ematriculaadd.pack(pady=(10,0))

        cbadd = Frame(self.add, bg="#505050")
        cbadd.pack()

        badd = Button(cbadd, bg="#707070", fg="#FFFFFF", font=("Verdana", "18"), text="Adicionar", borderwidth=0)
        badd.bind("<Button-1>", self.consultarAmigo)
        badd.pack(pady=(20,0))

    def consultarAmigo(self, event):
        if self.ematriculaadd.get() != self.dadosDir["vinculo"]["matricula"]:
            cst = {"flag":"CST", "content":self.ematriculaadd.get()}
            cst = json.dumps(cst)
            cst = cst.encode("utf-8")
            self.s.send(cst)
        else:
            self.lladd.configure(text="Você Não Pode Se Adicionar!")

    def selecionarAmigo(self, event):
        self.cMens.pack(side=LEFT, fill=BOTH, expand=1)
        nome = event.widget.get(event.widget.curselection()[0])
        for matricula in self.D.keys():
            if self.D[matricula]["nome"] == nome:
                if self.D[matricula]["grupo"] == None:
                    sla = {"flag":"SLA1", "content":{"matricula_origem":self.dadosDir["vinculo"]["matricula"], "matricula_destino":matricula}}
                    sla = json.dumps(sla)
                    sla = sla.encode("utf-8")
                    self.s.send(sla)
                else:
                    sla = {"flag":"SLA2", "content":{"matricula_origem":self.dadosDir["vinculo"]["matricula"], "grupo":self.D[matricula]["grupo"]}}
                    sla = json.dumps(sla)
                    sla = sla.encode("utf-8")
                    self.s.send(sla)
                break
        
Login()

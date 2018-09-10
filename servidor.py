from socket import *
import threading, json

#D = {"matricula1":{nome:"nome", conexao:con, grupos:{GRUPO1:{conexao:[con, con1], mensagens:[msg1,msg2,msg3]}}}}
D = {}
C = {}
cg = 0

def flagMSG(msg, con):
    if msg["msg"][0] == "\n":
        print("Mensagem Recebida ({}):\n".format(D[msg["matricula"]]["nome"]) + msg["msg"].replace("\n", "\n\t")[1:])
    else:
        print("Mensagem Recebida ({}):\n".format(D[msg["matricula"]]["nome"]) + "\t" + msg["msg"].replace("\n", "\n\t"))
    D[msg["matricula"]]["grupos"][msg["grupo"]]["mensagens"].append((D[msg["matricula"]]["nome"], "\t" + msg["msg"].replace("\n", "\n\t")))
    resp = {"rflag":"MSG", "rcontent":{"nome": D[msg["matricula"]]["nome"],"mensagem":msg["msg"]}}
    resp = json.dumps(resp)
    resp = resp.encode("utf-8")
    for con in D[msg["matricula"]]["grupos"][msg["grupo"]]["conexao"]:
        con.send(resp)

def flagREG(reg, con):
    if reg["matricula"] in D.keys():
        for matricula in D.keys():
            for grupo in D[matricula]["grupos"].keys():
                for c in range(len(D[matricula]["grupos"][grupo]["conexao"])):
                    if D[matricula]["grupos"][grupo]["conexao"][c] == C[reg["matricula"]]:
                        D[matricula]["grupos"][grupo]["conexao"][c] = con
        C[reg["matricula"]] = con
        print("{} se conectou!".format(D[reg["matricula"]]["nome"]))
    else:
        D[reg["matricula"]] = {"nome":reg['nome'], "conexao": con, "grupos": {}}
        C[reg["matricula"]] = con
        print(reg['nome'],"foi registrado!")
        print("{} se conectou!".format(D[reg["matricula"]]["nome"]))

def flagCST(cst, con):
    resp = {"rflag":"CST", "rcontent":None}
    if cst in D.keys():
        resp["rcontent"] = {"nome":D[cst]["nome"], "matricula":cst}
        resp = json.dumps(resp)
        resp = resp.encode("utf-8")
        con.send(resp)
    else:
        resp["rcontent"] = {"nome":"", "matricula":""}
        resp = json.dumps(resp)
        resp = resp.encode("utf-8")
        con.send(resp)

def flagSLA1(sla1, con, cg):
    resp = {"rflag":"SLA1", "rcontent":None}
    cg += 1
    resp["rcontent"] = {"grupo":"GRUPO"+str(cg),"matricula_destino": sla1["matricula_destino"]}
    D[sla1["matricula_origem"]]["grupos"][resp["rcontent"]["grupo"]] = {"conexao":[con, D[sla1["matricula_destino"]]["conexao"]], "mensagens":[]}
    resp = json.dumps(resp)
    resp = resp.encode("utf-8")
    con.send(resp)

#problema
def flagSLA2(sla2, con):
    resp = {"rflag":"SLA2", "rcontent":[]}
    for mensagem in D[sla2["matricula_origem"]]["grupos"][sla2["grupo"]]["mensagens"]:
        resp["rcontent"].append(mensagem)
    resp = json.dumps(resp)
    resp = resp.encode("utf-8")
    con.send(resp)

def conexao(con):
    with con:
        while True:
            msg = con.recv(1024)
            msg = msg.decode("utf-8")
            msg = json.loads(msg)
            if msg["flag"] == "MSG":
                flagMSG(msg["content"], con)
            elif msg["flag"] == "REG":
                flagREG(msg["content"], con)
            elif msg["flag"] == "CST":
                flagCST(msg["content"], con)
            elif msg["flag"] == "SLA1":
                flagSLA1(msg["content"], con, cg)
            elif msg["flag"] == "SLA2":
                flagSLA2(msg["content"], con)
                    
def ativar():
    host = ""
    port = 5000

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen(5)
        print("Servidor Ligado!")
        while True:
            con, cli = s.accept()
            threading.Thread(target=conexao, args=(con,)).start()

ativar()

from tkinter import *
from tkinter import ttk

##Definindo função responsável por ordenar nossa lista
def ordem(vetor):
    tamanho = len(vetor)
    for i in range(tamanho):
        troca = False
        for j in range(1, tamanho - i):
            if vetor[j] < vetor[j - 1]:
                Temp = vetor[j]
                vetor[j] = vetor[j - 1]
                vetor[j - 1] = Temp
                troca = True
        if not troca:
            break
    return vetor
##Fim da função responsável por ordenar nossa lista

##Definindo função que lê o .txt insere ele em uma lista, chamamos o metódo de ordenção e após ordenado a lista é retornada em um treeview
def carregar_pedidos():
    janela10=Toplevel()##Criando janela
    janela10.title('Pedidos')##Configurações da janela
    janela10.configure(background='light blue')
    janela10.geometry('600x200')
    janela10.resizable(False, False)
    frame0=LabelFrame(janela10,text='Pedidos feitos')
    frame0.pack(pady=10,padx=10)
    tv_pedidos=ttk.Treeview(frame0,columns=('nome','quantidade','valorpago','datapedido'),show='headings')
    tv_pedidos.column('nome',minwidth=0,width=200)
    tv_pedidos.column('quantidade',minwidth=0,width=150)
    tv_pedidos.column('valorpago',minwidth=0,width=100)
    tv_pedidos.column('datapedido',minwidth=0,width=100)
    tv_pedidos.heading('nome',text='Nome')
    tv_pedidos.heading('quantidade',text='Quantidade solicitada')
    tv_pedidos.heading('valorpago',text='Valor pago')
    tv_pedidos.heading('datapedido',text='Data do pedido')##Fim das configurações
    arquivo=open("pedidos.txt","r")##Abrindo conexão e lendo nosso .txt
    pedidos = []##Criando lista que irá receber o .txt
    for linha in arquivo.readlines():
        pedidos = pedidos + [linha] ##Atribuindo cada linha do txt em uma posição da lista
    arquivo.close()##Fechando conexão com nosso txt
    ordem(pedidos)##Chamando o método de ordenação que recebe como parâmetro nossa lista
    for (a) in pedidos:     ##Após ordenado, inserindo valores no treeview
            tv_pedidos.insert('','end',values=(a))
    tv_pedidos.pack()
##Fim da função lê o .txt insere ele em uma lista, chamamos o metódo de ordenção e após ordenado a lista é retornada em um treeview

##Definindo função que lê o .txt insere ele em uma lista, chamamos o metódo de ordenção e após ordenado a lista é retornada em um treeview
def carregar_fornecedores():
    janela99=Toplevel()##Criando janela
    janela99.title('Fornecedores')##Configurações da janela
    janela99.configure(background='light blue')
    janela99.geometry('600x200')
    janela99.resizable(False, False)
    frame17=LabelFrame(janela99,text='Dados fornecedores')
    frame17.pack(pady=10,padx=10)
    tv_fornecedor=ttk.Treeview(frame17,columns=('nome','fone'),show='headings')
    tv_fornecedor.column('nome',minwidth=0,width=500)
    tv_fornecedor.column('fone',minwidth=0,width=300)
    tv_fornecedor.heading('nome',text='Nome')
    tv_fornecedor.heading('fone',text='Contato')##Fim das configurações
    arquivo=open("fornecedores.txt","r")##Abrindo conexão e lendo nosso .txt
    fornecedores = []##Criando lista que irá receber o .txt
    for linha in arquivo.readlines():
        fornecedores = fornecedores + [linha]##Atribuindo cada linha do txt em uma posição da lista
    arquivo.close()##Fechando conexão com nosso txt
    ordem(fornecedores)##Chamando o método de ordenação que recebe como parâmetro nossa lista
    for (a) in fornecedores:     ##Após ordenado, inserindo valores no treeview
            tv_fornecedor.insert('','end',values=(a))
    tv_fornecedor.pack()
##Fim da função que lê o .txt insere ele em uma lista, chamamos o metódo de ordenção e após ordenado a lista é retornada em um treeview

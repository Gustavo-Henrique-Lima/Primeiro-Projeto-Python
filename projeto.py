from tkinter import *
from tkinter import messagebox
from cont_projeto import *
from tkinter import ttk
import sqlite3
from sqlite3 import Error 
##Criando classe BANCO que será responsável pela manipulação do banco de dados
class banco():
    ##Conexão com o banco de dados
    def conectar():
        caminho='C:\\Users\\gusta\\OneDrive\\Documentos\\Projeto\\loja_projeto.db3' ##Ensinando caminho para o banco de dados
        con=None##Declarando variável para receber o caminho
        try:
            con=sqlite3.connect(caminho)##Atribuindo o caminho na variável
        except Error as erro:
            print(erro)
        return con
    ##Fim da conexão com o banco de dados

    ##Função para preencher nosso TreeView com o que está gravando no banco de dados
    def dql(query):                 
        conexao=banco.conectar()    ##Abrindo conexão com a base de dados
        a=conexao.cursor()          ##Criando ponteiro
        a.execute(query)            ##Linha responsável por executar a ação dentro do bd
        res=a.fetchall()            ##Fechando o ponteiro
        conexao.close()             ##Fechando conexão com a base de dados
        return res
    ##Fim da função para preencher nosso TreeView
    
    ##Definindo a função que serve de base para as funções de manipulação do BD
    def dml(query):              
        conexao=banco.conectar()    ##Abrindo conexão com a base de dados
        b=conexao.cursor()          ##Criando ponteiro
        b.execute(query)            ##Linha responsável por executar a ação dentro do bd
        conexao.commit()            ##Salvando a ação dentro do BD
        conexao.close()             ##Fechando conexão com a base de dados
    ##Fim da função que serve de base para as funções de manipulação do BD
#############Fim da classe BANCO



#############Criando classe funções que será responsável pelo ações que os botões devem fazer
class funcs(banco):
       ##Função que verifica se o login do usuário gerente corresponde com o que está no BD
    def verificar_login_gerente(self):
        senha = self.senha.get()                ##Capturando senha do usuário gerente
        try:
            query="SELECT senha FROM login_gerente WHERE id LIKE'%"+self.usuario.get()+"%'"
            senha_b=banco.dql(query)
            if senha == senha_b[0][0]:
                self.tela_gerente()
            else:
                messagebox.showinfo(title='Erro',message='Usuário e/ou senha inválidos')
        except:
            messagebox.showinfo(title='Erro',message='Usuário não cadastrado')
    
    ##Fim da função que verifica se o login do usuário gerente corresponde com o que está no DB
    
    ##Função que verifica se o login do usuário operador corresponde com o que está no DB
    def verificar_login_operador(self):
        senha_operador = self.pega_senha.get()      ##Capturando senha do usuário operador
        try:
            query="SELECT senha FROM login_operador WHERE id LIKE'%"+self.pega_usuario.get()+"%'"
            senha_bd=banco.dql(query)
            if senha_operador == senha_bd[0][0]:
                self.tela_operador()
            else:
                messagebox.showinfo(title='Erro',message='Usuário e/ou senha inválidos')
        except:
            messagebox.showinfo(title='Erro',message='Usuário não cadastrado')
    ##Fim da função que verifica se o login do usuário operador corresponde com o que está no BD
    
    ##Função que carrega o que está no BD e coloca no nosso Treeview
    def carregar_produto(self):
        self.tv.delete(*self.tv.get_children())     ##Apagando tudo que por ventura possa está no Treeview
        vquery="SELECT * FROM produtos ORDER BY nome ASC"     ##Varrendo as tuplas do banco de dados e ordenando de forma alfabética
        linhas=banco.dql(vquery)                    ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas:                            ##For para tirar o que está na váriavel linhas e jogar no nosso Treeview
            self.tv.insert('','end',values=i)       ##Inserindo valores no TreeView
    ##Fim da função que carrega o que está no BD e coloca no nosso Treeview
    
    ##Definindo função responsável por cadastrar produtos no BD
    def inserir_produto(self):
        if self.vcod.get()=='' or self.vcnome.get()=='' or  self.vcquant.get()=='' or  self.vcprecoc.get()=='' or  self.vcprecov.get()=='':##Garantindo que todos os dados do produto seram inseridos
            messagebox.showinfo(title='Erro', message='Digite todos os dados do produto')
            return
        try:
            vquery="INSERT INTO produtos (codigo,nome,quantidade,preco_compra,preco_venda) VALUES('"+self.vcod.get()+"','"+self.vcnome.get()+"','"+self.vcquant.get()+"','"+self.vcprecoc.get()+"','"+self.vcprecov.get()+"')" ##Inserindo o que foi digitado pelo usuário na base de dados
            banco.dml(vquery) ##Usando função responsável por executar ações no banco de dados
        except:
            messagebox.showinfo(title='Erro', message='Erro ao cadastrar o produto') ##Caso usuário esqueça de digitar algum dado do produto, será mostrado uma tela de erro
            return
        self.carregar_produto()     ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        self.vcod.delete(0,END)     ##Apagando código digitado pelo usuário para não haver erro de digitação
        self.vcnome.delete(0,END)   ##Apagando nome digitado pelo usuário para não haver erro de digitação
        self.vcquant.delete(0,END)  ##Apagando quantidade digitado pelo usuário para não haver erro de digitação
        self.vcprecoc.delete(0,END) ##Apagando preco de compra digitado pelo usuário para não haver erro de digitação
        self.vcprecov.delete(0,END) ##Apagando preco de venda digitado pelo usuário para não haver erro de digitação
        self.vcod.focus()           ##Deixando cursor na primeira entry
    ###Fim da função responsável por cadastrar produtos no BD
    
    ##Definindo função responsável por realizar pesquisa de produtos com o código digitado pelo usuário na base de dados
    def pesquisar_produto(self):
        self.tv.delete(*self.tv.get_children())  ##Apagando algo que por ventura não deveria está lá
        vquery="SELECT * FROM produtos WHERE nome LIKE '%"+self.vcnome.get()+"%'"##Pegando o que foi digitado pelo usuário e comparando ao que tem no bd
        linhas=banco.dql(vquery)##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas: ##Retornando no treeview o que foi encontrando com base no que foi digitado pelo usuário
            self.tv.insert('','end',values=i)
        self.vcnome.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
    ##Fim da função responsável por realizar pesquisa de produtos com o código digitado pelo usuário na base de dados
    
    ##Definindo função responsável por deletar produto com base no que o usuário selecionar
    def deletar_produto(self):
        try:
            codigo=-1                           ##Criando variável para pegar o código escolhido pelo usuário
            item=self.tv.selection()[0]         ##Criando item que receberá o que o código que o usuário clicar
            valores=self.tv.item(item,"values") ##Capturando valor
            codigo=valores[0]                   ##Atribuindo valor na variável
            vquery="DELETE FROM produtos WHERE codigo="+codigo ##Usando variável para buscar o produto no bd
            banco.dml(vquery)                   ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
            self.tv.delete(item)                ##Esquecendo o que foi escolhido pelo usuário
        except:                                 ##Exceção por erro
            messagebox.showinfo(title='Erro', message='Erro ao apagar produto') ##Retornando erro
    ##Fim da função responsável por deletar produto com base no que o usuário selecionar

    ##Definindo função responsável por preencher Treeview com o que está na base de dados
    def carregar_funcionario(self):
        self.tv_funcionario.delete(*self.tv_funcionario.get_children())##Apagando o que por ventura não deveria está
        vquery="SELECT * FROM funcionarios ORDER BY nome ASC"##Pegando todos os funcionários que estão no bd
        linhas=banco.dql(vquery)##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas:##Colocando tudo que foi pego no bd no treeview
            self.tv_funcionario.insert('','end',values=i)
    ##Fim da função responsável por preencher Treeview com o que está na base de dados

    ##Definindo função responsável por cadastrar funcionários na BD
    def inserir_funcionario(self):
        if self.vcmat.get()=='' or self.lbnom.get()=='' or self.lbcar.get()=='' or self.lbdata.get()=='':
            messagebox.showinfo(title='Erro', message='Digite todos os dados do funcionário')
            return
        try:
            vquery="INSERT INTO funcionarios (matricula,nome,cargo,data_de_entrada) VALUES('"+self.vcmat.get()+"','"+self.lbnom.get()+"','"+self.lbcar.get()+"','"+self.lbdata.get()+"')"
            banco.dml(vquery) ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        except:
            messagebox.showinfo(title='Erro', message='Erro ao cadastrar o funcionário,TENTE NOVAMENTE')
            return
        self.carregar_funcionario()##Recarregando bd para que a atualização seja mostrada sem haver necessidade de fechar a janela
        self.vcmat.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
        self.lbnom.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
        self.lbcar.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
        self.lbdata.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
        self.vcmat.focus()##Retornando cursor para a entry matricula
    ##Fim da função responsável por cadastrar funcionários na BD

    ##Definindo função responsável por deletar funcionário com base no que o usuário selecionar
    def deletar_funcionario(self):
        try:
            matricula=-1 ##Criando variável que receberá o valor que for escolhido pelo usuário
            item=self.tv_funcionario.selection()[0]##Criando ponteiro que mostrará o valor 
            valores=self.tv_funcionario.item(item,"values")##Capturando valor
            matricula=valores[0]##Atribuindo valor na variável
            vquery="DELETE FROM funcionarios WHERE matricula="+matricula##Criando ação para apagar o cadastro do funcionário
            banco.dml(vquery) ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
            self.tv_funcionario.delete(item)##Apagando o que foi digitado para não haver erro de digitação
        except:           ##Exceção por erro
            messagebox.showinfo(title='Erro', message='CLIQUE EM CIMA DA MATRICULA DO FUNCIONÁRIO') ##Retornando erro
    ##Fim da função responsável por deletar funcionário com base no que o usuário selecionar

    ##Definindo função responsável por realizar pesquisa de funcionário 
    def pesquisar_funcionario(self):
        self.tv_funcionario.delete(*self.tv_funcionario.get_children()) ##Deletando tudo que não deveria está no treeview
        vquery="SELECT * FROM funcionarios WHERE matricula LIKE '%"+self.vcmat.get()+"%'"##Pegando matrícula informada pelo usuário e comparando no bd
        linhas=banco.dql(vquery) ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas:         ##Retornando no treeview o que foi encontrado
            self.tv_funcionario.insert('','end',values=i)
        self.vcmat.delete(0,END)##Apagando valor digitado pelo usuário para não haver erro de digitação
    ##Fim da função responsável por realizar pesquisa de funcionário
    
    ##Definindo função responsável por carregar os dados de login gerente no treeview
    def carregar_login_gerente(self):
       self.tv_gerentes.delete(*self.tv_gerentes.get_children())
       vquery="SELECT * FROM login_gerente ORDER BY id ASC"
       linhas=banco.dql(vquery)
       for i in linhas:
           self.tv_gerentes.insert('','end',values=i)
   ##Fim da função  responsável por carregar os dados de login gerente no treeview
   
   ##Definindo função reponsável por cadastrar login dos gerentes
    def cadastrar_login_gerente(self):
        if self.id_gerente.get()=='' or self.senha_gerente.get()=='':
            messagebox.showinfo(title='Erro', message='Digite todos os dados de login do gerente')
            return
        try:
            vquery="INSERT INTO login_gerente (id,senha) VALUES('"+self.id_gerente.get()+"','"+self.senha_gerente.get()+"')"
            banco.dml(vquery)
        except:
             messagebox.showinfo(title='Erro', message='Erro ao cadastrar o login') 
             return
        self.carregar_login_gerente()
        self.id_gerente.delete(0,END)
        self.senha_gerente.delete(0,END)
        self.id_gerente.focus()
    ##Fim da função reponsável por cadastrar login dos gerentes

    ##Definindo função responsável por buscar os dados de login dos gerentes
    def pesquisar_login_gerente(self):
        self.tv_gerentes.delete(*self.tv_gerentes.get_children())
        vquery="SELECT * FROM login_gerente WHERE id LIKE '%"+self.id_gerente.get()+"%'"
        linhas=banco.dql(vquery) ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas:         ##Retornando no treeview o que foi encontrado
            self.tv_gerentes.insert('','end',values=i)
        self.id_gerente.delete(0,END)##Apagando valor digitado pelo usuário para não haver erro de digitação
        self.id_gerente.focus()
    ##Fim da função responsável por buscar os dados de login dos gerentes
    
    ##Definindo onde o operador consulta o estoque
    def carregar_produto_estoque(self):
        self.tv_estoque.delete(*self.tv_estoque.get_children()) ##Apagando tudo que por ventura possa está no Treeview
        vquery="SELECT codigo,nome,quantidade,preco_venda FROM produtos ORDER BY nome ASC"     ##Varrendo as tuplas do banco de dados e ordenando de forma alfabética
        linhas=banco.dql(vquery)                    ##Atribuindo o que está no banco de dados a linhas
        for i in linhas:                            ##For para tirar o que está na váriavel linhas e jogar no nosso Treeview
            self.tv_estoque.insert('','end',values=i) ##Inserindo valores no TreeView          
    ##Fim da função  onde o operador consulta o estoque
    
    ##Definindo função reponsável por apagar os dados de login gerentes na base da dados
    def apagar_login_gerente(self):
        if self.id_gerente.get()=='':
            messagebox.showinfo(title='Erro',message='Insira o id do usuário que você deseja apagar!')
        else:
            vquery="DELETE FROM login_gerente WHERE id LIKE '%"+self.id_gerente.get()+"%'"
            banco.dml(vquery)
            self.carregar_login_gerente()
            self.id_gerente.delete(0,END)##Apagando valor digitado pelo usuário para não haver erro de digitação
            self.id_gerente.focus()              
    ##Fim da função reponsável por apagar os dados de login gerentes na base da dados
    
    ##Definindo função responsável por carregar login dos operadores para o treeview
    def carregar_login_operador(self):
       self.tv_operadores.delete(*self.tv_operadores.get_children())
       vquery="SELECT * FROM login_operador ORDER BY id ASC"
       linhas=banco.dql(vquery)
       for i in linhas:
           self.tv_operadores.insert('','end',values=i)
    ##Fim da função responsável por carregar login dos operadores para o treeview

    ##Definindo função responsável por cadastrar os login dos operadores
    def cadastrar_login_operador(self):
        if self.id_operador.get()=='' or self.senha_operador.get()=='':
            messagebox.showinfo(title='Erro', message='Digite todos os dados de login do gerente')
            return
        try:
            vquery="INSERT INTO login_operador (id,senha) VALUES('"+self.id_operador.get()+"','"+self.senha_operador.get()+"')"
            banco.dml(vquery)
        except:
             messagebox.showinfo(title='Erro', message='Erro ao cadastrar o login') 
             return
        self.carregar_login_operador()
        self.id_operador.delete(0,END)
        self.senha_operador.delete(0,END)
        self.id_operador.focus()
    ##Fim da função responsável por cadastrar os login dos operadores
    
    ##Definindo função responsável por buscar login dos operadores na base de dados e retornar no treeview
    def buscar_login_operador(self):
        self.tv_operadores.delete(*self.tv_operadores.get_children())
        vquery="SELECT * FROM login_operador WHERE id LIKE '%"+self.id_operador.get()+"%'"
        linhas=banco.dql(vquery) ##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas:         ##Retornando no treeview o que foi encontrado
            self.tv_operadores.insert('','end',values=i)
        self.id_operador.delete(0,END)##Apagando valor digitado pelo usuário para não haver erro de digitação
        self.id_operador.focus()
    ##Fim da função responsável por buscar login dos operadores na base de dados e retornar no treeview
    
    ##Definindo função responsável por apagar dados de login do operador na base da dados
    def apagar_login_operador(self):
        if self.id_operador.get()=='':
            messagebox.showinfo(title='Erro',message='Insira o id do usuário que você deseja apagar!')
        else:
            vquery="DELETE FROM login_operador WHERE id LIKE '%"+self.id_operador.get()+"%'"
            banco.dml(vquery)
            self.carregar_login_operador()
            self.id_operador.delete(0,END)##Apagando valor digitado pelo usuário para não haver erro de digitação
            self.id_operador.focus()  
    ##Fim da função responsável por apagar dados de login do operador na base da dados


    ##Definindo função responsável por permitir ao operador consultar produtos no BD
    def consultar_produto(self):
        self.tv_estoque.delete(*self.tv_estoque.get_children())  ##Apagando algo que por ventura não deveria está lá
        vquery="SELECT * FROM produtos WHERE nome LIKE '%"+self.cnome_estoque.get()+"%'"##Pegando o que foi digitado pelo usuário e comparando ao que tem no bd
        linhas=banco.dql(vquery)##Usando função criada para acionar o bd e atribuindo a função que ela deve executar
        for i in linhas: ##Retornando no treeview o que foi encontrando com base no que foi digitado pelo usuário
            self.tv_estoque.insert('','end',values=i)
        self.cnome_estoque.delete(0,END)##Apagando o que foi digitado para não haver erro de digitação
    ##Fim da função responsável por permitir ao operador consultar produtos no BD
###########Fim da classe funcão responsável por deletar produto com base no que o usuário selecionar



###########Criando classe programa
class programa(funcs):
    ##Função que cria a tela inicial
    def __init__(self):
        self.Escolha=Tk()                   ##Moldando a tela
        self.Escolha.title('Bem vindo')
        self.Escolha.geometry('300x400')
        self.fontePadrao = ('Arial', '10')
        self.Escolha.resizable(False, False)
        self.Escolha.maxsize(width=900, height=700)
        self.Escolha.minsize(width=400, height=300)
        self.fechar=Button(text='Encerrar programa',command=self.Escolha.destroy)
        self.fechar.pack()
        self.escolher=Button(text='Gerente',height = 10,width = 30,font=self.fontePadrao,command=self.login_gerente)
        self.escolher.pack()
        self.escolher_2=Button(text='Operador',height=10,width=30,font=self.fontePadrao,command=self.login_operador)
        self.escolher_2.pack()
        self.Escolha.mainloop()
    ##Fim da função que cria a tela inicial
    
    ##Função da janela login, que solicita id e senha do usuário
    def login_gerente(self):
        self.Escolha.destroy()              ##Fechado janela anterior
        self.Janela=Tk()                    ##Moldando a tela de login
        self.Janela.title('Login')
        self.Janela.geometry('200x300')
        self.Janela.resizable(False,False)
        self.fontePadrao = ('Arial', "10")
        self.container1 = Frame(self.Janela)
        self.container1['pady'] = 30
        self.container1.pack()
        self.containerDados1 = Frame(self.Janela)
        self.containerDados1['padx'] = 50
        self.containerDados1.pack()
        self.containerDados2 = Frame(self.Janela)
        self.containerDados2['padx'] = 50
        self.containerDados2.pack()
        self.containerBotao = Frame(self.Janela)
        self.containerBotao['pady'] = 30
        self.containerBotao.pack()
        self.titulo = Label(self.container1, text='LOGIN')
        self.titulo['font'] = ('Arial', '10', 'bold')
        self.titulo.pack()
        self.loginId = Label(self.containerDados1, text='ID:')
        self.loginId['font'] = self.fontePadrao
        self.loginId.pack()
        self.usuario = Entry(self.containerDados1)
        self.usuario["width"] = 30
        self.usuario.pack()
        self.loginSenha = Label(self.containerDados2, text='Senha:')
        self.loginSenha['font'] = self.fontePadrao
        self.loginSenha.pack()
        self.senha= Entry(self.containerDados2, show='*')
        self.senha["width"] = 30
        self.senha.pack()
        self.entrar=Button(text='Entrar',command=self.verificar_login_gerente)
        self.entrar.pack()
        self.Janela.mainloop()
    ##Fim da função da janela login, que solicita id e senha do usuário
    
    ##Definindo tela de login para o operador
    def login_operador(self):
        self.Escolha.destroy()
        self.jane=Tk()   #Moldando a tela
        self.jane.title('Login')
        self.jane.geometry('200x300')
        self.jane.resizable(False,False)
        self.fontePadrao = ('Arial', '12')
        self.container1 = Frame(self.jane)
        self.container1['pady'] = 20
        self.container1.pack()
        self.containerDados1 = Frame(self.jane)
        self.containerDados1['padx'] = 50
        self.containerDados1.pack()
        self.containerDados2 = Frame(self.jane)
        self.containerDados2['padx'] = 50
        self.containerDados2.pack()
        self.containerBotao = Frame(self.jane)
        self.containerBotao['pady'] = 30
        self.containerBotao.pack()
        self.titulo = Label(self.container1, text='LOGIN')
        self.titulo['font'] = ('Arial', '10', 'bold')
        self.titulo.pack()
        self.login_Id = Label(self.containerDados1, text='ID:')
        self.login_Id['font'] = self.fontePadrao
        self.login_Id.pack()
        self.pega_usuario = Entry(self.containerDados1)
        self.pega_usuario["width"] = 30
        self.pega_usuario.pack()
        self.login_Senha = Label(self.containerDados2, text='Senha:')
        self.login_Senha['font'] = self.fontePadrao
        self.login_Senha.pack()
        self.pega_senha= Entry(self.containerDados2, show='*')
        self.pega_senha["width"] = 30
        self.pega_senha.pack()
        self.confirmar=Button(text='Entrar',command=self.verificar_login_operador)
        self.confirmar.pack()
        self.jane.mainloop() 
    ##Fim da função tela login operador
    
    #Definindo a tela do aplicativo destinada ao gerente
    def tela_gerente(self):
        self.container1.pack_forget() #Apagando dados da tela
        self.containerDados1.pack_forget()
        self.containerDados2.pack_forget()
        self.Janela.destroy() #Fechando janela anterior
        self.principal = Tk() #Moldando tela
        self.fechar=Button(text='Encerrar programa',command=self.principal.destroy)
        self.fechar.pack()
        msg_bemvindo=Label(self.principal, text='Bem-vindo')
        msg_bemvindo.configure(background='#49A')
        msg_bemvindo['font']=('Arial', '12')
        msg_bemvindo.pack()
        self.principal.title('Gerência')
        self.principal.geometry('800x600')
        self.principal.resizable(False, False)
        self.principal.configure(background='#49A')
        self.fontePadrao = ('Arial','12')
        self.opcao=Button(text='Gerenciar produtos',foreground='white',background='#49A',height = 10,width = 30,font=self.fontePadrao,command=self.gerenciar_produtos)
        self.opcao.place(x=1,y=2)
        self.opcao_2=Button(text='Gerenciar funcionários',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=self.gerenciar_funcionario)
        self.opcao_2.place(x=1,y=200)
        self.opcao_3=Button(text='Consultar fornecedores',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=carregar_fornecedores)
        self.opcao_3.place(x=520,y=200)
        self.opcao_4=Button(text='Lista de pedidos',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=carregar_pedidos)
        self.opcao_4.place(x=520,y=2)
        self.opcao_5=Button(text='Gerenciar login gerentes',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=self.gerenciar_login_gerentes)
        self.opcao_5.place(x=1,y=400)
        self.opcao_6=Button(text='Gerenciar login operadores',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=self.gerenciar_login_operadores)
        self.opcao_6.place(x=520,y=400)
        self.principal.mainloop()
    ##Fim da função que define a tela do aplicativo destinada ao gerente
    
    ##Definindo função para gerenciamento de estoque
    def gerenciar_produtos(self):
        self.janela1=Tk()
        self.janela1.title('Estoque')
        self.janela1.configure(background='light blue')
        self.janela1.geometry('700x500')
        self.janela1.resizable(False,False)
        self.frame1=LabelFrame(self.janela1,text='Produtos em estoque')
        self.frame1.pack(pady=10,padx=10)
        self.tv=ttk.Treeview(self.frame1,columns=('codigo','nome','quantidade','precocompra','precovenda'),show='headings')
        self.tv.column('codigo',minwidth=0,width=100)
        self.tv.column('nome',minwidth=0,width=150)
        self.tv.column('quantidade',minwidth=0,width=150)
        self.tv.column('precocompra',minwidth=0,width=100)
        self.tv.column('precovenda',minwidth=0,width=100)
        self.tv.heading('codigo',text='Código')
        self.tv.heading('nome',text='Nome')
        self.tv.heading('quantidade',text='Quantidade disponivel')
        self.tv.heading('precocompra',text='Preço de compra')
        self.tv.heading('precovenda',text='Preço de venda')
        self.tv.pack()
        self.carregar_produto()
        self.frame2=LabelFrame(self.janela1,text='Alterar estoque')
        self.frame2.place(width=650,height=200)
        self.frame2.place(x=47,y=260)
        self.vcod=Label(self.frame2,text='Código')
        self.vcod.pack(side='left')
        self.vcod=Entry(self.frame2)
        self.vcod.pack(side='left',padx=10)
        self.lbnome=Label(self.frame2,text='Nome')
        self.lbnome.pack(side='left')
        self.vcnome=Entry(self.frame2)
        self.vcnome.pack(side='left',padx=10)
        self.lbquant=Label(self.frame2,text='Quantidade')
        self.lbquant.pack(side='left',padx=10)
        self.vcquant=Entry(self.frame2)
        self.vcquant.pack(side='left',padx=10)
        self.lbprecoc=Label(self.frame2,text='Preço de compra')
        self.lbprecoc.place(x=1,y=115)
        self.vcprecoc=Entry(self.frame2)
        self.vcprecoc.place(x=100,y=118)
        self.lprecov=Label(self.frame2,text='Preço de venda')
        self.lprecov.place(x=230,y=115)
        self.vcprecov=Entry(self.frame2)
        self.vcprecov.place(x=320,y=118)
        self.bt_inserir=Button(self.frame2,text='Cadastrar',bd=4,bg='#107db2',command=self.inserir_produto)
        self.bt_inserir.place(x=10,y=5,width=100,height=40)
        self.bt_buscar=Button(self.frame2,text='Buscar',bd=4,bg='#107db2',command=self.pesquisar_produto)
        self.bt_buscar.place(x=110,y=5,width=100,height=40)
        self.bt_mostrar=Button(self.frame2,text='Mostrar todos',bd=4,bg='#107bd2',command=self.carregar_produto)
        self.bt_mostrar.place(x=210,y=5,width=100,height=40)
        self.bt_apagar=Button(self.frame2,text='Apagar produto',bd=4,bg='#107db2',command=self.deletar_produto)
        self.bt_apagar.place(x=520,y=5,width=100,height=40)
        self.janela1.mainloop()
    ##Fim da função para gerenciamento de estoque
    
    ##Definindo função para gerenciamento de quadro de funcionários
    def gerenciar_funcionario(self):
        self.janela10=Tk()
        self.janela10.title('Quadro de funcionários')
        self.janela10.configure(background='light blue')
        self.janela10.geometry('700x500')
        self.janela10.resizable(False,False)
        self.frame10=LabelFrame(self.janela10,text='Produtos em estoque')
        self.frame10.pack(pady=10,padx=10)
        self.tv_funcionario=ttk.Treeview(self.frame10,columns=('matricula','nome','cargo','data de admissao'),show='headings')
        self.tv_funcionario.column('matricula',minwidth=0,width=100)
        self.tv_funcionario.column('nome',minwidth=0,width=200)
        self.tv_funcionario.column('cargo',minwidth=0,width=200)
        self.tv_funcionario.column('data de admissao',minwidth=0,width=150)
        self.tv_funcionario.heading('matricula',text='Matrícula')
        self.tv_funcionario.heading('nome',text='Nome')
        self.tv_funcionario.heading('cargo',text='Cargo')
        self.tv_funcionario.heading('data de admissao',text='Data de admissão')
        self.tv_funcionario.pack()
        self.carregar_funcionario()
        self.frame20=LabelFrame(self.janela10,text='Gerenciar quadro de funcionários')
        self.frame20.place(width=650,height=200)
        self.frame20.place(x=30,y=260)
        self.vcmat=Label(self.frame20,text='Matrícula')
        self.vcmat.pack(side='left')
        self.vcmat=Entry(self.frame20)
        self.vcmat.pack(side='left',padx=10)
        self.lbnom=Label(self.frame20,text='Nome')
        self.lbnom.pack(side='left')
        self.lbnom=Entry(self.frame20)
        self.lbnom.pack(side='left',padx=10)
        self.lbcar=Label(self.frame20,text='Cargo')
        self.lbcar.pack(side='left',padx=10)
        self.lbcar=Entry(self.frame20)
        self.lbcar.pack(side='left',padx=10)
        self.lbdata=Label(self.frame20,text='Data de admissão')
        self.lbdata.place(x=1,y=115)
        self.lbdata=Entry(self.frame20)
        self.lbdata.place(x=100,y=118)
        self.inserir=Button(self.frame20,text='Cadastrar funcionário',bd=4,bg='#107db2',command=self.inserir_funcionario)
        self.inserir.place(x=10,y=5,width=125,height=40)
        self.buscar=Button(self.frame20,text='Buscar funcionário',bd=4,bg='#107db2',command=self.pesquisar_funcionario)
        self.buscar.place(x=135,y=5,width=125,height=40)
        self.mostrar=Button(self.frame20,text='Mostrar todos',bd=4,bg='#107bd2',command=self.carregar_funcionario)
        self.mostrar.place(x=260,y=5,width=100,height=40)
        self.apagar=Button(self.frame20,text='Apagar funcionário',bd=4,bg='#107db2',command=self.deletar_funcionario)
        self.apagar.place(x=520,y=5,width=125,height=40)
        self.janela10.mainloop()
    ##Fim da função para gerenciamento de quadro de funcionários
    
    ##Definindo função responsável pela tela do aplicativo destinada ao operador 
    def tela_operador(self):
        self.container1.pack_forget() #Apagando dados da tela
        self.containerDados1.pack_forget()
        self.containerDados2.pack_forget()
        self.jane.destroy() #Fechando janela anterior
        self.principall=Tk() #Moldando tela
        self.fechar=Button(text='Encerrar programa')
        self.fechar.pack()
        self.fechar['command']=self.principall.destroy #Opção de fechar o aplicativo
        msg_bemvindo=Label(self.principall, text='Bem-vindo')
        msg_bemvindo['font']=('Arial', '12')
        msg_bemvindo.configure(background='#49A')
        msg_bemvindo.pack()
        self.principall.title('Operador')
        self.principall.resizable(False,False)
        self.op=Button(text='Estoque',foreground='white',background='#49A',height = 10,width = 30,font=self.fontePadrao,command=self.consulta_estoque)
        self.op.place(x=1,y=2)
        self.op1=Button(text='Lista de pedidos',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=carregar_pedidos)
        self.op1.place(x=520,y=2)
        self.op2=Button(text='Consultar fornecedores',foreground='white',background='#49A',height=10,width=30,font=self.fontePadrao,command=carregar_fornecedores)
        self.op2.place(x=520,y=200)
        self.principall.geometry('800x600')
        self.principall.configure(background='#49A')
        self.principall.mainloop()
    ###Fim da função responsável pela tela do aplicativo destinada ao operador

    ##Definindo função que permite controlar o login dos gerentes na base de dados
    def gerenciar_login_gerentes(self):
        self.janela500=Tk()
        self.janela500.title('Logins')
        self.janela500.configure(background='light blue')
        self.janela500.geometry('700x500')
        self.janela500.resizable(False,False)
        self.frame500=LabelFrame(self.janela500,text='Logins dos gerentes')
        self.frame500.pack(pady=10,padx=10)
        self.tv_gerentes=ttk.Treeview(self.frame500,columns=('id','senha'),show='headings')
        self.tv_gerentes.column('id',minwidth=0,width=300)
        self.tv_gerentes.column('senha',minwidth=0,width=300)
        self.tv_gerentes.heading('id',text='Id')
        self.tv_gerentes.heading('senha',text='Senha')
        self.frame21=LabelFrame(self.janela500,text='Dados gerentes')
        self.frame21.place(width=650,height=200)
        self.frame21.place(x=47,y=260)
        self.id=Label(self.frame21,text='Id')
        self.id.pack(side='left',padx=10)
        self.id_gerente=Entry(self.frame21)
        self.id_gerente.pack(side='left',padx=10)
        self.sen=Label(self.frame21,text='Senha')
        self.sen.pack(side='left',padx=10)
        self.senha_gerente=Entry(self.frame21)
        self.senha_gerente.pack(side='left',padx=10)
        self.bt_inserir=Button(self.frame21,text='Cadastrar login',bd=4,bg='#107db2',command=self.cadastrar_login_gerente)
        self.bt_inserir.place(x=10,y=5,width=100,height=40)
        self.bt_buscar=Button(self.frame21,text='Buscar login',bd=4,bg='#107db2',command=self.pesquisar_login_gerente)
        self.bt_buscar.place(x=110,y=5,width=100,height=40)
        self.bt_mostrar=Button(self.frame21,text='Mostrar todos',bd=4,bg='#107bd2',command=self.carregar_login_gerente)
        self.bt_mostrar.place(x=210,y=5,width=100,height=40)
        self.bt_apagar=Button(self.frame21,text='Apagar login',bd=4,bg='#107db2',command=self.apagar_login_gerente)
        self.bt_apagar.place(x=520,y=5,width=100,height=40)
        self.tv_gerentes.pack()
        self.carregar_login_gerente()
    ##Fim da função que permite controlar o login dos gerentes na base de dados
    
    ##Definindo função que permite controlar o login dos operadores na base de dados
    def gerenciar_login_operadores(self):
        self.janela800=Tk()
        self.janela800.title('Logins')
        self.janela800.configure(background='light blue')
        self.janela800.geometry('700x500')
        self.frame800=LabelFrame(self.janela800,text='Logins dos operadores')
        self.frame800.pack(pady=10,padx=10)
        self.tv_operadores=ttk.Treeview(self.frame800,columns=('id','senha'),show='headings')
        self.tv_operadores.column('id',minwidth=0,width=300)
        self.tv_operadores.column('senha',minwidth=0,width=300)
        self.tv_operadores.heading('id',text='Id')
        self.tv_operadores.heading('senha',text='Senha')
        self.frame39=LabelFrame(self.janela800,text='Dados operadores')
        self.frame39.place(width=650,height=200)
        self.frame39.place(x=47,y=260)
        self.id_operador=Label(self.frame39,text='Id')
        self.id_operador.pack(side='left',padx=10)
        self.id_operador=Entry(self.frame39)
        self.id_operador.pack(side='left',padx=10)
        self.sen_operador=Label(self.frame39,text='Senha')
        self.sen_operador.pack(side='left',padx=10)
        self.senha_operador=Entry(self.frame39)
        self.senha_operador.pack(side='left',padx=10)
        self.bt_inserir=Button(self.frame39,text='Cadastrar login',bd=4,bg='#107db2',command=self.cadastrar_login_operador)
        self.bt_inserir.place(x=10,y=5,width=100,height=40)
        self.bt_buscar=Button(self.frame39,text='Buscar login',bd=4,bg='#107db2',command=self.buscar_login_operador)
        self.bt_buscar.place(x=110,y=5,width=100,height=40)
        self.bt_mostrar=Button(self.frame39,text='Mostrar todos',bd=4,bg='#107bd2',command=self.carregar_login_operador)
        self.bt_mostrar.place(x=210,y=5,width=100,height=40)
        self.bt_apagar=Button(self.frame39,text='Apagar login',bd=4,bg='#107db2',command=self.apagar_login_operador)
        self.bt_apagar.place(x=520,y=5,width=100,height=40)
        self.tv_operadores.pack()
        self.carregar_login_operador()
    ##Fim da função que permite controlar o login dos operadores na base de dados
    
    ##Função responsável por apresentar o estoque na tela do operador
    def consulta_estoque(self):
        self.janela5=Tk()
        self.janela5.title('Estoque')
        self.janela5.configure(background='light blue')
        self.janela5.geometry('700x500')
        self.frame5=LabelFrame(self.janela5,text='Produtos')
        self.frame5.pack(pady=10,padx=10)
        self.tv_estoque=ttk.Treeview(self.frame5,columns=('codigo','nome','quantidade','precovenda'),show='headings')
        self.tv_estoque.column('codigo',minwidth=0,width=100)
        self.tv_estoque.column('nome',minwidth=0,width=100)
        self.tv_estoque.column('quantidade',minwidth=0,width=200)
        self.tv_estoque.column('precovenda',minwidth=0,width=100)
        self.tv_estoque.heading('codigo',text='Código')
        self.tv_estoque.heading('nome',text='Nome')
        self.tv_estoque.heading('quantidade',text='Quantidade disponivel')
        self.tv_estoque.heading('precovenda',text='Preço')
        self.tv_estoque.pack()
        self.carregar_produto_estoque()
        self.frame15=LabelFrame(self.janela5,text='Pesquisar')
        self.frame15.place(width=650,height=200)
        self.frame15.place(x=47,y=260)
        self.nome_estoque=Label(self.frame15,text='Nome')
        self.nome_estoque.pack(side='left')
        self.cnome_estoque=Entry(self.frame15)
        self.cnome_estoque.pack(side='left',padx=10)
        self.consultar=Button(self.frame15,text='Buscar',bd=4,bg='#107db2',command=self.consultar_produto)
        self.consultar.place(x=30,y=5,width=100,height=40)
        self.mostrar=Button(self.frame15,text='Mostrar todos',bd=4,bg='#107bd2')
        self.mostrar.place(x=130,y=5,width=100,height=40)
        self.janela5.mainloop()
    ##Fim da função responsável por apresentar o estoque na tela do operador



##Programa principal
aplication=programa()

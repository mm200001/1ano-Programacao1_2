author = "Marcos Leitão, 55852"
author = "Miguel Fernandes, 56909"

# $ python projeto.py xadrez.csv anos 

import csv
from itertools import groupby
from functools import reduce
from matplotlib import pyplot  as plt
import math
from operator import add, itemgetter
import numpy as np
import re
from collections import Counter  

####################################################################################################################
#######################################################################################################################
def ler_csv_dicionario(nome_ficheiro):
    """Função que lê um ficheiro csv

    Args:
        nome_ficheiro (str): nome do ficheiro csv

    Returns:
        list: retorna uma lista de dicionários
    """
    with open(nome_ficheiro, 'r', encoding='utf-8') as ficheiro_csv:
        return list(csv.DictReader(ficheiro_csv, delimiter = ","))
#######################################################################################################################
########################################--> FUNÇÃO ANOS <--############################################################

def get_ano(data):
    """Obtem o ano de uma dada data

    Args:
        data (str): data em string

    Returns:
        str: retorna o ano em string
    """
    return data.split("-")[0]

def get_numero_jogos_do_ano(ano,datas):
    """obtem o numero de jogos de cada ano

    Args:
        ano (int): o ano em inteiro
        datas (list): lista de anos

    Returns:
        int: retorna o número de jogos do ano
    """
    contador = 0
    for data in datas:
        if data == ano:
            contador +=1
    return contador

def get_lista_numero_jogos_dos_anos(abcissas,datas):
    """obtem a lista de numero jogos

    Args:
        abcissas (list): lista de anos
        datas (list): lista de anos com repetições

    Returns:
        list: retorna a lista de numero jogos, lista já ordenada
    """
    return list(map(lambda x: get_numero_jogos_do_ano(x,datas) ,abcissas))

def get_numeroJogadoras(abcissa,datas,jogadoras):
    """obtem o numero de jogadoras

    Args:
        abcissa (int): ano 
        datas (list): lista de anos com repetições
        jogadoras (list): lista de jogadoras

    Returns:
        int: retorna numero de jogadoras
    """

    lista = []
    for d,j in zip(datas,jogadoras):
        if d == abcissa:
            if j[0] not in lista:
                lista.append(j[0])
            if j[1] not in lista: 
                lista.append(j[1]) 
    return len(lista)


def get_lista_numero_jogadoras(abcissas,datas,jogadoras): 
    """obtem a lista numero jogadoras

    Args:
        abcissas (list): lista de abcissas
        datas (list): lista de datas
        jogadoras (list): lista de jogadoras

    Returns:
        list: lista numero jogadoras
    """
    return reduce(lambda acc,abcissa: acc + [get_numeroJogadoras(abcissa,datas,jogadoras)], abcissas, [])

def gerar_grafico_anos(abcissas,ordenadasJogos,ordenadasJogadoras):
    """Cria o grafico da função anos

    Args:
        abcissas (list):lista de abcissas (anos)
        ordenadasJogos (list): lista das ordenadas (jogos)
        ordenadasJogadoras (list): lista das ordenadas (jogadoras)
    """ 

    plt.bar(abcissas,ordenadasJogos, color="green",label='#jogos')
    plt.xlabel('Ano')
    plt.ylabel('Jogos',color='green')
    plt.xticks(abcissas,rotation='vertical')
    plt.legend(loc=6)
    plt.twinx()
    plt.plot(abcissas,ordenadasJogadoras,color="blue",label='#jogadoras Diferentes')
    plt.ylabel('#Jogadoras diferentes',color='blue')
    plt.ylim(0,max(ordenadasJogadoras))
    plt.title('Jogos e jogadoras por ano')
    plt.legend( loc=2)
    plt.show()

def anos(nome_ficheiro): 
    """Gera gráfico da função anos

    Args:
        nome_ficheiro (str): nome do ficheiro csv
    """

    ficheiro_csv = ler_csv_dicionario(nome_ficheiro) 

    datas = [int(get_ano(linha['end_time'])) for linha in ficheiro_csv] 

    jogadoras = [(linha['white_username'],linha['black_username']) for linha in ficheiro_csv]

    abcissas = sorted(list(dict.fromkeys(datas)))

    ordenadasJogos = get_lista_numero_jogos_dos_anos(abcissas,datas)

    ordenadasJogadoras = get_lista_numero_jogadoras(abcissas,datas,jogadoras)

    gerar_grafico_anos(abcissas,ordenadasJogos,ordenadasJogadoras)

#######################################################################################################################
#################################--> FUNÇÃO CLASSES <-- ###############################################################

def get_numeroJogosformatoJogo(time_class,formatoJogo,dados_jogo):
    """obtem o numero de jogos por formato

    Args:
        time_class (str): um time class
        formatoJogo (str): um formato de jogo
        dados_jogo (list): lista de dados 

    Returns:
        int: retorna o numero de jogos por fomato de jogo
    """
    contador = 0
    for d in dados_jogo:
        if d[0] == time_class:
            if d[1] == formatoJogo:
                contador +=1
    return contador


def get_formatoJogo(dados):
    """obtem os formatos de jogo

    Args:
        dados (list): lista de dados

    Returns:
        list: lista de formatos de jogo
    """
    lista = []
    for d in dados:
        if d[1] not in lista:
            lista.append(d[1])
    return lista

def get_lista_numeroJogos_porFormato(time_class,formatosJogos,tipos_de_jogo): 
    """obtem a lista de numero de jogos por formato

    Args:
        time_class (str): um time class
        formatosJogos (list): lista de formatos de jogos
        tipos_de_jogo (list]): list tipo de jogos

    Returns:
        list: retorna uma lista com numero de jogos por formato
    """

    return list(map(lambda x:(x,get_numeroJogosformatoJogo(time_class,x,tipos_de_jogo)), formatosJogos))

def totalJogos_timeClass(time_class):
    """obtem o total de jogos de um time class

    Args:
        time_class (list): [description]

    Returns:
        int: retorna total jogos time class
    """
    contador = 0
    for jogos in time_class:
        contador += int(jogos[1])
    return contador


def get_lista_numeroJogos_timeClass(lista_name_time_class,lista_numeroJogos_Classes):
    """obtem lista numero jogos time class

    Args:
        lista_name_time_class (list): lista time class
        lista_numeroJogos_Classes ([type]): [description]

    Returns:
        tuplo: lista nomes time class, lista de total jogos time class
    """

    lista = list(map(lambda y: totalJogos_timeClass(y), lista_numeroJogos_Classes))

    return (lista_name_time_class,lista)

def gerar_grafico_classes(lista_classes):
    """Cria grafico classes

    Args:
        lista_classes (list): lista de classes
    """
    titulos = ['rapid','daily','bullet','blitz','time_class']
    linhas = math.ceil(len(lista_classes)/3)
    count = 0
    for n in range(len(lista_classes)):
        plt.subplot(linhas,3,n+1)
        if count != len(lista_classes)-1:
            abcissas = list(map(lambda x: x[0], lista_classes[count]))
            ordenadas = list(map(lambda x: x[1], lista_classes[count]))
            plt.bar(abcissas,ordenadas)
            plt.xticks(abcissas,rotation='vertical')
            count +=1
        else:
            plt.bar(lista_classes[count][0],lista_classes[count][1])
            plt.xticks(lista_classes[count][0],rotation='vertical')
        plt.ylabel('#jogos')
        plt.xlabel('Formato de jogo')
        plt.title(titulos[count])
    plt.tight_layout(pad=1.0)
    plt.show()


def classes(nome_ficheiro,n=5):
    """Mostra grafico classes

    Args:
        nome_ficheiro (str): nome ficheiro csv
        n (int, optional): numero de formatos apresentar, padrão é 5.
    """
    ficheiro_csv = ler_csv_dicionario(nome_ficheiro)

    tipos_de_jogo = [(linha['time_class'],linha['time_control']) for linha in ficheiro_csv]

    formatosJogos = get_formatoJogo(tipos_de_jogo)

    rapid = sorted(get_lista_numeroJogos_porFormato('rapid',formatosJogos,tipos_de_jogo),key=lambda x: x[1], reverse=True)

    daily = sorted(get_lista_numeroJogos_porFormato('daily',formatosJogos,tipos_de_jogo),key=lambda x: x[1], reverse=True)

    bullet = sorted(get_lista_numeroJogos_porFormato('bullet',formatosJogos,tipos_de_jogo),key=lambda x: x[1], reverse=True)                                                                                               

    blitz = sorted(get_lista_numeroJogos_porFormato('blitz',formatosJogos,tipos_de_jogo),key=lambda x: x[1], reverse=True)

    time_class = get_lista_numeroJogos_timeClass(['blitz','bullet','daily','rapid'],[blitz,bullet,daily,rapid])

    gerar_grafico_classes([rapid[:n],daily[:n],bullet[:n],blitz[:n],time_class])

#######################################################################################################################
###########################################--> FUNÇÃO VITORIAS <--#####################################################


def get_jogadoras(dados,function):
    """obtem jogadoras

    Args:
        dados (list): lista de dados
        function (function): função aplicar

    Returns:
        list: lista de jogadoras
    """

    return [ key.lower() for key, _ in groupby(dados,function) ]


def get_win(grupo,color): 
    """obtem vitorias

    Args:
        grupo (list): lista do grupo
        color (str): nome da cor result

    Returns:
        str: retorna win
    """

    if color == 'B':
        return grupo[0]['black_result'] 
    else:
        return grupo[0]['white_result'] 


def criar_dicionario_jogo(jogadoras): 
    """cria dicionario de jogo

    Args:
        jogadoras (list): lista de jogadoras

    Returns:
        dict: dicionario de jogo
    """
    return dict(list(map(lambda x: (x.lower(),[]),jogadoras)))

def get_gameWin(ficheiro_csv,color_result):
    """obtem o jogo win

    Args:
        ficheiro_csv (lista): lista de dados do jogo total
        color_result (str): nome cor da peça result

    Returns:
        list: lista de jogos ganhos filtrados
    """
    return list(filter(lambda l: l[color_result] == 'win', ficheiro_csv)) 

def get_totalGame(ficheiro_csv,color_result):
    """obtem os dados jogo total

    Args:
        ficheiro_csv (list): lista de dajos jogo total
        color_result (str): nome cor da peça result

    Returns:
        list: lista resultado filtrado
    """
    return list(filter(lambda l: l[color_result], ficheiro_csv)) 

def concatenar(agrupado,dicionarioJogadoras,color):
    """concatenar

    Args:
        agrupado (grupby): grupo
        dicionarioJogadoras (dict): dicionario de jogadoras
        color (str): cor peça

    Returns:
        dict: cocatenado e inserido
    """
    for key, group in agrupado:
        try:
            dicionarioJogadoras[key.lower()].append(get_win(list(group),color))
        except:
            pass 
    
    return dicionarioJogadoras


def contar_win(dicionarioJogadoras):
    """conta vitorias

    Args:
        dicionarioJogadoras (dict): dicionario jogadoras

    Returns:
        dict: dicionario jogadoras
    """
    for key, v in dicionarioJogadoras.items():
         dicionarioJogadoras[key.lower()] = len(v)
    return dicionarioJogadoras

def total_vitorias(dados,function): 
    """total vitorias

    Args:
        dados (list): lista de dados
        function (funcao): funcao a utilizar

    Returns:
        int: numero de viorias
    """
    lista = [ key.lower() for key, group in groupby(dados,function)] 
    return lista.count('win')


def procuraTotalGames(key,totalGames):
    """procura total de jogos

    Args:
        key (str): nome jogadoras
        totalGames (dict): dict total jogos

    Returns:
        int: total jogos
    """
    try:
        return totalGames[key]
    except:
        totalGames[key] = 0
        return totalGames[key]


def procuraGamesColorWin(key,colorGame):
    """procura de jogos por cor

    Args:
        key (str): nome jogadora
        colorGame (dict): dict

    Returns:
        int: numero jogos com a peça por cor
    """
    try:
        return colorGame[key]
    except:
        colorGame[key] = 0
        return colorGame[key][key]

def construirDicionarFinal(key,totalGamesWhites,totalGamesBlack,GamesWhiteWin,GamesBlackWin):
    """construir dict

    Args:
        key (str): nome jogadora
        totalGamesWhites (dict): dicionario total games white
        totalGamesBlack (dict): dicionario total games black
        GamesWhiteWin (dict): dicionario total games white win 
        GamesBlackWin (dict): dicionario total games black win
    """
    try: 
        percentagemWinBlack = (procuraGamesColorWin(key,GamesBlackWin) * 100) / procuraTotalGames(key,totalGamesBlack)
    except:
        percentagemWinBlack = 0
    
    try:
        percentagemWinWhite = (procuraGamesColorWin(key,GamesWhiteWin) * 100) / procuraTotalGames(key,totalGamesWhites)
    except:
        percentagemWinWhite = 0

    somaTotalJogos = procuraTotalGames(key,totalGamesWhites) + procuraTotalGames(key,totalGamesBlack)

    return(somaTotalJogos,percentagemWinWhite/100,percentagemWinBlack/100)

def gerarGraficosVitorias(dicionario):
    """criar grafico vitorias

    Args:
        dicionario (dict): dicionario de dados
    """

    labels = list(map(lambda x: x[0].lower(), dicionario))
    white = list(map(lambda x: x[1][0][1], dicionario))
    black = list(map(lambda x: x[1][0][2], dicionario))

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, white, width, color='grey',label='peças brancas')
    ax.bar(x + width/2, black, width, color='black',label='peças pretas')
    plt.legend()

    ax.set_xticks(x)
    ax.set_xticklabels(labels,rotation='vertical')

    plt.title('Percentagem de vitórias jogando com peças brancas/pretas')
    plt.xlabel('Jogadoras')
    plt.ylabel('Percentagem')
    

    fig.tight_layout()
    
    plt.show()


def vitorias(nome_ficheiro,command = None):
    """mostra grafico vitorias

    Args:
        nome_ficheiro (str): nome ficheiro csv
        command ([type], optional): comando inserido no terminal 
    """

    ficheiro_csv = ler_csv_dicionario(nome_ficheiro)

    dados = [(linha['white_username'],linha['white_result'],linha['black_username'],linha['black_result']) for linha in ficheiro_csv]

    jogadorasBlack,jogadorasWhite = get_jogadoras(dados, lambda x: x[2]),get_jogadoras(dados,lambda x: x[0])

    dict_Jogadoras_BlackWin,dict_Jogadoras_WhiteWin = criar_dicionario_jogo(jogadorasBlack),criar_dicionario_jogo(jogadorasWhite)

    dict_Jogadoras_Total_Jogos_black,dict_Jogadoras_Total_Jogos_white = criar_dicionario_jogo(jogadorasBlack),criar_dicionario_jogo(jogadorasWhite)

    game_black_win,game_white_win = get_gameWin(ficheiro_csv,'black_result'),get_gameWin(ficheiro_csv,'white_result')

    total_gameBlack,total_gameWhite = get_totalGame(ficheiro_csv,'black_result'),get_totalGame(ficheiro_csv,'white_result')

    agrupar_game_black_win,agrupar_game_white_win = groupby(game_black_win, lambda x: x['black_username']),groupby(game_white_win, lambda x: x['white_username'])

    agrupar_totalGame_black,agrupar_totalGame_white = groupby(total_gameBlack, lambda x: x['black_username']),groupby(total_gameWhite, lambda x: x['white_username'])  

    dict_Jogadoras_BlackWin_,dict_Jogadoras_WhiteWin_ = concatenar(agrupar_game_black_win,dict_Jogadoras_BlackWin,'B'),concatenar(agrupar_game_white_win,dict_Jogadoras_WhiteWin,'W')

    dict_Jogadoras_Total_Jogos_black_,dict_Jogadoras_Total_Jogos_white_  = concatenar(agrupar_totalGame_black,dict_Jogadoras_Total_Jogos_black,'B'),concatenar(agrupar_totalGame_white,dict_Jogadoras_Total_Jogos_white,'W')

    dict_Jogadoras_BlackWin__,dict_Jogadoras_WhiteWin__ = contar_win(dict_Jogadoras_BlackWin_),contar_win(dict_Jogadoras_WhiteWin_)

    dict_Jogadoras_Total_Jogos_black__,dict_Jogadoras_Total_Jogos_white__ =contar_win(dict_Jogadoras_Total_Jogos_black_),contar_win(dict_Jogadoras_Total_Jogos_white_)

    dicionarioTodasAsJogadoras = criar_dicionario_jogo(jogadorasWhite + jogadorasBlack) 

    for key,_ in dicionarioTodasAsJogadoras.items():
        dicionarioTodasAsJogadoras[key.lower()].append(construirDicionarFinal(key.lower(),dict_Jogadoras_Total_Jogos_white__,dict_Jogadoras_Total_Jogos_black__,dict_Jogadoras_WhiteWin__,dict_Jogadoras_BlackWin__))

    if type(command) == int:
        gerarGraficosVitorias(sorted(list(dicionarioTodasAsJogadoras.items()),key=lambda x: x[1], reverse= True)[:command])
    
    if type(command) == list:
        lista = []
        for nome in command:
            lista.append((nome.lower(),dicionarioTodasAsJogadoras[nome.lower()]))
        gerarGraficosVitorias(sorted(lista,key=lambda x: x[1][0], reverse= True))

#######################################################################################################################
###########################################--> FUNÇÃO SEGUINTE <--#####################################################

def criarDict(keys):
    """ crai dicionario

    Args:
        keys (str): chave

    Returns:
        dict: dicionario
    """
    dic = dict()
    for key in keys:
        dic[key] = []
    return dic
    
def valid(item,notation):
    """expressao valida

    Args:
        item (str): string
        notation (str): notacao do jogo

    Returns:
        bool: booleano
    """
    k = item.split()
    try:
        if k[1] == notation:
            if k[4] == "1...":
                return True
    except:
        return False

def get_jogadas(pgn):
    """obtem jogadas

    Args:
        pgn (str): string

    Returns:
        str: retorna jogada seguinte
    """
    count = 0
    for item in pgn.split():
        if bool(re.search(r'[A-Z]*[a-z]+[0-9]+[.]*',item)) == True or bool(re.search(r'O\-O',item))== True or bool(re.search(r'O\-O\-O',item)) == True:
            count +=1
        if count == 2:
            return item

def gerar_grafico_seguinte(TotaljogadasIniciais,principais5,notation):
    """Cria grafico

    Args:
        TotaljogadasIniciais (int): total de jogadas iniciais
        principais5 (lista): lista das n primeiras
        notation (str): notacao
    """

    abcissas = list(map(lambda x: x[0],principais5))
    ordenadas = list(map(lambda x: x[1]/TotaljogadasIniciais,principais5))
    x = np.arange(len(abcissas))
    ax = plt.axes()
    ax.bar(x,ordenadas)
    ax.set_xticks(x)
    ax.set_xticklabels(abcissas)
    plt.title('Jogadas mais prováveis depois de ' + notation)
    plt.xlabel('Jogadas')
    plt.ylabel('Probabilidade')
    plt.show()

def seguinte(nome_ficheiro,n=5,notation = 'e4'):
    """mostra grafico funcao seguinte

    Args:
        nome_ficheiro (str): nome ficheiro csv
        n (int, optional): n primeiras jogadas de acordo com o comando.
        notation (str, optional): notacao escolhida. Defaults to 'e4'.
    """
    ficheiro_csv = ler_csv_dicionario(nome_ficheiro)
    pgn = [key for key, _ in groupby(ficheiro_csv,lambda x: x['pgn'])]
    pgn_filtrado = list(filter(lambda x: valid(x,notation),pgn))
    total_respostas = list(map(lambda item: get_jogadas(item), pgn_filtrado ))
    total_ocorrencias = Counter(total_respostas).most_common()[:n]
    gerar_grafico_seguinte(len(total_respostas),total_ocorrencias,notation)

#######################################################################################################################
###########################################--> FUNÇÃO MATE <--#####################################################

def verificar_vitoria_color(dict,color):
    """Verifica vitoria de acordo com a cor

    Args:
        dict (dict): dicionario
        color (str): cor peça jogo

    Returns:
        bool: retorna bool se tiver win ou nao
    """
    return dict[color] == 'win' 


def verificar_xeque_color(dict,color,adversario):
    """verifica xeque mate

    Args:
        dict (dcit): dict jogo
        color (cor peça): cor peça result
        adversario (str): nome adversario

    Returns:
        str: nome adversario que ganhou por xeque
    """

    if dict[color] == 'checkmated':
        return dict[adversario]

def gerarGraficomate(jogadoras,wins_xequeMate):
    """cria grafico xeque mate

    Args:
        jogadoras (list): lista jogadoras
        wins_xequeMate (list): lista win xeque mate
    """

    labels = list(map(lambda x: x[0], jogadoras))
    grey = wins_xequeMate
    blue = list(map(lambda x: x[1], jogadoras))
    linhas = list(map(lambda x: (grey[x] * 100)/blue[x] /100  ,range(len(labels))))

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, grey, width, color='grey',label='jogos ganhos por xeque-mate')
    ax.bar(x + width/2, blue, width, color='blue',label='jogos ganhos')
    plt.legend()
    plt.ylabel('#Jogos')
    
    ax.twinx()
    plt.plot(x,linhas,color="red",label='percentagem de xaque-mate')
    plt.ylabel('Percentagem de xeque-mate',color="red")
    ax.set_xticks(x)
    ax.set_xticklabels(labels,rotation='vertical')

    fig.tight_layout()
    plt.title('Percentagem de xeque-mae,jogos ganhos, e jogos ganhos por xeque-mate')
    plt.legend(loc=6)
    
    plt.show()


def mate(nome_ficheiro, c = 5):
    """Mostra grafico xeque mate

    Args:
        nome_ficheiro (str): nome ficheiro csv
        c (int, optional): numero jogadoras a mostrar. Defaults to 5.
    """
    ficheiro_csv = ler_csv_dicionario(nome_ficheiro) 

    jogos_black_vitoria = list(filter(lambda x: verificar_vitoria_color(x,'black_result'), ficheiro_csv))
    jogos_white_vitoria = list(filter(lambda x: verificar_vitoria_color(x,'white_result'), ficheiro_csv))

    jogadores_black_xeque = list(map(lambda x: verificar_xeque_color(x,'white_result',"black_username"), jogos_black_vitoria))
    
    jogadores__white_xeque = list(map(lambda x: verificar_xeque_color(x,'black_result',"white_username"), jogos_white_vitoria)) 

    jogadores_black_win = list(map(lambda x: x["black_username"], jogos_black_vitoria))
    jogadores__white_win = list(map(lambda x: x["white_username"], jogos_white_vitoria)) 

    total_jogos_xeque = Counter(jogadores_black_xeque + jogadores__white_xeque)

    total_jogos_win = Counter(jogadores_black_win + jogadores__white_win).most_common()[:c]

    listaNumsWinXeque = list(map(lambda x: total_jogos_xeque[x[0]],total_jogos_win)) 

    gerarGraficomate(total_jogos_win,listaNumsWinXeque)
##########################################################################################################

def escrever_csv(nome_ficheiro, lista_dicionarios):
    """Escrever csv

    Args:
        nome_ficheiro (str): nome ficheiro de saida
        lista_dicionarios (list): lista de conteudo para escrever no ficheiro
    """
    cabecalhos = ['game_id','game_url','pgn','time_control','end_time','rated','time_class','rules','wgm_username','white_username','white_rating','white_result','black_username','black_rating','black_result']
    with open(nome_ficheiro,'w',encoding="UTF-8",newline='') as ficheiro_csv:
        escritor = csv.DictWriter(ficheiro_csv,fieldnames=cabecalhos,delimiter=',')
        escritor.writeheader()
        for linha in lista_dicionarios:
            escritor.writerow(linha)

def filtrar(word,r): 
    """filtrar

    Args:
        word (str): palavra
        r (str): expressao regular

    Returns:
        bool: boolenao
    """

    if bool(re.search(r,word)) == True:
        return True
    return False

def extrair(ficheiro_entrada,ficheiro_saida='out.csv',r='.*',coluna='wgm_username'):
    """extrair, criar conteudo um novo ficheiro

    Args:
        ficheiro_entrada (str): ficheiro csv
        ficheiro_saida (str, optional): nome do ficheiro csv a criar. Defaults to 'out.csv'.
        r (str, optional): [description]. expressão regular Defaults to '^a'.
        coluna (str, optional): [description]. coluna a escolher Defaults to 'wgm_username'.
    """

    ficheiro_csv = ler_csv_dicionario(ficheiro_entrada)

    ficheiro_filtrado = list(filter(lambda x: filtrar(x[coluna],r),ficheiro_csv))

    escrever_csv(ficheiro_saida, ficheiro_filtrado)

import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("ficheiro_csv", help="O ficheiro csv para ser lido")
    parser.add_argument("comando", help="Comandos: anos, classes, vitorias, seguinte, mate, extrair")
    parser.add_argument('-c', nargs=1, default= None, type=int, required= False, help='Permite escolher um número')
    parser.add_argument('-u', nargs='+', default= None,type=str, required= False, help='Permite escolher jogadora')
    parser.add_argument('-j', nargs=1, default= None,type=str, required= False, help='Escolhe jogada')
    parser.add_argument('-o', nargs='?', default= 'out.csv',type=str, required= False, help='Nome do ficheiro a criar')
    parser.add_argument('-r', nargs='?', default= '^a',type=str, required= False, help='Expressão regular a considerar')
    parser.add_argument('-d', nargs='?', default= 'wgm_username',type=str, required= False, help='Coluna a considerar')
    argument = parser.parse_args()
    lista = sys.argv

    if argument.comando == 'anos':
        if len(lista) == 3:
            anos(argument.ficheiro_csv)
        else:
            print('Erro no comando, digite novamente')
    
    if argument.comando == 'classes':
        if len(lista) == 3:
            classes(argument.ficheiro_csv,5)
        elif '-c' in lista:
            argument.c = argument.c[0]
            classes(argument.ficheiro_csv,argument.c)
        else:
            print('Erro no comando, digite novamente')
    
    if argument.comando == 'vitorias':
        if ('-c' in lista and '-u' not in lista):
            argument.c = argument.c[0]
            vitorias(argument.ficheiro_csv,argument.c)

        elif ('-u' in lista and '-c' not in lista):
            vitorias(argument.ficheiro_csv,argument.u)      
        
        elif len(lista) == 3:
             vitorias(argument.ficheiro_csv,5)
        
        else:
            print('Erro no comando, digite novamente')

    if argument.comando == 'seguinte':
        if len(lista) == 3:
             seguinte(argument.ficheiro_csv)

        elif ('-j' in lista and '-c' in lista):
            argument.j = argument.j[0]
            argument.c = argument.c[0]
            seguinte(argument.ficheiro_csv,argument.c,argument.j)
        
        elif ('-j' not in lista and '-c' in lista):
            argument.c = argument.c[0]
            seguinte(argument.ficheiro_csv,argument.c)

        elif ('-j' in lista and '-c' not in lista):
            argument.j = argument.j[0]
            seguinte(argument.ficheiro_csv,5,argument.j)
        
        else:
            print('Erro no comando, digite novamente')

    if argument.comando == 'mate':
        if len(lista) == 3:
            mate(argument.ficheiro_csv)
        elif '-c' in lista:
            argument.c = argument.c[0]
            mate(argument.ficheiro_csv,argument.c)
        else:
            print('Erro no comando, digite novamente')

    if argument.comando == 'extrair':
        if len(lista) == 3:
             extrair(argument.ficheiro_csv)
        
        else:
            flag = False
            invalidos = ['-c','-u','-j']
            for item in lista:
                if item in invalidos:
                    print('Erro no comando, digite novamente')
                    flag = True
                    break
            if flag != True:
                extrair(argument.ficheiro_csv,argument.o,argument.r,argument.d)
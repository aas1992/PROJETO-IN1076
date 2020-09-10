# Imports
import time
import numpy as np
import pandas as pd
import math
import random 
import matplotlib.pyplot as plt

# Parâmetros de Entrada
p = 100                  # Tamanho da População 
n = len(cidades)        # Quantidade de genes em cada cromossomo/número de cidades
pe = 0.3                # Porcentagem de indivíduos Elite
pm = 0.2                # Porcentagem de indivíduos gerados na mutação
taxaHerancaElite = 0.7  # Taxa de um descendente herdar o alelo do pai Elite
N_geracoes = 100         # Número máximo de gerações

# Gerar a População Inicial de forma aleatória
def gerarPopulacao():
    populacao=[]
    for i in range(p):
        individuo=[]
        for j in range(n):
            individuo.append(random.random())
        populacao.append(individuo)
    return populacao

# O Decoder é responsável por decodificar os valores dos genes em uma sequência de cidades para um percurso
def decoder(populacao):
    decodificador=[]                # Dicionario rotulado mapeando a cidade e seu valor aleatorio correpondente gerado para cada indivíduo
    rotas=[]                        # Receberá todas as rotas viáveis
    cromossomos_Ordenados=[]        # Receberá todos os cromossomos dos indivíduos

    for i in range(len(populacao)):
        individuo={}
        for j in range(n):
            individuo[j]=populacao[i][j]
        decodificador.append(individuo)
   
    for ind in decodificador:
        rota=[]                   # Para cada rota individual
        cromossomo=[]             # Recebe o vetor de cromossomos de cada individuo
        for item in sorted(ind, key=ind.get):
            rota.append(item)
            cromossomo.append(ind[item])
        rota.append(rota[0])
        rotas.append(rota) 
        cromossomos_Ordenados.append(cromossomo)

    return (rotas, cromossomos_Ordenados)   # Retorna todas as rotas e todos os cromossomos

# Determinar a distância Euclidiana entre a cidade i e a cidade j
def distancia(cidade1, cidade2):
  X_a, Y_a = cidades[cidade1]
  X_b, Y_b = cidades[cidade2]
  dist = math.sqrt((X_b-X_a)**2 + (Y_b-Y_a)**2)
  return dist

# Função Objetivo: Calcula a distância total de percorrer todas as cidades
def funcaoObjetivo(rota):
  dist_total = 0
  for i in range(0, len(rota)-1):
    cid1 = rota[i]
    cid2 = rota[i+1]
    dist_total = dist_total + distancia(cid1, cid2)
  return dist_total

# Calcula a aptidão de cada indivíduo
def fitness(rotas):
    lista_fitness=[]
    for rot in rotas:
        lista_fitness.append(funcaoObjetivo(rot))
    return lista_fitness

# Classifica a população como Elite e Não Elite
def classificarPopulacao(populacaoAtual, fitness):
    dictPopFit = {}
    dictPop = {}
    popAtual = []

    for i in range(len(fitness)):
        dictPop[i]=fitness[i]
    
    for item in sorted(dictPop, key=dictPop.get):
            dictPopFit[item]=dictPop[item]
    for chaves in dictPopFit:
        popAtual.append(populacaoAtual[chaves])

    popElite=[]
    for i in range(0, (int(pe*len(popAtual)))):
        popElite.append(popAtual[i])
    #print('Elite: ', popElite)

    popNElite=[] 
    for i in range((int(pe*len(popAtual))), len(popAtual)):
        popNElite.append(popAtual[i])
    #print('NElite: ', popNElite)
    
    return (popElite, popNElite)

def popMutante(pm):
    popMutante=[]
    for i in range(0, int(pm*p)):
        individuo=[]
        for j in range(n):
            individuo.append(random.random())
        popMutante.append(individuo)
    #print('Mutantes: ', popMutante)
    return popMutante

# Determinar o cruzamento de um indivíduo Elite e um indivíduo Não Elite
def crossover(taxaRestantePop, parent1, parent2):
    descendente = []                # Lista para adicionar os descendentes gerados
    chaveAleatoria = []             # Vetor de chave aleatória que irá receber números reais entre 0 e 1
    for j in range(0, len(parent1)):
        chaveAleatoria.append(random.random())   # A chave aleatória adiciona aleatoriamente um valor real entre 0 e 1

    for indice in range(0, len(parent1)):
        if chaveAleatoria[indice] <= taxaHerancaElite:  # Se o valor da chave for menor do que a taxa de herança, então:
            descendente.append(parent1[indice])      # O descendente recebe o alelo do pai 1 (Elite)
           
        else:   # Se o valor da chave for maior do que a taxa de herança, então:
            descendente.append(parent2[indice])      # O descendente recebe o alelo do pai 2 (Não Elite)
    return descendente

# Gerar Próxima População a partir dos indivíduos Elite, acasalamento e Mutante
def novaGeracao(popElite, popNElite, popMutantes):
    novaPopulacao = []
    
    # Elite
    for i in popElite:
        novaPopulacao.append(i)

    # Cruzamento
    taxaRestantePop = p-(pe*p)-(pm*p)    # TaxaRestantePop recebe o número de indivíduos que ainda faltam para completar a população

    for i in range(0, int(taxaRestantePop)):
        parent1=random.choice(popElite)   # O parent 1 é escolhido aleatoriamente do conjunto Elite
        parent2=random.choice(popNElite)  # O parent 2 é escolhido aleatoriamente do conjunto Não Elite
        if (len(parent1)==len(parent1)):  # Verifica se o parent 1 tem o mesmo tamanho do parent 2 para o crossover
            novaPopulacao.append(crossover(taxaRestantePop, parent1, parent2)) # Realiza o crossover e adiciona o descendente na Nova População
    
    # pm Mutantes são adicionados à nova população
    for i in popMutantes:
        novaPopulacao.append(i)

    return novaPopulacao

# Algoritmo BRKGA
def BRKGA():
    melhorFitness = []
    populacaoInicial = gerarPopulacao()
    rotas,ordemPopulacao = decoder(populacaoInicial)
    list_fitness = fitness(rotas)
    
    for i in range(1, N_geracoes):
        #print('Geração: ', i)
        popElite, popNElite = classificarPopulacao(ordemPopulacao, list_fitness)        
        popMutantes = popMutante(pm)
        novaPopulacao = novaGeracao(popElite, popNElite, popMutantes)
        rotas, ordemPopulacao = decoder(novaPopulacao)
        list_fitness = fitness(rotas)
        L = np.argmin(list_fitness)
        melhorFitness.append(list_fitness[L])
        melhorRota = rotas[L]

    print(melhorFitness)
    print(melhorRota)

BRKGA()


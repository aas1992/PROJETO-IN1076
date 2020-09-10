# Imports
import time
import numpy as np
import pandas as pd
import math
import random 
import matplotlib.pyplot as plt

i25 = pd.read_csv(os.path.join(dir_remoto,'Projeto - Algortimos/data/Instancia_25.csv'),  sep = ";" )
i35 = pd.read_csv(os.path.join(dir_remoto,'Projeto - Algortimos/data/Instancia_35.csv'),  sep = ";" )
i50 = pd.read_csv(os.path.join(dir_remoto,'Projeto - Algortimos/data/Instancia_50.csv'),  sep = ";" )
i100 = pd.read_csv(os.path.join(dir_remoto,'Projeto - Algortimos/data/Instancia_100.csv'),  sep = ";" )


i25 = i25.to_numpy()
i35 = i35.to_numpy()
i50 = i50.to_numpy()
i100 = i100.to_numpy()


print(i25.shape)
print(i35.shape)
print(i50.shape)
print(i100.shape)


def dicionario(dados):
  dicio = {}
  for i in range(len(dados)):
    dicio[dados[i][0]] = (dados[i][1], dados[i][2])
  return dicio

# Rodar um de cada vez no BRKGA
cidades = dicionario(i25)
cidades = dicionario(i35)
cidades = dicionario(i50)
cidades = dicionario(i100)

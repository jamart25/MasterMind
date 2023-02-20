# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 17:49:36 2022

@author: Nanoi O-Yama
"""

import random

"""
Primero diseño el juego para jugar como codebreaker.

Se jugará con 6 colores y 4 pegs. La máquina generará una combinación aleatoria de 4 colores
(Rojo = 0, Naranja = 1, Amarillo = 2, Verde = 3, Azul = 4 y Blanco = 5) y el codebreaker tendrá 
que adivinar dicha combinación.

El codemaker por cada prediccion que haga el codebreaker asignará '=' si ha acertado COLOR y 
POSICIÓN y '+' si ha acertado COLOR pero NO POSICIÓN.
"""

#Paso 1. Obtengo el cojunto de todas las combinaciones posibles
S = []
allPosibilities = []
for i in {0, 1, 2, 3, 4, 5}:
    for j in {0, 1, 2, 3, 4, 5}:
        for k in {0, 1, 2, 3, 4, 5}:
            for p in {0, 1, 2, 3, 4, 5}:
                S.append([i, j, k, p])
                allPosibilities.append([i, j, k, p])
                
allPegs = []
for i in range(5):
    for j in range(5):
        if i + j <= 4:
            allPegs.append((i, j))


def masterMind():
    
    
    colors = {0, 1, 2, 3, 4, 5}
    avaliablePositions = [{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}]
    
    code = [0, 0, 0, 0]
    codeHip = [0, 1, 2, 3] 
    cont = 0
    
    for i in range(4):
        code[i] = random.randint(0, 5)

    
    #Se ha generado la lista aleatoria, ahora empieza el juego
   
    #El juego no acaba hasta que las cadenas coinciden
    
    while not(code == codeHip): 
        
        #La primera predicción del codeBreaker siempre será la misma
        if not (cont==0):   
            codeHip = codeBreaker(codeHip, pegs, colors, avaliablePositions)
            
        pegs = ['...', '...', '...', '...']  #Elijo poner "..." porque es más visual
        
        #Ahora se comparan las cadenas 
        
        for i in range(4):
            if code[i] == codeHip[i]:
                pegs[i] = '='
            else:
                for j in range(4):
                    if code[i] == codeHip[j] and not(pegs[j] == '=') and not(j == i):
                        pegs[j] = '+'
                    else:
                        pass
        #Recojo la predicción del codebreaker 
        print(codeHip, pegs)
        cont = cont + 1
    
    return code, codeHip, pegs


#Función que recoge la predicción del codebreaker
    
def prediccion():
    
    print("Ingrese su hipótesis")
    
    codeHip = [0, 0, 0, 0]
    
    for i in range(4):
        codeHip[i] = int(input())
        
    return codeHip
   


#Esta es la función que en base a la información que le llega planea la siguiente predicción
def codeBreaker(codeHip, pegs, colors, avaliablePositions):
    
    nextCodeHip = [6, 6, 6, 6]
    colorsUsed = set()
    
    #nos interesa que este a parte, para evitar que posiciones con '+' o '=' cojan un color descartado
    for i in range(4):
        if pegs[i] == '...':
            colors.discard(codeHip[i])
            avaliablePositions[codeHip[i]] = set()
    
    for i in range(4):
        
        if pegs[i] == '...':
            nextCodeHip[i] = random.choice(tuple(colors))
            while i not in avaliablePositions[nextCodeHip[i]]:
                if (nextCodeHip[i] in colorsUsed) and not(colors-colorsUsed == set()):
                    nextCodeHip[i] = random.choice(tuple(colors-colorsUsed))
                else:
                    nextCodeHip[i] = random.choice(tuple(colors))    
                     
            colorsUsed.add(nextCodeHip[i])
                
        if pegs[i] == '=':
            nextCodeHip[i] = codeHip[i]
            for j in range(6):
                avaliablePositions[j].discard(i)
        elif pegs[i] == '+':
            avaliablePositions[codeHip[i]].discard(i)
            
            aux = random.choice(tuple(colors))
            while i not in avaliablePositions[aux]:
                if (aux in colorsUsed) and not(colors-colorsUsed == set()):
                    aux = random.choice(tuple(colors-colorsUsed))
                else:
                    aux = random.choice(tuple(colors))
            
            nextCodeHip[i] = aux
            colorsUsed.add(aux)
            
            
    return nextCodeHip;


def knuth():
    
    code = [0, 0 , 0, 0]
    codeHip = [1, 1, 2, 2] #Paso 2. Empezamos con la predicción inicial
    score = []; #guarda las puntuaciones del algoritmo para cada prediccion
    listMinScore = []
    minMaxScore = 0
    setMinMax = set()
    
    
    for i in range(4):
        code[i] = random.randint(0, 5)
    
    #Paso 3. Probamos la predicción inicial para obtener una respuesta.
    while True: 
                    
        pegs = getPegs(codeHip, code)
        print(codeHip, pegs)
        
        if pegs == (4, 0): #Paso 4. Si se ha adivinado la cadena, hemos acabado
            return codeHip, pegs
        else: #Paso 5. En caso contrario se elimina de S cualquier respuesta que de como resultado unos pegs distintos
            for j in S:
                if not(getPegs(j, codeHip) == pegs):
                    S.remove(j)
                else:
                    pass
                
        #Paso 6. Aplicar la técnica del minimax
        #Tenemos en cuenta cada código que NO SE HAYA USADO de los 1296 posibles
        allPosibilities.remove(codeHip) 
        #Para cada una de las posibilidades no usadas anteriormente, calculamos cuantas se eliminarían
        #para cada conjunto de pegs posible
        listMaxScore = []
        
        for i in allPosibilities:
            listMinScore = []
            for j in allPegs:
                score = []
                for p in allPosibilities: #a bote pronto esto es sobre el conjunto S
                    cont = 0
                    if not(p == i):
                        if not(getPegs(i, p) == j):
                            cont = cont + 1
                        else:
                            pass
                    score.append(cont)
                minScore = min(score)
                listMinScore.append(minScore)
            maxScore = max(listMinScore)
            listMaxScore.append(maxScore)
        minMaxScore = min(set(listMaxScore))
        
        
        """
        |(B, W)|  [0, 1, 2, 2]   |  ...   listMinScore es la lista de todos los min(score)
        |      |                 |  ...
        |      |                 |  ...
        |(2, 2)|   min(score)    |  ...
        |      |                 |  ...
        ---------------------------------
   max  |      |max(listMinScore)|  ...  -> listMaxScore
   
        ...y de todos los max(listMinScore) escojo el valor más pequeño minMaxScore
        
        """
        for i in range(len(listMaxScore)):
            if listMaxScore[i] == minMaxScore:
                setMinMax.add(tuple(allPosibilities[i]))
            else:
                pass
        
        Saux = set()
        for i in S:
            Saux.add(tuple(i))

        #elegimos la próxima predicción
        if not(setMinMax & Saux == set()):
            codeHip = list(min(setMinMax & Saux))
        else:
            codeHip = list(min(setMinMax))
        
        #pegs = getPegs(codeHip, code)
        #print(codeHip, pegs)
            
    return codeHip, pegs


#Esta funcion me proporciona la combinacion de pegs al comparar dos combinaciones
def getPegs(codeHip, code):
    
    black = 0
    white = 0
    
    for i in range(4):
            if code[i] == codeHip[i]:
                black = black + 1
            else:
                for j in range(4):
                    if code[i] == codeHip[j] and not(code[j] == codeHip[j]) and not(j == i):
                        white = white + 1
                    else:
                        pass
                    
            
    return (black, white)


def haz():
    for i in range(1000):
        print('\n Bienvenido: \n')
        try:
            masterMind()
        except:
            print("Hubo error :(")
    return 'Victoria'




"""    
def codeBreaker(codeHip, pegs, colors, avaliablePositions):
    
    nextCodeHip = [1, 1, 1, 1]
    positions = {0, 1, 2, 3}
    trash = set()
    
    for i in range(4):
        if pegs[i] == '...':
            trash.add(codeHip[i])
    
    for i in trash:
        colors.remove(i)
            
    for i in range(4):
        if pegs[i] == '...':
            nextCodeHip[i] = random.choice(tuple(colors))
            positions.remove(i)
                
        elif pegs[i] == '=':
            nextCodeHip[i] = codeHip[i]
            for j in range(len(avaliablePositions)):
                avaliablePositions[j].discard(i)
    
    for i in range(4):
        if pegs[i] == '+':
            colors.remove(codeHip[i])
            nextCodeHip[i] = random.choice(tuple(colors))
            avaliablePositions[codeHip[i]].remove(i)
            
            while True:
                try:
                    aux = random.choice(tuple(avaliablePositions[codeHip[i]]&positions))
                    aux = random.choice(tuple(avaliablePositions[codeHip[i]]&positions))
                    break
                except IndexError:
                    pass
                except NameError:
                    pass
                    
            nextCodeHip[aux] = codeHip[i]
            positions.remove(aux)
            colors.add(codeHip[i])
            
    return nextCodeHip
"""        
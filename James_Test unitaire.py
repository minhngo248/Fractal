# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:51:18 2021

@author: james
"""
from re import *
import os

def extraire_fichier(forme):
    L = []
    #os.chdir("James-prog-final") # pour aller à ce répertoire
    for i in os.listdir():
        if forme in i:
            L.append(i)
    return L

def test_unitaire(name):
    consigne = open(str(name),"r")
    grammar = [line.rstrip() for line in consigne.readlines()]
    regles=[]
    j = 0
    for i in range(len(grammar)):
        if search(r"axiome[\s]+=[\s]+['\"][a-zA-Z-+*\[\]<>$&]+['\"]", grammar[i]) or search(r"angle[\s]+=[\s]+[0-9]+(?:.[0-9]+)?", grammar[i]) or search(r"taille[\s]+=[\s]+[0-9]+(?:.[0-9]+)?", grammar[i]) or search(r"niveau[\s]+=[\s]+[0-9]+", grammar[i]) or search(r"regles[\s]+=", grammar[i]) or search(r"['\"][a-zA-Z]=[a-zA-Z-+*\[\]<>$&]+['\"]", grammar[i]):
            j += 1
    #print(j)
    if j == len(grammar):
        return True
    else:
        return False
    consigne.close()

def traitementfichier_(name):
    consigne = open(str(name),"r")
    grammar = [line.rstrip() for line in consigne.readlines()]
    regles=[]
    for i in range(len(grammar)):
        if 'axiome' in grammar[i]:
            axiome = (findall(r"['\"][a-zA-Z-+*\[\]<>$&]+['\"]", grammar[i]))          
            #print(axiome)
            axiome = axiome[0].replace('"','')
            #print(axiome)
        elif 'angle' in grammar[i]: 
            angle = float(findall(r"[0-9]+(?:.[0-9]+)?", grammar[i])[0])
        elif 'taille' in grammar[i]:
            taille= float(findall(r"[0-9]+(?:.[0-9]+)?", grammar[i])[0])
        elif 'niveau' in grammar[i]:         
            niveau= int(findall(r"[0-9]+", grammar[i])[0])
        elif 'regles' in grammar[i]:
            for j in range(i+1,len(grammar)):
                if 'axiome'in grammar[j] or 'angle'in grammar[j] or'niveau'in grammar[j] or 'taille' in grammar[j]:
                    break
                elif '=' not in grammar[j]: #vérifie le format de la règle  : ex : a=aabaaa...
                    input("Mauvais format de règles.\nArrêt du programme, appuyez sur entrée pour fermer")
                    exit()
                #print(grammar[j])
                rule = (findall(r"=[a-zA-Z-+*\[\]<>$&]+['\"]", grammar[j]))
                rule = [rule[0].replace('"','')]
                #print(rule)
                rule = rule[0].replace('=','')
                #print(rule)
                regles.append(rule)  
    consigne.close()
    return (axiome,regles,angle,taille,niveau)

def axiomereplace2_(tupcon):
    (ouvert,ferme)=(0,0)
    if tupcon[4] == 0:     
        return tupcon
    else :
        axiome = str(tupcon[0])
        regles = tupcon[1]
        for e in regles:
            axiome = axiome.replace(str(e[0]), str(e[2:])) #remplace a dans axiome par ce qu'il y a après le = de la règle
        for e in axiome:
            if e=='[' : 
                ouvert+=1
            elif e==']':
                ferme+=1
            if ferme>ouvert:
                input("Le fichier décharge trop de fois la liste de positions.\nArrêt du programme, appuyez sur entrée pour fermer")
                exit()           
        return axiomereplace2_((axiome,regles,tupcon[2],tupcon[3],tupcon[4]-1))
    
fichier = ''
Ltxt = extraire_fichier(".txt")
print("Voici la liste des L-systeme dans le repertoire: \n",Ltxt)
# Le fichier d’entrée sera demander explicitement dès le début de votre programme.
print("------------------------------------------------------------------------------")
fichier = input("Veuillez ecrire correctement le nom du fichier d'entree format txt': ")
test = test_unitaire(fichier)
if test == True: # Consigne respecté: Pour tout fichier d’entrée incorrect, votre programme doit s’arrêter et indiquer la raison de l’arrêt.
    tup = traitementfichier_(fichier)
    tup = axiomereplace2_(tup)
    print("Ce fichier d'entrée (consigne) est de bon format!")
    print(tup)
else:
    print("Ce fichier d'entrée (consigne) n'est pas de bon format! Arrêt immédiat")
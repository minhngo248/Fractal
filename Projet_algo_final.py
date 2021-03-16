# -*- coding: utf-8 -*-
"""
Programmation pour le projet python année 2020/2021
NGO Ngoc Minh, NGUYEN-CAO James-Quoc-Thai, TACHI NGOUFFO Ivannie Roxanne, COUCHOUD Matteo
CPI2 Groupe 4
"""

from turtle import *
from re import *
import os

def traitementfichier_(name):
    consigne = open(str(name)+'.txt',"r")
    grammar = [line.rstrip() for line in consigne.readlines()]
    regles=[]
    for i in range(len(grammar)):
        if 'axiome' in grammar[i]:
            axiome = str(findall(r"['\"][a-zA-Z\-\+\*\[\]\<\>\}\&\#{]+['\"]", grammar[i])[0].replace('"',''))
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
                regles.append(grammar[j])
    regles = [k[1:len(k)-1]for k in regles]
    consigne.close()    
    return (axiome,regles,angle,taille,niveau) # Retourne un tuple

def traitementTest_(name):
    if not os.path.isfile(str(name) +'.txt'): #Si pas dans le répertoire : erreur
        input("Le fichier spécifié n'existe pas dans le répertoire.\nArrêt du programme, appuyez sur entrée pour fermer.")
        exit()
    consigne = open(str(name)+".txt","r")
    grammar = [line.rstrip() for line in consigne.readlines()]
    countn=0
    for lin in grammar: # compte dans chaque ligne la présence d'un élément nécessaire noté au format demandé. Si ligne vide en plus alors pas d'erreur car pas comptée.  
        if (search(r"axiome[\s]+=[\s]+['\"][a-zA-Z\-\+\*\[\]\<\>\}\&\#{]+['\"]", lin) or search(r"angle[\s]+=[\s]+[0-9]+(?:.[0-9]+)?", lin) 
            or search(r"taille[\s]+=[\s]+[0-9]+(?:.[0-9]+)?", lin) or search(r"niveau[\s]+=[\s]+[0-9]+", lin) or search(r"regles[\s]+=", lin) 
            or search(r"['\"][a-zA-Z]=[a-zA-Z\-\+\*\[\]<\>\}\&\#\{]+['\"]", lin)):
            countn +=1
        if 'axiome' in lin: #On vérifie le nombre d'axiomes. Plus d'un axiome => mauvais format
            axiome = list(filter(str.strip, findall(r"['\"][a-zA-Z\-\+\*\[\]\<\>\}\&\#{]+['\"]", lin)))
        if 'niveau' in lin: #On vérifie si niveau est un entier ie si il y a un '.' dans la ligne
            if'.' in lin :
               input("Mauvais format de fichier : le niveau doit être un entier.\nArrêt du programme, appuyez sur entrée pour fermer.")
               return False
    if  countn >= 6  and len(axiome)==1: # On a un maximum de 2 règles dans le cadre du projet, donc on a entre 6 et 7 éléments.
        return True
    else: # Il manque un ou des éléments nécéssaires ou il y a une erreur de format d'écriture (mauvais symbole, plus d'un axiome, un espace manquant)
        if len(axiome)>1:
            input("Mauvais format de fichier : plus d'un axiome.\nArrêt du programme, appuyez sur entrée pour fermer.")
        else:
            input("Il manque un élément nécessaire de la consigne ou un élément n'est pas défini avec le bon format.\nArrêt du programme, appuyez sur entrée pour fermer.")
        return False #il y a une erreur, on stope le programme
    consigne.close()


def axiomereplace2_(tupcon): 
    if tupcon[4] == 0:     
        return tupcon
    else :
        axiome = str(tupcon[0])
        regles = tupcon[1]
        for e in regles:
            axiome = axiome.replace(str(e[0]), str(e[2:])) #remplace a dans axiome par ce qu'il y a après le = de la règle
        return axiomereplace2_((axiome,regles,tupcon[2],tupcon[3],tupcon[4]-1))
    
def dechargementtest_(tuplereplace):
    (ouvert,ferme)=(0,0)
    axiome = tuplereplace[0]
    for e in axiome:
            if e=='[' : 
                ouvert+=1
            elif e==']':
                    ferme+=1
            #On décharge trop la liste de position, on appelle donc dans une liste vide => risque d'erreur
            if ferme>ouvert: 
                input("Le fichier décharge trop de fois la liste de positions.\nArrêt du programme, appuyez sur entrée pour fermer")
                exit()
            else : 
                return tuplereplace

def ecriturefichier_(tupleinput,position):
    axiome = tupleinput[0]
    newaxiome = '%µ£$'+axiome+'ù'
    angle = tupleinput[2]
    taille = tupleinput[3]
    fichier = open("resultat.py","w")   
    dico = {"a":"pd();forward("+str(taille)+");", "b":"pu();forward("+str(taille)+");",
            "-":"left("+str(angle)+");", "+":"right("+str(angle)+");","[":"position.append(pos());rangle.append(heading());",
            "]":"pu();goto(position.pop(len(position)-1));setheading(rangle.pop(len(rangle)-1))","*":"right(180);","<":"pensize(pensize()*2);", 
            ">":"pensize(pensize()/2);","#":"pencolor('blue');","}":"pencolor('red');","&":"pencolor('black');",
            "{":"pencolor('green');","%":"from turtle import*","µ":"speed('fastest');","£":"color('black');","$":"position = [];rangle = []","ù":"exitonclick();"}
    for e in newaxiome:
        for clef, valeur in dico.items():
            if e == clef:
                fichier.write(valeur+"\n")
                print(valeur)
    fichier.close()

# exécution des fonctions
entree = str(input("Entrez le nom du fichier-consigne sans l'extension : "))
testb =traitementTest_(entree)
if testb == True:
    tuptrait = traitementfichier_(entree)
    tupcon = axiomereplace2_(tuptrait)
    tupcon = dechargementtest_(tupcon)
    ecriturefichier_(tupcon,(0,0))
    exec(open("resultat.py").read())
    input("")
elif testb == False:
    exit()
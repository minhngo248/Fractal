from turtle import *
import os
from re import *

def lire_fichier(nomFich):
    if not os.path.isfile(nomFich):
        print("Le fichier " + nomFich + " n'existe pas")
        return None
    f = open(nomFich,"r")
    regles = []
    l = f.readlines()
    for i in range(len(l)):
        if 'axiome' in l[i]:
            axiome = findall(r"['\"][a\-\+\*\[\]b]+['\"]",l[i])
            axiome = axiome[0].replace('"','')
        elif 'angle' in l[i]:
            angle = float(findall(r"[0-9]+(?:.[0-9]+)?",l[i])[0])
        elif 'taille' in l[i]:
            taille = float(findall(r"[0-9]+(?:.[0-9]+)?",l[i])[0])
        elif 'niveau' in l[i]:
            niveau = int(findall(r"[0-9]+",l[i])[0])
        elif 'regles' in l[i]:
            for j in range(i+1,len(l)):
                if ('axiome' in l[j] or 'angle' in l[j] or 'niveau' in l[j] or 'taille' in l[j]):
                    break
                regles.append(l[j])
    regles = [k[1:len(k)-2] for k in regles]
    f.close()
    return (axiome,regles,angle,taille,niveau)

def tupSuc(tup):
    if tup[4] == 0:
        return tup
    else:
        axiome = tup[0]
        regles = tup[1]
        for i in range(len(regles)):
            axiome = axiome.replace(regles[i][0], regles[i][2:])
        return tupSuc((axiome, regles, tup[2], tup[3], tup[4]-1))  

def FichierSortie(tup):
    f = open("code_flocon.py","w")
    f.write("from turtle import *\n")
    for i in tup[0]:
        if i == 'a':
            f.write("pd()\nforward(%f)\n" %(tup[3]))
        elif i == 'b':
            f.write("pu()\nforward(%f)\n" %(tup[3]))
        elif i == '+':
            f.write("right(%f)\n" %(tup[2]))
        elif i == '-':
            f.write("left(%f)\n" %(tup[2]))   
        elif i == '*':
            f.write("right(180)\n")
        elif i == ']':
            f.write("A = pos()\n")
        elif i == '[':
            f.write("goto(A)\n")
    f.write("exitonclick()")
    f.close()  

def afficherCommandes():
    f = open("code_flocon.py","r")
    l = f.readlines()
    for i in l:
        print(i)       

def Draw(tup):
    A = []
    speed("fastest")
    for i in tup[0]:
        if i == 'a':
            pd()
            forward(tup[3]) #tup[3] = taille
        elif i == 'b':
            pu()
            forward(tup[3])
        elif i == '+':
            right(tup[2]) #tup[2] = angle
        elif i == '-':
            left(tup[2])
        elif i == '*':
            right(180)
        elif i == '[':
            A.append(pos())
        elif i == ']':
            goto(A[len(A)-1])
    print(len(A))

s = str(input("Entrez le nom du fichier: "))
tup = lire_fichier(s)
tup = tupSuc(tup)
print(tup)
#FichierSortie(tup)
#afficherCommandes()
Draw(tup)
exitonclick()
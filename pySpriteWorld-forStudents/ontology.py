import numpy as np
import csv
import sys
#import cytoolz # pip install cytoolz
from collections import defaultdict
import os
import itertools

noms_d_affreux = """
Nuzak,Lystis, Mefeero, Sazai, Ross, Azok,
Bron, Turok, Garaddon, Hruon, Jeddek,
Grom, Thrum, Drog, Gorrum, Harg, Thrug, Karg,
Roberick, Magan, Danforth, Lansire,
Merander, Gyram, Darrick, Herby,
Grobnick, Kazbo,
Ceres,Demeter,Fichtelite,Haniyas,Jarn,Lando,Laterite,
Maa,Madd,Mu,Nog,Reki,Topo,Uralite,Ziemia,
Cyprian,Danorum,Logia,Malleus,Neaniskos,Papyri,Utpala
"""


class Ontology:

    def __init__(self,pairs=True,filename='tiny_spritesheet_ontology.csv'):
        self.onto = self.construit_ontologie(pairs,filename)
        self.cate = self.construit_categories()

    def names(self,sprt):
        if sprt is None:
            return None
        try:
            # si le sprite a un nom en propre, le renvoyer
            return [sprt.nom]
        except AttributeError:
            if sprt.tileid in self.onto:
                return self.onto[sprt.tileid]
            else:
                return ['']
                #raise "erreur.. le sprite n'a pas de nom"

    def firstname(self,sprt):
        return None if sprt==None else self.names(sprt)[0]

    def secondname(self,sprt):
        return None if sprt==None else self.names(sprt)[1]

    @staticmethod
    def construit_ontologie(pairs,filename):
        '''
            Construit un dictionnaire (de type cles=pairs d entier ou juste entier, valeur=ensemble de strings)
            Ce dictionnaire decrit ce qu'il y a dans les tiles, en reprenant l information d un fichier csv

            Par exemple :

            si pairs = True, on a         ontology[(15,1)] = {'blob'}
            si pairs = False,on aurait    ontology[ 241 ]  = {'blob'}

            Car a la ligne 15, colonne 1 (qui est la 241 case) dans l'image data/tiny-Complete-Spritesheet-32x32.png, il y a un blob
            L'indexation commence a partir de 0.

            Si un tile est decrit par plusieurs elements e1,e2,e3  alors on rajoute a la fin l element e1-e2-e3
            Ainsi, ontology[(15,12)] = {'araignee', 'mort','araignee-mort'}
        '''

        dirname = os.path.dirname(os.path.abspath(__file__))

        ontology = {}
        f = open(dirname + "/" + filename, 'r')
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            for j,s in enumerate(row):
                l = s.lower().split(' ')
                summary = '-'.join(l)
                if summary not in l:
                    l.append(summary)
                ontology[(i,j) if pairs else i*len(row)+j] = l
        f.close()

        # les guerriers sont de la case (16,6) jusqu'a (21,12)
        noms_guerriers = [st.strip() for st in noms_d_affreux.split(',')]
        idx_nom = itertools.count()
        for i in range(16,22):
            for j in range(6,13):
                ontology[(i,j)] = [noms_guerriers[ next(idx_nom) ],'guerrier']

        return ontology




    def construit_categories(self):
        '''
            cree un dictionnaire (key=categorie, valeur=ensemble d indexs)
            par exemple, on a:
            >>> c["salade"]
            set([(10, 11)])
            >>> c["citrouille"]
            set([(10, 12)])
            >>> c["epinards"]
            set([(2, 8)])
        '''
        cat = defaultdict(set)

        for idx,descr in self.onto.items():
            for nom in descr:
                cat[nom].add( idx )
        return cat

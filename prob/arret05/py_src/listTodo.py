#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour automatiquement faire la liste "to-do" de certains usagers sur des serveurs distants
#
#
#  Copyright 2022 F. Mailhot et Université de Sherbrooke
#

import argparse
from datetime import date, datetime
import subprocess
import re
import random
import os
import time

class ListTodo():
    """Classe utilisée pour appeler en continu l'application todo à distance :

    Copyright 2022, F. Mailhot et Université de Sherbrooke
    """

    def __init__(self):
        parser = argparse.ArgumentParser(prog='listTodo.py')
        parser.add_argument('-l', action='store_true', help="Liste des éléments dans la liste to-do des serveurs, pour les usagers définis dans MONNOM")
        parser.add_argument('-L', action='store_true', help="Liste des éléments dans la liste to-do des serveurs, pour tous les usagers")
        parser.add_argument('-i', action='store_true', help="Liste infinie des éléments dans la liste to-do des serveurs, pour les usagers définis dans MONNOM")
        parser.add_argument('-d', type=int, default=10, help="Délai entre les appels pour obtenir la liste infinie")
        args = parser.parse_args()

        self.setup_list_config()

        if args.i:
            self.list_infinite(args.d)
        if args.l:
            self.list_todo()
        if args.L:
            self.list_all_todo()
        return

    def setup_list_config(self):
        self.mon_usager = os.environ['MONNOM']
        self.mon_usager = self.mon_usager.replace('\'','')
        self.mes_usagers = self.mon_usager.split(",")
        self.mon_serveur = os.environ['MONSERVEUR']
        self.mon_serveur = self.mon_serveur.replace('\'','')
        self.mes_serveurs = self.mon_serveur.split(",")
        return

    def list_todo(self):
        for usager in self.mes_usagers:
            commande = "/usr/local/bin/todo -l -F " + usager
            for serveur in self.mes_serveurs:
                subprocess.run(["/usr/bin/ssh", serveur, commande])
            print("")
        return

    def list_infinite(self,delay):
        while True:
            self.list_todo()
            time.sleep(delay)
        return

    def list_all_todo(self):
        commande = "/usr/local/bin/todo -l"
        for serveur in self.mes_serveurs:
            subprocess.run(["/usr/bin/ssh", serveur, commande])
            print("")
        return

if __name__ == "__main__":
    list_todo = ListTodo()



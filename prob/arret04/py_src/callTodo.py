#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour ajouter automatiquement des tâches d'un certain usager à une liste "to-do" dans un serveur distant
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

class CallTodo():
    """Classe utilisée pour appeler en continu l'application todo à distance :

    Copyright 2022, F. Mailhot et Université de Sherbrooke
    """

    TODO = './todo.txt'
    TMP = './tmp.txt'
    LATEST_TODO = './latest_todo.txt'

    def __init__(self):
        parser = argparse.ArgumentParser(prog='callTodo.py')
        parser.add_argument('-r', action='store_true', help="Ajout d'un élément todo aléaloire (tiré de fortune)")
        parser.add_argument('-x', type=int, help="Retrait d'un élément présent")
        parser.add_argument('-u', type=str, default='Jean Néassé', help='Usager qui entre l\'élément todo')
        parser.add_argument('-l', action='store_true', help="Liste des éléments dans la liste to-do")
        parser.add_argument('-e', action='store_true', help="Imprime la variable d'environnement MYSERVER")
        parser.add_argument('-i', action='store_true', help="Créée des tâches et les retire sans arrêt")
        parser.add_argument('-w', action='store_true', help="Accès remote")
        parser.add_argument('-d', type=int, default=10, help="Délai entre les appels pour obtenir la liste infinie")
        args = parser.parse_args()

        args.u = self.get_fortune("people")
        self.init_setup()

        if args.r:
            self.add_todo(self.get_fortune(), args.u)
        if args.x:
            self.remove_todo(args.x)
        if args.l:
            if args.F:
                self.list_todo(args.F)
            else:
                self.list_todo('')
        if args.e:
            print(os.environ['MYSERVER'])
        if args.i:
            self.write_infinite(args.d)
        if args.w:
            self.write_todo("nouveau")
        return


    def init_setup(self):
        self.mon_usager = os.environ['MONNOM']
        self.mon_usager = self.mon_usager.replace('\'','')
        self.mon_serveur = os.environ['MONSERVEUR']
        self.mon_serveur = self.mon_serveur.replace('\'','')
        self.add_command = "/usr/local/bin/todo -u " + self.mon_usager + " -r"
        self.remove_command = "/usr/local/bin/todo -N 1"
        return

    def ajoute_des_taches(self):
        for i in range(4):
            self.write_todo(self.add_command)

    def write_infinite(self, delay):
        self.ajoute_des_taches()
        while True:
            add_iteration = random.randint(1,2)
            for i in range(add_iteration):
                subprocess.run(["/usr/bin/ssh", self.mon_serveur, self.add_command])
                time.sleep(delay)
            remove_iteration = random.randint(1,2)
            for i in range(remove_iteration):
                subprocess.run(["/usr/bin/ssh", self.mon_serveur, self.remove_command])
                time.sleep(delay)


    def get_fortune(self, fortune_db="fortunes"):
        fortune = subprocess.run(["fortune", fortune_db], capture_output=True)
        fortune_str = fortune.stdout.decode("utf-8").strip()
        return fortune_str

    def write_todo(self, commande):
        subprocess.run(["/usr/bin/ssh", self.mon_serveur, commande])


    def add_todo(self, new_msg, user):
        f = open(self.TODO, 'a+', encoding='utf-8')  # Add to the end of the file
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write("TODO<" + str(self.todo_num) + "> : Usager : [" + user + "], (" + str(today) + ":" + current_time + ") Task: " + str(new_msg) + '\n')
#        time.sleep(10)
        f.close()
        self.increment_latest_todo_num()
        return

    def remove_todo(self, todo_num):
        f = open(self.TODO, 'r', encoding='utf-8')
        tmp_f = open(self.TMP, 'w', encoding='utf-8')
        for line in f:
            line_todo_num = re.findall('<[0-9]+>', line)
            line_todo_num = int(re.findall('[0-9]+', str(line_todo_num))[0])
            if line_todo_num != todo_num:
                tmp_f.write(line)
        f.close()
        tmp_f.close()
        tmp_f = open(self.TMP, 'r', encoding='utf-8')
        f = open(self.TODO, 'w', encoding='utf-8')
        for line in tmp_f:
            f.write(line)
        return

    def remove_N_todo(self, number_of_removals):
        f = open(self.TODO, 'r', encoding='utf-8')
        tmp_f = open(self.TMP, 'w', encoding='utf-8')
        current_line = 1
        for line in f:
            if current_line > number_of_removals:
                tmp_f.write(line)
            current_line += 1
        f.close()
        tmp_f.close()
        tmp_f = open(self.TMP, 'r', encoding='utf-8')
        f = open(self.TODO, 'w', encoding='utf-8')
        for line in tmp_f:
            f.write(line)
        return

    def list_todo(self, filter):
        f = open(self.TODO, 'r', encoding='utf-8')
        for line in f:
            if filter == '':
                print(line, end='')
            else:
                if line.find(filter) != -1:
                    print(line, end='')
        return


if __name__ == "__main__":
    call_todo = CallTodo()



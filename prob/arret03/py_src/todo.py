#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour produire un gestionnaire de liste "to-do" minimaliste
#
#
#  Copyright 2022 F. Mailhot et Université de Sherbrooke
#

import argparse
from datetime import date, datetime
import subprocess
import re
import os

class Todo():
    """Classe utilisée pour effectuer la gestion d'une liste to-do minimaliste :

    Copyright 2022, F. Mailhot et Université de Sherbrooke
    """

    TODO = './todo.txt'
    TMP = './tmp.txt'
    LATEST_TODO = './latest_todo.txt'

    def __init__(self):
        self.todo_num = self.get_latest_todo_num()
        parser = argparse.ArgumentParser(prog='todo.py')
        parser.add_argument('-t', type=str, help="Ajout d'un nouvel élément todo, passé en paramètre par une chaine de caractères")
        parser.add_argument('-r', action='store_true', help="Ajout d'un élément todo aléaloire (tiré de fortune)")
        parser.add_argument('-x', type=int, help="Retrait d'un élément présent")
        parser.add_argument('-N', type=int, help="Retrait des N premiers todo de la liste")
        parser.add_argument('-u', type=str, default='Jean Néassé', help='Usager qui entre l\'élément todo')
        parser.add_argument('-U', action='store_true', help='Usager choisi au hasard')
        parser.add_argument('-F', type=str, help="Filtre de la liste to-do pour l\'usager unique indiqué")
        parser.add_argument('-l', action='store_true', help="Liste des éléments dans la liste to-do")
        parser.add_argument('-e', action='store_true', help="Utilise la variable d'environnement")
        args = parser.parse_args()
        if args.U:
            args.u = self.get_fortune("people")
        if args.t:
            self.add_todo(args.t, args.u)
        if args.r:
            self.add_todo(self.get_fortune(), args.u)
        if args.x:
            self.remove_todo(args.x)
        if args.N:
            self.remove_N_todo(args.N)
        if args.l:
            if args.F:
                self.list_todo(args.F)
            else:
                self.list_todo('')
        if args.e:
            print(os.environ['MYNAME'])
        return
    def get_fortune(self, fortune_db="fortunes"):
        fortune = subprocess.run(["fortune", fortune_db], capture_output=True)
        fortune_str = fortune.stdout.decode("utf-8").strip()
        return fortune_str

    def get_latest_todo_num(self):
        try:
            f = open(self.LATEST_TODO, 'r', encoding='utf-8')
            line = f.readline()
            latest_todo = int(line)
            f.close()
        except IOError:
            latest_todo = 1
        return latest_todo

    def increment_latest_todo_num(self):
        f = open(self.LATEST_TODO, 'w+', encoding='utf-8')
        f.write(str(self.todo_num + 1))
        f.close()
        return


    def add_todo(self, new_msg, user):
        f = open(self.TODO, 'a+', encoding='utf-8')  # Add to the end of the file
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write("TODO<" + str(self.todo_num) + "> : [" + user + "], (" + str(today) + ":" + current_time + ") : " + str(new_msg) + '\n')
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
    todo = Todo()



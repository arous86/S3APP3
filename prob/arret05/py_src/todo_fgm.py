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
import psycopg2
import psycopg2.extras
import configparser

class Parser():
    def parse_parameters(self):
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
        self.args = parser.parse_args()
        return

    def __init__(self):
        self.parse_parameters()
        return

class Db():
    host = "db"  # localhost for local testing, db for docker deployment
    port = "5435"
    database = "postgres"
    user = "postgres"
    password = "postgres"

    ADD_TODO_DEB = "insert into todo.extern_element (task,td_user) values ('"
    ADD_TODO_TASK_TO_USER = "', '"
    ADD_TODO_END = "');"

    DONE_TODO_USER_DEB = "update todo.extern_element set done_time = now()" \
                    "where id = (select id from todo.fn_oldest_user_task('"
    DONE_TODO_USER_END = "'));"

    DONE_TODO_ID_DEB = "update todo.extern_element set done_time = now()" \
                         "where id = "
    DONE_TODO_ID_END = ";"

    LIST_ALL_ACTIVE_TODO = "select * from todo.extern_element where is_active;"

    LIST_USER_TODO_DEB = "select * from todo.fn_user_active_elements ('"
    LIST_USER_TODO_END = "');"

    GET_OLDEST_TODO_DEB = "select * from todo.fn_oldest_user_task ('"
    GET_OLDEST_TODO_END = "');"

    GET_TASK_ID_DEB = "select * from todo.fn_id_task ('"
    GET_TASK_ID_END = "');"

    def bd_set_host(self,host):
        self.host = host
        return

    def bd_set_port(self,port):
        self.port = port
        return

    def bd_set_database(self,database):
        self.database = database
        return

    def bd_set_user(self,user):
        self.user = user
        return

    def bd_set_password(self,password):
        self.password = password
        return
    def bd_set_config(self):
        self.config = configparser.ConfigParser()
        self.config['DEFAULT'] = {'Host': self.host,
            'BdPort': self.port,
            'Database': self.database,
            'User': self.user,
            'Password': self.password}
        with open('db_config.txt', 'w') as configfile:
            self.config.write(configfile)
        return
    def bd_get_config(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read('db_config.txt')
            self.host = self.config['DEFAULT']['Host']
            self.port = self.config['DEFAULT']['BdPort']
            self.database = self.config['DEFAULT']['Database']
            self.user = self.config['DEFAULT']['User']
            self.password = self.config['DEFAULT']['Password']
        except:
            pass
        return

    def bd_config(self):
        self.bd_set_host(os.environ["DB_HOST"] if os.environ.__contains__("DB_HOST") else self.host)
        self.bd_set_database(os.environ["DB_NAME"] if os.environ.__contains__("DB_NAME") else self.database)
        self.bd_set_port(os.environ["DB_PORT"] if os.environ.__contains__("DB_PORT") else self.port)
        self.bd_set_user(os.environ["DB_USER"] if os.environ.__contains__("DB_USER") else self.user)
        self.bd_set_password(os.environ["DB_PASS"] if os.environ.__contains__("DB_PASS") else self.password)
        self.bd_set_config()

    def set_db(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return

    def get_oldest_todo(self, user):
        req = self.GET_OLDEST_TODO_DEB + user + self.GET_OLDEST_TODO_END
        self.cur.execute(req)
        return self.cur

    def get_task_id(self, task_id):
        req = self.GET_TASK_ID_DEB + task_id + self.GET_TASK_ID_END
        self.cur.execute(req)
        return self.cur

    def get_all_active_list(self):
        req = self.LIST_ALL_ACTIVE_TODO
        self.cur.execute(req)
        return self.cur

    def get_active_list(self, user):
        req = self.LIST_USER_TODO_DEB + user + self.LIST_USER_TODO_END
        self.cur.execute(req)
        return self.cur

    def escape_string(self,string_to_escape):
        escaped_string = string_to_escape.translate(str.maketrans({"'": r"''"}))
        return escaped_string

    def set_new_todo(self, task, user):
        escaped_string_task = self.escape_string(task)
        req = self.ADD_TODO_DEB + escaped_string_task + self.ADD_TODO_TASK_TO_USER + user + self.ADD_TODO_END
        self.cur.execute(req)
        self.conn.commit()
        return self.cur

    def set_done_oldest_todo(self, user):
        req = self.DONE_TODO_USER_DEB + user + self.DONE_TODO_USER_END
        self.cur.execute(req)
        self.conn.commit()
        return self.cur

    def set_done_todo_id(self, task_id):
        req = self.DONE_TODO_ID_DEB + str(task_id) + self.DONE_TODO_ID_END
        self.cur.execute(req)
        self.conn.commit()
        return self.cur

    def print_cur(self):
        for res in self.cur:
            print(res)

    def __init__(self, parser_args):
        self.parser = parser_args
        self.bd_config()
        self.set_db()
        return

class Todo():
    """Classe utilisée pour effectuer la gestion d'une liste to-do minimaliste :

    Copyright 2022, F. Mailhot et Université de Sherbrooke
    """

    def exec_command(self):
        if self.parser.args.U:
            self.parser.args.u = self.get_fortune("people")
        if self.parser.args.t:
            self.add_todo(self.args.t, self.parser.args.u)
        if self.parser.args.r:
            self.add_todo(self.get_fortune(), self.parser.args.u)
        if self.parser.args.x:
            self.remove_todo_id(self.parser.args.x)
        if self.parser.args.N:
            self.remove_N_todo(self.parser.args.N, self.parser.args.u)
        if self.parser.args.l:
            if self.parser.args.F:
                self.list_todo(self.parser.args.F)
            else:
                self.list_all_todo()
        if self.parser.args.e:
            print(os.environ['MYNAME'])
        return


    def __init__(self):
        self.parser = Parser()
        self.db = Db(self.parser.args)
        self.exec_command()
        return
        
    def get_fortune(self, fortune_db="fortunes"):
        fortune = subprocess.run(["fortune", fortune_db], capture_output=True)
        fortune_str = fortune.stdout.decode("utf-8").strip()
        return fortune_str

    def add_todo(self, new_msg, user):
        self.db.set_new_todo(new_msg,user)
        print("User: ", user, ", added task :", new_msg)
        return

    def remove_todo(self, user):
        self.db.set_done_oldest_todo(user)
        return

    def remove_todo_id(self, task_id):
        self.db.set_done_todo_id(task_id)
        return

    def remove_N_todo(self, number_of_removals, user):
        for i in range(number_of_removals):
            self.db.set_done_oldest_todo(user)
        return

    def list_todo_id(self, task_id):
        self.db.get_task_id(task_id)
        rows = self.db.cur.fetchall()
        for row in rows:
            print("Task id (", row['id'], "): ", row['td_user'], ": ", row['init_time'], "    >>", row['task'], "<<   ", sep='')
        return

    def list_todo(self, user):
        self.db.get_active_list(user)
        rows = self.db.cur.fetchall()
        for row in rows:
            print("Task id (", row['id'], "): ", row['td_user'], ": ", row['init_time'], "    >>", row['task'], "<<   ", sep='')
        return

    def list_all_todo(self):
        self.db.get_all_active_list()
        rows = self.db.cur.fetchall()
        for row in rows:
            print("Task id (", row['id'], "): ", row['td_user'], ": ", row['init_time'], "    >>", row['task'], "<<   ", sep='')
        return


if __name__ == "__main__":
    todo = Todo()



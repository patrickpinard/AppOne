#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Auteur  : Patrick Pinard
# Date    : 5 janvier 2024
# Objet   : AppOne est la base (framework) Flask pour une application web PWA
# Source  : app.py
# Version : 1

#   Clavier MAC :
#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    s
#   \  = Alt + Maj + /


import datetime
import json
import os
from threading import Thread
from time import sleep

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from myLOGLib import LogEvent, eventlog

load_dotenv()

####### Variables ###############

USERNAME = os.getenv("USERNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
NAME = os.getenv("APPNAME")
RELEASE = os.getenv("APPRELEASE")
AUTHOR = os.getenv("APPAUTHOR")
DATE = os.getenv("APPDATE")
INTERVAL = int(os.getenv("INTERVAL"))
DEBUG = bool(os.getenv("DEBUG"))

####### Démarrage du LOG file  ###############

now = datetime.datetime.now()
date = now.strftime("%-d.%-m")
time = now.strftime("%H:%M:%S")
dateandtime = date + " à " + time
LastRebootTime = dateandtime
LogEvent("Redémarrage le " + str(LastRebootTime))
LogEvent(NAME + " " + RELEASE + " " + AUTHOR)

####### Création de l'APPLICATION FLASK ###############

app = Flask(__name__)

####################   API   ############################


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """
    Shutdown
    """
    if request.method == "POST":
        LogEvent("Shutdown ...  bye bye !")
        # os.system('sudo halt')
    return jsonify("Shutdown en cours...")


@app.route("/reboot", methods=["POST", "GET"])
def reboot():
    """
    Reboot
    """
    if request.method == "POST":
        LogEvent("Reboot ... see you soon !")
        # os.system('sudo reboot')
    return jsonify("Reboot en cours...")


######### HOME ####################


@app.route("/", methods=["GET"])
def home():
    """Affiche la page principale"""

    return render_template(
        "home.html", Username=USERNAME, LastRebootTime=LastRebootTime
    )


######### PARAMETERS ####################


@app.route("/", methods=["GET"])
def dashboard():
    """Affiche la page par defaut : home"""

    return render_template(
        "home.html", Username=USERNAME, LastRebootTime=LastRebootTime
    )


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Affiche la page des dashboard"""

    return render_template(
        "dashboard.html", Username=USERNAME, LastRebootTime=LastRebootTime
    )


@app.route("/parameters", methods=["GET"])
def parameters():
    """Affiche la page des paramètres"""

    return render_template(
        "parameters.html", Username=USERNAME, LastRebootTime=LastRebootTime
    )


@app.route("/graph", methods=["GET"])
def graph():
    """Affiche la page des graphiques"""

    return render_template(
        "graph.html", Username=USERNAME, LastRebootTime=LastRebootTime
    )


@app.route("/events", methods=["GET"])
def events():
    """Affiche les events"""

    return render_template(
        "events.html",
        eventlog=eventlog,
        Username=USERNAME,
        LastRebootTime=LastRebootTime,
    )


@app.route("/formulaire", methods=["GET"])
def formulaire():
    return render_template(
        "formulaire.html",
        eventlog=eventlog,
        Username=USERNAME,
        LastRebootTime=LastRebootTime,
    )


####################   fin API   ###########################


##### Threads  #######


class FlaskApp(Thread):
    def __init__(self, threadID, name):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        LogEvent("FlaskApp Thread started")
        try:
            # app.run(host='0.0.0.0', port = 443, debug=False, ssl_context=('cert.pem', 'key.pem'))
            app.run(host="0.0.0.0", port=80, debug=False)
        except OSError as err:
            LogEvent("ERREUR : thread FlaskApp ! Message : " + str(err))


class Loop(Thread):
    def __init__(self, threadID, name):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global INTERVAL, db

        LogEvent("Loop Thread started")
        id = 0
        while True:
            try:
                while True:
                    LogEvent(" *** Thread Loop id = " + str(id) + " ***")
                    id = id + 1
                    sleep(INTERVAL)

            except OSError as err:
                LogEvent("ERREUR : thread Loop ! Message : " + str(err))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port=80, debug=True)
    # thread1 = FlaskApp(1, "FlaskApp")
    # thread2 = Loop(2, "Loop")

    # thread1.start()
    # thread2.start()

    # thread1.join()
    # thread2.join()

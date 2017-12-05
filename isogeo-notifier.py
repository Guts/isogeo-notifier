#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

"""
    __author__ = "GeoJulien"
    __copyright__ = "Copyright 2016, Isogeo"
    __credits__ = ["Isogeo", "GeoJulien"]
    __license__ = "GPL3"
    __version__ = "1.1.0"
    __maintainer__ = "Julien Moura"
    __email__ = "projects+notifier@isogeo.com"
    __status__ = "Beta"
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import ConfigParser     # to manage options.ini
from datetime import datetime
from os import path

# 3rd party library
from dateutil.parser import parse as dtparse
from isogeo_pysdk import Isogeo
from win10toast import ToastNotifier

# ############################################################################
# ######### Main program ###########
# ##################################

# application parameters stored into an ini file
settings_file = r"isogeo_params.ini"

# testing ini file
if not path.isfile(path.realpath(settings_file)):
    print("ERROR: to execute this script as standalone"
          " you need to store your Isogeo application "
          "settings in a isogeo_params.ini file. "
          "You can use the template to set your own.")
    import sys
    sys.exit()
else:
    pass

# reading ini file
config = ConfigParser.SafeConfigParser()
config.read(settings_file)

share_id = config.get('auth', 'app_id')
share_token = config.get('auth', 'app_secret')
last_exe = config.get('metrics', 'last_exe')
last_total = int(config.get('metrics', 'last_total'))


# ------------ Real start ----------------
# instanciating Isogeo class
isogeo = Isogeo(client_id=share_id,
                client_secret=share_token,
                lang="fr")

token = isogeo.connect()

# Windows 10 notifications class
notif = ToastNotifier()

# ------------ REAL START ----------------------------
latest_data_modified = isogeo.search(token,
                                     page_size=10,
                                     order_by="modified",
                                     whole_share=0,
                                     sub_resources=["events"]
                                     )

# parsing the previous date
last_exe = dtparse(last_exe).strftime("%a %d %B %Y (%H:%M)")
last_exe = last_exe.decode("Latin1")

# comparing total of metadats shared since last time
now_total = latest_data_modified.get('total')

if now_total > last_total:
    notif.show_toast("Isogeo - Total partage",
                     "{} données ajoutées\ndepuis le {}"
                     .format(now_total - last_total, last_exe),
                     icon_path=r"img/favicon.ico",
                     duration=10)
elif now_total < last_total:
    notif.show_toast("Isogeo - Total partage",
                     "{} données retirées\ndepuis le {}"
                     .format(last_total - now_total, last_exe),
                     icon_path=r"img/favicon.ico",
                     duration=10)
elif now_total == last_total:
    notif.show_toast("Isogeo - Total partage",
                     "Pas de changement \ndepuis le {}"
                     .format(last_exe),
                     icon_path=r"img/favicon.ico",
                     duration=10)
else:
    pass

# for md in latest_data_modified.get("results"):
#     print('you')


# print("Last 10 data updated \nTitle | datetime\n\t description")
# for md in latest_data_modified.get("results"):
#     title = md.get('title')
#     evt_description = md.get("events")[0].get("description")
#     print(str("___________________\n\n{} | {} \n\t {}").
#           format(title.encode("utf8"),
#                  dtparse(md.get("modified")[:19]).strftime("%a %d %B %Y"),
#                  evt_description.encode("utf8")))
#     notif.balloon_tip('Isogeo - Dernières données modifiée', title)

# ------------ SAVE METRICS ----------------------------
config.set('metrics', 'last_exe', str(datetime.now()))
config.set('metrics', 'last_total', str(latest_data_modified.get("total")))

# Writing our configuration file to 'example.ini'
with open('isogeo_params.ini', 'wb') as configfile:
    config.write(configfile)

del(notif)

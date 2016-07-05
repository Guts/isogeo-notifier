# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# ------------------------------------------------------------------------------
# Name:         Isogeo sample - Latest modified datasets
# Purpose:      Get the latest modified datasets from an Isogeo share, using
#               the Isogeo API Python minimalist SDK.
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      14/02/2016
# Updated:      18/02/2016
# ------------------------------------------------------------------------------

# ##############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import ConfigParser     # to manage options.ini
from datetime import datetime
from os import path

# 3rd party library
from dateutil.parser import parse as dtparse

# Isogeo
from isogeo_pysdk import Isogeo

# custom
from modules.win10_notif import WindowsBalloonTip

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
notif = WindowsBalloonTip()

# ------------ REAL START ----------------------------
latest_data_modified = isogeo.search(token,
                                     page_size=10,
                                     order_by="modified",
                                     whole_share=0,
                                     sub_resources=["events"]
                                     )

# parsing the previous date
last_exe = dtparse(last_exe).strftime("%a %d %B %Y (%H:%M)")

# comparing total of metadats shared since last time
now_total = latest_data_modified.get('total')

if now_total > last_total:
    notif.balloon_tip("Isogeo - Total partage", u"{} nouvelles données\ndepuis le {}".format(now_total - last_total, last_exe))
elif now_total < last_total:
    notif.balloon_tip("Isogeo - Total partage", u"{} données supprimées\ndepuis le {}".format(last_total - now_total, last_exe))
elif now_total == last_total:
    notif.balloon_tip("Isogeo - Total partage", u"Aucune nouvelle donnée \ndepuis le {}".format(last_exe))
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

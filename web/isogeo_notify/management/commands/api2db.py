# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# ############################################################################
# ########## Libraries #############
# ##################################
# Standard library
import logging
from os import path

# 3rd party modules
import arrow
from isogeo_pysdk import Isogeo

# Django project
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from isogeo_notify.models import Metadata, Workgroup

# ############################################################################
# ########## Globals ##############
# #################################

# logger = logging.getLogger("ElPaso")


# ############################################################################
# ########### Classes #############
# #################################


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _update_db(self):
        """Update metadata list from API."""
        # get stored metadata
        db_mds = Metadata.objects.all()
        db_wgs = Workgroup.objects.all()

        # connect to isogeo
        isogeo = Isogeo(client_id=settings.ISOGEO_CLIENT_ID,
                        client_secret=settings.ISOGEO_CLIENT_SECRET,
                        lang="fr")
        token = isogeo.connect()
        search = isogeo.search(token,
                                  # page_size=10,
                                  order_by="modified",
                                  # whole_share=0,
                                  # sub_resources=["events"]
                                  )
        # tags
        tags = search.get("tags")
        for tag in tags:
            if tag.startswith("owner"):
                new_owner = Workgroup(isogeo_uuid=tag[6:-1],
                                      label=tags.get(tag))
                new_owner.save()


        # metadatas
        # for md in search.get("results"):
        #     try:
        #         new_md = Metadata(isogeo_id=md.get("_id"),
        #                           title=md.get("title", "No title"),
        #                           name=md.get("name"),
        #                           abstract=md.get("abstract"),
        #                           md_dt_crea=md.get("_created"),
        #                           md_dt_update=md.get("_modified"),
        #                           rs_dt_crea=md.get("created"),
        #                           rs_dt_update=md.get("modified"),
        #                           source=True)
        #         new_md.save()
        #         logging.info("Metadata added")
        #     except IntegrityError:
        #         # in case of duplicated offer
        #         logging.error("Metadata already existed")
        #         continue
        logging.info("{} metadata added")

    def handle(self, *args, **options):
        self._update_db()

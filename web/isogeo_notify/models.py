# Standard library
import random
import uuid
# Django
from django.db import models


class MetadataType(models.Model):
    label = models.CharField(max_length=50,
                             db_index=True,
                             unique=True,
                             default="VECTOR",
                             verbose_name="Type de métadonnée",
                             )

    description = models.TextField(blank=True)
    api_filter = models.TextField(blank=True)
    api_val = models.TextField(blank=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Type de métadonnée"
        verbose_name_plural = "Types de métadonnée"


class CrawlerHistory(models.Model):
    dt_start = models.DateTimeField("Début")
    dt_end = models.DateTimeField("Fin")
    md_count = models.IntegerField("Nombre de métadonnées")
    md_modified = models.IntegerField("Métadonnées modifiées (t-1)")

    def __str__(self):
        return self.dt_start

    class Meta:
        verbose_name = "Historique du crawler"
        verbose_name_plural = "Historiques du crawler"


class State(models.Model):
    stid = models.AutoField(primary_key=True,
                            default=random.getrandbits(10))
    label = models.CharField(max_length=50,
                             db_index=True,
                             unique=True,
                             default="ACTIVE",
                             verbose_name="Statut",
                             )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Statut de la métadonnée"
        verbose_name_plural = "Status des métadonnées"


class Workgroup(models.Model):
    wgid = models.AutoField(primary_key=True)
    isogeo_uuid = models.UUIDField("Identifiant groupe de travail",
                                   default=uuid.uuid4,
                                   editable=False)
    label = models.CharField(max_length=150,
                             verbose_name="Groupe de travail",
                             )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Groupe de travail"
        verbose_name_plural = "Groupes de travail"


class Metadata(models.Model):
    mdid = models.AutoField("ID",
                            primary_key=True,
                            auto_created=True,
                            default=uuid.uuid4)
    isogeo_uuid = models.UUIDField(default=uuid.uuid4,
                                   editable=False)
    workgroup = models.ForeignKey(Workgroup,
                                  blank=True,
                                  default=random.getrandbits(100),
                                  verbose_name="Groupe de travail")
    # identification
    title = models.CharField("Titre", max_length=300)
    name = models.CharField("Nom technique", max_length=300, blank=True)
    abstract = models.TextField("Résumé", blank=True)

    # dates
    md_dt_crea = models.DateTimeField("Création de la métadonnée",
                                      blank=True)
    md_dt_update = models.DateTimeField("Dernière modification de la métadonnée",
                                        blank=True)
    md_dt_shared_first = models.DateTimeField("Vue la première fois",
                                              blank=True)
    md_dt_shared_last = models.DateTimeField("vue la dernière fois",
                                             blank=True)
    rs_dt_crea = models.DateTimeField("Création de la donnée",
                                      blank=True)
    rs_dt_update = models.DateTimeField("Dernière modification de la donnée",
                                        blank=True)
    # related fields
    md_type = models.ForeignKey(MetadataType,
                                verbose_name="Type de ressource décrite")
    state = models.ForeignKey(State,
                              blank=True,
                              null=True,
                              verbose_name="Statut")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Métadonnée"
        verbose_name_plural = "Métadonnées"
        get_latest_by = "md_dt_update"

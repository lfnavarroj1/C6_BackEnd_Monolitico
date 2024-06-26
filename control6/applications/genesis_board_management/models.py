from django.db import models


# Create your models here.

class ResultBt(models.Model):
    id = models.BigIntegerField(primary_key=True)
    num_ticket = models.CharField(max_length=14)
    start_date = models.BigIntegerField()
    notify_count = models.IntegerField()
    notify_subtype = models.CharField(max_length=60)
    cft_id = models.IntegerField()
    cft = models.CharField(max_length=60)
    interruption = models.BooleanField()
    work_group_cod = models.CharField(max_length=25)
    uoid = models.IntegerField()
    uo = models.CharField(max_length=60)
    tdc_expirado = models.BooleanField()
    tdc = models.BigIntegerField()
    isrejectedornotcreated = models.BooleanField()
    address = models.CharField(max_length=70)
    groupable = models.BooleanField()
    localadress = models.CharField(max_length=160)
    chargedcustomerflg = models.BooleanField()
    provisionalrepairflg = models.BooleanField()
    commentcc = models.TextField()
    prioritydanger = models.IntegerField()
    createtime = models.BigIntegerField()
    updatetime = models.BigIntegerField()
    facreatetime = models.BigIntegerField()
    faupdatetime = models.BigIntegerField()
    unreaddescriptionflag = models.IntegerField()
    tdchighlightflag = models.IntegerField()
    ten = models.TimeField()
    stmonexecution = models.BooleanField()
    status_id = models.IntegerField()
    status_description = models.CharField(max_length=20)
    status_shortdescription = models.CharField(max_length=5)
    tickettype_id = models.IntegerField()
    tickettype_description = models.CharField(max_length=60)
    tickettype_shortdescription = models.CharField(max_length=4)
    origin_id = models.IntegerField()
    origin_description = models.CharField(max_length=150)
    priority_id = models.IntegerField(max_length=250)

    # priority_description = models.IntegerField(max_length=250)
    # priority_shortdescription = models.CharField(max_length=250)
    # tensionlevel_id = models.CharField(max_length=250)
    # tensionlevel_description = models.CharField(max_length=250)
    # tensionlevel_shortdescription = models.CharField(max_length=250)
    # eventtype_id = models.CharField(max_length=250)
    # eventtype_description = models.CharField(max_length=250)
    # nclie = models.CharField(max_length=250)
    # network_substation_id = models.CharField(max_length=250)
    # network_substation_description = models.CharField(max_length=250)
    # network_line_id = models.CharField(max_length=250)
    # network_line_description = models.CharField(max_length=250)
    # network_linebt_id = models.CharField(max_length=250)
    # network_linebt_description = models.CharField(max_length=250)
    # network_trafo_id = models.CharField(max_length=250)
    # network_trafo_description = models.CharField(max_length=250)
    # network_cd_id = models.CharField(max_length=250)
    # network_cd_description = models.CharField(max_length=250)
    # network_pcr_id = models.CharField(max_length=250)
    # network_pcr_description = models.CharField(max_length=250)

    cause_id = models.IntegerField()
    cause_description = models.CharField(max_length=120)
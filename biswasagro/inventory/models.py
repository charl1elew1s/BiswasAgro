from django.db import models


# Create your models here.
class Dailyworks(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    worktype = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=5, decimal_places=0)
    unit = models.CharField(max_length=10)
    personel = models.CharField(max_length=20)
    comment = models.CharField(max_length=50)
    logs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dailyworks'

    def __str__(self):
        return (f"id={self.id} date={self.date} worktype={self.worktype} item={self.item} "
                f"amount={self.amount} unit={self.unit} personel={self.personel} comment={self.comment} "
                f"logs={self.logs}")


class Fishbuy(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    fishname = models.CharField(max_length=20)
    buyfrom = models.CharField(max_length=50)
    buyamount = models.IntegerField()
    fishquantity = models.IntegerField()
    price = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, db_comment='1 is paid, 2 is due')
    fishto = models.CharField(max_length=50)
    vouchar = models.CharField(max_length=15)
    comments = models.CharField(max_length=50)
    logs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'fishbuy'

    def __str__(self):
        return (f"id={self.id} date={self.date} fishname={self.fishname} buyfrom={self.buyfrom} "
                f"buyamount={self.buyamount} fishquantity={self.fishquantity} price={self.price} "
                f"status={self.status} fishto={self.fishto} vouchar={self.vouchar} "
                f"comments={self.comments} logs={self.logs}")


class Fishtype(models.Model):
    id = models.AutoField(primary_key=True)
    fishname = models.CharField(db_column='FishName', unique=True, max_length=20)  # Field name made lowercase.
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'fishtype'

    def __str__(self):
        return f"id={self.id} fishname={self.fishname} logs={self.logs}"


class Fooddistribution(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    gher = models.IntegerField()
    item = models.IntegerField()
    amount = models.IntegerField()
    unit = models.IntegerField()
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'fooddistribution'

    def __str__(self):
        return (f"id={self.id} date={self.date} gher={self.gher} item={self.item} amount={self.amount} "
                f"unit={self.unit} logs={self.logs}")


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=20)
    item_name = models.CharField(max_length=15, unique=True)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'items'

    def __str__(self):
        return f"id={self.id} sector={self.sector} item_name={self.item_name} logs={self.logs}"


class Units(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=10)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'units'

    def __str__(self):
        return f"id={self.id} unit={self.unit} logs={self.logs}"


class Land(models.Model):
    id = models.AutoField(primary_key=True)
    gher = models.IntegerField()
    mousa = models.CharField(max_length=15)
    dag = models.CharField(max_length=20)
    khotian = models.CharField(max_length=3)
    amount = models.FloatField()
    plane_land = models.FloatField()
    par_cannel = models.FloatField()
    owners = models.CharField(max_length=200)
    comment = models.CharField(max_length=100)
    logs = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'land'

    def __str__(self):
        return (f"id={self.id} gher={self.gher} mousa={self.mousa} dag={self.dag} "
                f"khotian={self.khotian} amount={self.amount} plane_land={self.plane_land} "
                f"par_cannel={self.par_cannel} owners={self.owners} comment={self.comment} "
                f"logs={self.logs}")


class Mousa(models.Model):
    id = models.AutoField(primary_key=True)
    mousa = models.CharField(max_length=255, blank=True, null=True)
    dag = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    vc_numnber = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, db_comment='1 is paid, 2 is pending ')
    log = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mousa'

    def __str__(self):
        return (f"id={self.id} mousa={self.mousa} dag={self.dag} owner={self.owner} date={self.date} "
                f"amount={self.amount} term={self.term} vc_numnber={self.vc_numnber} status={self.status} "
                f"log={self.log}")


class Mousaname(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'mousaname'

    def __str__(self):
        return f"id={self.id} name={self.name}"


class Sectors(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(unique=True, max_length=15)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sectors'

    def __str__(self):
        return f"id={self.id} sector={self.sector} logs={self.logs}"


class Sources(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=20)
    logs = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'sources'

    def __str__(self):
        return f"id={self.id} source={self.source} logs={self.logs}"


class Term(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'term'

    def __str__(self):
        return f"id={self.id} term={self.term}"

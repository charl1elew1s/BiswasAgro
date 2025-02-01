from django.db import models


# Create your models here.
class Fishbuy(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    fishname = models.CharField(max_length=20)
    buyfrom = models.CharField(max_length=50)
    buyamount = models.IntegerField()
    fishquantity = models.IntegerField()
    price = models.IntegerField()
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
                f"fishto={self.fishto} vouchar={self.vouchar} comments={self.comments} logs={self.logs}")


class Fishtype(models.Model):
    id = models.AutoField(primary_key=True)
    fishname = models.CharField(db_column='FishName', max_length=20)  # Field name made lowercase.
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'fishtype'

    def __str__(self):
        return f"id={self.id} fishname={self.fishname} logs={self.logs}"


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=20)
    item_name = models.CharField(max_length=15)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'items'

    def __str__(self):
        return f"id={self.id} sector={self.sector} item_name={self.item_name} logs={self.logs}"


class Units(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(unique=True, max_length=10)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'units'

    def __str__(self):
        return f"id={self.id} unit={self.unit} logs={self.logs}"


class Land(models.Model):
    id = models.AutoField(primary_key=True)
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
        return (f"id={self.id} mousa={self.mousa} dag={self.dag} khotian={self.khotian} "
                f"amount={self.amount} plane_land={self.plane_land} par_cannel={self.par_cannel} "
                f"owners={self.owners} comment={self.comment} logs={self.logs}")


class Sectors(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(unique=True, max_length=15)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sectors'

    def __str__(self):
        return f"id={self.id} sector={self.sector} logs={self.logs}"


class TblProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    prix = models.IntegerField(db_column='Prix')  # Field name made lowercase.
    categorie = models.CharField(db_column='Categorie', max_length=50)  # Field name made lowercase.
    etat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_product'

    def __str__(self):
        return f"id={self.id} name={self.name} prix={self.prix} categorie={self.categorie} etat={self.etat}"

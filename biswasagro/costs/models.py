from django.db import models


# Create your models here.
class Cost(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    costcategory = models.CharField(max_length=20)
    costitems = models.CharField(max_length=20)
    buyamount = models.FloatField()
    unit = models.CharField(max_length=10)
    cost = models.FloatField()
    buyer = models.CharField(max_length=20)
    buyvoucher = models.CharField(max_length=20)
    comment = models.CharField(max_length=50)
    logs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cost'

    def __str__(self):
        return f"id={self.id} date={self.date} costcateogry={self.costcategory} costitems={self.costitems}"


class Costitems(models.Model):
    id = models.AutoField(primary_key=True)
    costitems = models.CharField(unique=True, max_length=20)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'costitems'

    def __str__(self):
        return f"id={self.id} costitems={self.costitems} logs={self.logs}"


class Costpurpose(models.Model):
    id = models.AutoField(primary_key=True)
    costpurpose = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'costpurpose'

    def __str__(self):
        return f"id={self.id} costpurpose={self.costpurpose}"


class Earning(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    sector = models.IntegerField()
    item = models.IntegerField()
    source = models.IntegerField()
    quantity_per_unit = models.IntegerField()
    quantity = models.IntegerField()
    unit = models.IntegerField()
    price = models.IntegerField()
    memo = models.CharField(max_length=15)
    comment = models.CharField(max_length=30)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'earning'

    def __str__(self):
        return (f"id={self.id} date={self.date} sector={self.sector} "
                f"item={self.item} source={self.source} quantity_per_unit={self.quantity_per_unit} "
                f"quantity={self.quantity} unit={self.unit} price={self.price} memo={self.memo} "
                f"comment={self.comment} logs={self.logs}")


class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    name = models.CharField(max_length=20)
    amount = models.FloatField()
    comments = models.CharField(max_length=50)
    logs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'investment'

    def __str__(self):
        return (f"id={self.id} date={self.date} name={self.name} amount={self.amount} "
                f"comments={self.comments} logs={self.logs}")

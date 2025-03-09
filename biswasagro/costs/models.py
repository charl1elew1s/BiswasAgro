from django.db import models


# Create your models here.
class Cost(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    costcategory = models.CharField(max_length=20)
    costitems = models.CharField(max_length=20, blank=True, null=True)
    buyamount = models.FloatField()
    unit = models.CharField(max_length=10)
    cost = models.FloatField()
    status = models.IntegerField(blank=True, null=True)
    buyer = models.CharField(max_length=20)
    buyvoucher = models.CharField(max_length=20)
    comment = models.CharField(max_length=50)
    logs = models.CharField(max_length=50)
    costitems_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cost'

    def __str__(self):
        return (f"id={self.id} date={self.date} costcategory={self.costcategory} costitems={self.costitems} "
                f"buyamount={self.buyamount} unit={self.unit} cost={self.cost} status={self.status} "
                f"buyer={self.buyer} buyvoucher={self.buyvoucher} comment={self.comment} "
                f"logs={self.logs} costitmes_id={self.costitems_id}")


class Costitems(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.IntegerField()
    costitems = models.CharField(unique=True, max_length=20)
    logs = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'costitems'

    def __str__(self):
        return f"id={self.id} sector={self.sector} costitems={self.costitems} logs={self.logs}"


class Costpurpose(models.Model):
    id = models.AutoField(primary_key=True)
    costpurpose = models.CharField(unique=True, max_length=20)

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
    quantity_per_unit = models.FloatField()
    quantity = models.IntegerField()
    unit = models.IntegerField()
    price = models.IntegerField()
    status = models.IntegerField(blank=True, null=True, db_comment='1 is paid, 2 is due')
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


class Loandetails(models.Model):
    loanid = models.AutoField(primary_key=True)
    investerid = models.IntegerField()
    amount = models.IntegerField()
    interestpermonth = models.DecimalField(max_digits=3, decimal_places=2)
    conditions = models.CharField(max_length=50)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'loandetails'

    def __str__(self):
        return (
            f"loanid={self.loanid} investerid={self.investerid} amount={self.amount} "
            f"interestpermonth={self.interestpermonth} conditions={self.conditions} logs={self.logs}")


class LoanProvidersInfo(models.Model):
    investerid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    address = models.CharField(db_column='Address', max_length=50)  # Field name made lowercase.
    mobile = models.TextField(db_column='Mobile')  # Field name made lowercase.
    refference = models.CharField(db_column='Refference', max_length=20)  # Field name made lowercase.
    logs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'loan_providers_info'

    def __str__(self):
        return (f"investerid={self.investerid} name={self.name} address={self.address} "
                f"mobile={self.mobile} refference={self.refference} logs={self.logs}")


class LoanTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    loanid = models.IntegerField()
    investerid = models.IntegerField()
    date = models.DateField()
    payment = models.IntegerField(db_column='Payment')  # Field name made lowercase.
    voucherno = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'loan_transactions'

    def __str__(self):
        return (f"id={self.id} loanid={self.loanid} investerid={self.investerid} "
                f"date={self.date} payment={self.payment} voucherno={self.voucherno}")

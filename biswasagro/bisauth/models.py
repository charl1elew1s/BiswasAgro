from django.db import models


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=15, unique=True, db_comment='role_text')

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return f"id={self.id} role={self.role}"


class Usersinfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=260)
    role = models.CharField(max_length=15)
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.
    email = models.CharField(max_length=20)
    mobile = models.TextField()

    class Meta:
        managed = False
        db_table = 'usersinfo'

    def __str__(self):
        return (f"id={self.id} name={self.name} username={self.username} "
                f"password={self.password} role={self.role} isactive={self.isactive} email={self.email} "
                f"mobile={self.mobile}")


class Staff(models.Model):
    staffno = models.AutoField(db_column='staffNo', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=15, blank=True, null=True)
    post = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=30)
    mobile = models.CharField(max_length=11)
    reference = models.CharField(max_length=15)
    log = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'staff'

    def __str__(self):
        return (f"staffno={self.staffno} name={self.name} post={self.post} "
                f"salary={self.salary} address={self.address} mobile={self.mobile} reference={self.reference} "
                f"log={self.log}")


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=20)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=30)  # Field name made lowercase.
    mobile = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'staffs'

    def __str__(self):
        return (f"id={self.id} name={self.name} designation={self.designation} "
                f"address={self.address} address={self.address} mobile={self.mobile}")


class Salary(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    purpose = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    total = models.IntegerField()
    personel = models.CharField(max_length=50)
    voucher = models.CharField(max_length=5)
    status = models.IntegerField(blank=True, null=True, db_comment='1 is paid, 2 is due')
    comment = models.CharField(max_length=20)
    logs = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'salary'

    def __str__(self):
        return (f"id={self.id} date={self.date} purpose={self.purpose} reason={self.reason} "
                f"quantity={self.quantity} rate={self.rate} total={self.total} personel={self.personel} "
                f"voucher={self.voucher} status={self.status} comment={self.comment} logs={self.logs}")

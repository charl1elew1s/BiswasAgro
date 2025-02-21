from django.db import models


class TblRoles(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, blank=True, null=True, db_comment='role_text')

    class Meta:
        managed = False
        db_table = 'tbl_roles'

    def __str__(self):
        return f"id={self.id} role={self.role}"


class TblUsers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=25, blank=True, null=True)
    roleid = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(null=False, blank=True)
    updated_at = models.DateTimeField(null=False, blank=True)

    class Meta:
        managed = False
        db_table = 'tbl_users'

    def __str__(self):
        return (f"id={self.id} name={self.name} username={self.username} "
                f"email={self.email} password={self.password} mobile={self.mobile} "
                f"roleid={self.roleid} is_active={self.is_active} "
                f"created_at={self.created_at} updated_at={self.updated_at}")

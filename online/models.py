# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Book(models.Model):
    id = models.BigIntegerField(primary_key=True)
    rating_max = models.IntegerField(blank=True, null=True)
    rating_numraters = models.BigIntegerField(db_column='rating_numRaters', blank=True, null=True)  # Field name made lowercase.
    rating_average = models.CharField(max_length=20, blank=True, null=True)
    rating_min = models.IntegerField(blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    pub_date = models.CharField(max_length=20, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    origin_title = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=512, blank=True, null=True)
    binding = models.CharField(max_length=200, blank=True, null=True)
    translator = models.CharField(max_length=200, blank=True, null=True)
    catalog = models.CharField(max_length=512, blank=True, null=True)
    ebook_url = models.CharField(max_length=512, blank=True, null=True)
    pages = models.BigIntegerField(blank=True, null=True)
    imgages = models.CharField(max_length=512, blank=True, null=True)
    alt = models.CharField(max_length=512, blank=True, null=True)
    douban_id = models.CharField(max_length=512, blank=True, null=True)
    publisher = models.CharField(max_length=512, blank=True, null=True)
    isbn10 = models.CharField(max_length=512, blank=True, null=True)
    isbn13 = models.CharField(max_length=512, blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    alt_title = models.CharField(max_length=512, blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    ebook_price = models.CharField(max_length=20, blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    series_title = models.CharField(max_length=512, blank=True, null=True)
    price = models.CharField(max_length=512, blank=True, null=True)
    json_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


class Cart(models.Model):
    id = models.BigIntegerField(primary_key=True)
    cart_item = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    cart_owner = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart'


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'category'


class Comment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    content = models.CharField(max_length=200)
    owner = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    id_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    role = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'

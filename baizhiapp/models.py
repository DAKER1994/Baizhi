# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TTest(models.Model):
    userid = models.TextField(blank=True, null=True)
    employer_name = models.TextField(blank=True, null=True)
    stature = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    born = models.TextField(blank=True, null=True)
    jobname = models.TextField(blank=True, null=True)
    salary = models.TextField(blank=True, null=True)
    hope_location = models.TextField(blank=True, null=True)
    native_place = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    school = models.TextField(blank=True, null=True)
    profession = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    now_location = models.TextField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    politics_status = models.TextField(blank=True, null=True)
    job_status = models.TextField(blank=True, null=True)
    hope_industry = models.TextField(blank=True, null=True)
    hope_position = models.TextField(blank=True, null=True)
    job_category = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_test'


class TUser(models.Model):
    username = models.TextField(blank=True, null=True)
    usertel = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'


class TZpgg(models.Model):
    userid = models.TextField(blank=True, null=True)
    employer_name = models.TextField(blank=True, null=True)
    stature = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    born = models.TextField(blank=True, null=True)
    jobname = models.TextField(blank=True, null=True)
    salary = models.TextField(blank=True, null=True)
    hope_location = models.TextField(blank=True, null=True)
    native_place = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    school = models.TextField(blank=True, null=True)
    profession = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    now_location = models.TextField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    politics_status = models.TextField(blank=True, null=True)
    job_status = models.TextField(blank=True, null=True)
    hope_industry = models.TextField(blank=True, null=True)
    hope_position = models.TextField(blank=True, null=True)
    job_category = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_zpgg'


from django.utils import timezone

#访问网站的ip地址和次数
class User_ip(models.Model):
    ip=models.CharField(verbose_name='IP地址',max_length=30)    #ip地址
    count=models.IntegerField(verbose_name='访问次数',default=0) #该ip访问次数
    country = models.CharField(verbose_name='所在国家',max_length=30)
    location = models.CharField(verbose_name='地区',max_length=30)
    province = models.CharField(verbose_name='省份',max_length=30)
    city = models.CharField(verbose_name='城市',max_length=30)
    operator = models.CharField(verbose_name='所属运营商',max_length=30)

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.ip
class Userip(models.Model):
    ip=models.CharField(verbose_name='IP地址',max_length=30)    #ip地址
    count=models.IntegerField(verbose_name='访问次数',default=0) #该ip访问次数
    # country = models.CharField(verbose_name='所在国家',max_length=30)
    # location = models.CharField(verbose_name='地区',max_length=30)
    # province = models.CharField(verbose_name='省份',max_length=30)
    # city = models.CharField(verbose_name='城市',max_length=30)
    # operator = models.CharField(verbose_name='所属运营商',max_length=30)

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.ip

#网站总访问次数
class VisitNumber(models.Model):
    count=models.IntegerField(verbose_name='网站访问总次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.count)

#单日访问量统计
class DayNumber(models.Model):
    day=models.DateField(verbose_name='日期',default=timezone.now)
    count=models.IntegerField(verbose_name='网站访问次数',default=0) #网站访问总次数
    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.day)

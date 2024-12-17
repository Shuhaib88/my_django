from django.db import models

class pallifund(models.Model):
    name = models.CharField(max_length=50)
    id_no = models.CharField(max_length=30)
    reciept_no = models.CharField(max_length=30)
    fund_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    amount = models.CharField(max_length=6)
    total_amount = models.CharField(max_length=6)
    debit_credit = models.CharField(max_length=6)
    date = models.CharField(max_length=15)
    
    def __str__(self):
      return f"{self.name} ({self.reciept_no} - {self.total_amount})"

class masapirivu(models.Model):
    name = models.CharField(max_length=50)
    id_no = models.CharField(max_length=30)
    reciept_no = models.CharField(max_length=30)
    palli = models.CharField(max_length=6)
    madrassa = models.CharField(max_length=6)
    mess = models.CharField(max_length=6)
    description = models.CharField(max_length=100)
    total_amount = models.CharField(max_length=6)
    debit_credit = models.CharField(max_length=6)
    date = models.CharField(max_length=15)

class additionalfund(models.Model):
    reciept_no = models.CharField(max_length=30)
    fund_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    amount = models.CharField(max_length=6)
    
class addmahallumembers(models.Model):
    id_no = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    house_name = models.CharField(max_length=30)
    family_member = models.CharField(max_length=20)
    relation = models.CharField(max_length=10)

class addfamilymembers(models.Model):
    id_no = models.CharField(max_length=30)
    family_member = models.CharField(max_length=30)
    relation = models.CharField(max_length=10)




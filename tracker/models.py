from django.db import models

class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title
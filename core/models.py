from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Employee(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    # It can be DateTimeField. however, this scenario is more user-friendly.
    name = models.CharField(max_length=250)
    hour = models.IntegerField()
    price_for_each_hour = models.BigIntegerField()

    total_salary = models.BigIntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.hour and self.price_for_each_hour:
            self.total_salary = self.hour * self.price_for_each_hour
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('PG', 'Pending'),
        ('DE', 'Done')
    )
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, models.CASCADE)
    title = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    status = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

    def __str__(self):
        return self.employee.name

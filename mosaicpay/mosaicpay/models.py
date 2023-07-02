from django.db import models

class Test(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.name

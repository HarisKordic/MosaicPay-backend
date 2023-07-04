from django.db import models

class Test(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.name
class Person(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

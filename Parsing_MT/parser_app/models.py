from djongo import models

class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    url = models.URLField()
    source = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
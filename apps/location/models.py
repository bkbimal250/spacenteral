from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'states'
        ordering = ['name']
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cities'
        unique_together = ('name', 'state')
        indexes = [
            models.Index(fields=['name', 'state'], name='idx_city_name_state'),
        ]
        ordering = ['name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='areas', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'areas'
        unique_together = ('name', 'city')
        indexes = [
            models.Index(fields=['name', 'city'], name='idx_area_name_city'),
        ]
        ordering = ['name']
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return f"{self.name} - {self.city.name}"

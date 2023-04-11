from django.db import models


class Lottery(models.Model):
    lottery_id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/')
    max_players = models.IntegerField()
    gwei_fee = models.IntegerField()
    address = models.CharField(max_length=255, blank=True)
    creator_address = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField()

    def __str__(self):
        return self.title


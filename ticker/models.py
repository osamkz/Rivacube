from django.db import models
import datetime

# Create your models here.


class Ticker(models.Model):
    id = models.CharField("id", max_length=20, primary_key=True)
    yticker = models.CharField(
        "yticker", max_length=12, db_index=True, null=False, default="_")
    date = models.DateField("date", db_index=True,
                            null=False, default=datetime.date.today)
    px_last = models.FloatField("px_last", null=True)
    px_high = models.FloatField("px_high", null=True)
    px_low = models.FloatField("px_low", null=True)
    px_open = models.FloatField("px_open", null=True)
    px_volume = models.BigIntegerField("px_volume", null=True)

    def __str__(self) -> str:
        return "{}, {}".format(self.yticker, self.date)

    def __iter__(self) -> list:
        return iter([
            self.yticker,
            self.date,
            self.px_last,
            self.px_high,
            self.px_low,
            self.px_open,
            self.px_volume
        ])

    class Meta:
        managed = True

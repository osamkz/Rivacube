from django.db import models
import datetime

# Create your models here.


class Ticker(models.Model):
    id = models.CharField("id", max_length=20, primary_key=True)
    yticker = models.ForeignKey(
        "Lexique", db_column="yticker", on_delete=models.PROTECT)
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


class Lexique(models.Model):
    isin = models.CharField("isin", max_length=12)
    bbg_ticker = models.CharField("bbg_ticker", max_length=14)
    yf_ticker = models.CharField("yf_ticker", max_length=12, primary_key=True)
    name = models.CharField('name', max_length=100)
    sector = models.CharField('sector', max_length=32)
    gics_sub_sector = models.CharField("gics_sub_sector", max_length=100)
    id_zone = models.CharField('id_zone', max_length=2)
    country = models.CharField('country', max_length=15)
    ccy = models.CharField("ccy", max_length=3)
    no_index = models.BooleanField("no_index")
    cybersecurity = models.BooleanField("cybersecurity")
    petsfervor = models.BooleanField("petsfervor")
    biodefense = models.BooleanField("biodefense")
    adv_mat = models.BooleanField("adv_mat")
    meta = models.BooleanField("meta")
    ltp = models.BooleanField("ltp")
    market = models.CharField("market", max_length=9, default="NA")

    def __str__(self) -> str:
        return (self.yf_ticker)

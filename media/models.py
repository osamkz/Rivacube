from django.db import models

# Create your models here.

# TODO: remettre une foreign key sur reply_to_status_id
# reply_to_status_id = models.ForeignKey('self', on_delete = models.CASCADE, default = None, blank = True, null = True)
# TODO: Creer un array pour mentions_screen_name


class Media(models.Model):
    status_id = models.BigIntegerField("status_id", primary_key=True)
    user_id = models.BigIntegerField("user_id")
    created_at = models.DateTimeField("created_at")
    screen_name = models.CharField("screen_name", max_length=32)
    text = models.TextField("text")
    source = models.CharField("source", max_length=64)
    display_text_width = models.SmallIntegerField("display_text_width")
    reply_to_status_id = models.BigIntegerField(
        'reply_to_status_id', default=None, blank=True, null=True)
    reply_to_user_id = models.BigIntegerField(
        "reply_to_user_id", default=None, blank=True, null=True)
    reply_to_screen_name = models.CharField(
        "reply_to_screen_name", max_length=32, default=None, blank=True, null=True)
    is_quote = models.BooleanField("is_quote")
    is_retweet = models.BooleanField("is_retweet")
    favorite_count = models.SmallIntegerField("favorite_count")
    retweet_count = models.IntegerField("retweet_count")
    mentions_screen_name = models.CharField(
        "mentions_screen_name", max_length=1024)
    lang = models.CharField("lang", max_length=3)
    description = models.TextField("description")
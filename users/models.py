from django.db import models
from django.contrib.auth.models import AbstractUser # 장고의 user를 import

# 아래 방식은 장고의 user를 상속받지 않고 처음부터 user를 만든다는 얘기임.
# class User(models.Model):
#     pass

# 장고의 user를 상속받는 user
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male") # "DB에 들어갈 이름", "관리자 페이지에서 보이는 label"
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won" # 튜플 괄호 생략 가능
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=150,
        editable=False,
    ) # editable=False -> 해당 column 사용 X
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=True,
    ) # 역할, 방을 빌려주는 사람인지, 빌리는 사람인지, BooleanField는 non-nullable field임
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )

    def total_rooms(self):
        return self.rooms.count()

    def total_reviews(self):
        return self.reviews.count()

# Create your models here.

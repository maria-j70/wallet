from django.db import models


class ActionChoices(models.IntegerChoices):
    w2w = 0
    deposit = 1
    withdrew = 2
    wage = 3
    w2w_delay = 4

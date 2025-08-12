from django.db import models

class Case(models.Model):
    title = models.CharField(max_length=120)
    setting = models.CharField(max_length=200)
    culprit_id_hidden = models.CharField(max_length=10)  # "S3"
    difficulty = models.CharField(max_length=10, default="medium")
    num_suspects = models.PositiveSmallIntegerField(default=5)
    num_clues = models.PositiveSmallIntegerField(default=8)
    num_red_herrings = models.PositiveSmallIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Suspect(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="suspects")
    sid = models.CharField(max_length=10)  # "S1"
    name = models.CharField(max_length=60)
    bio = models.CharField(max_length=220)

class Clue(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="clues")
    cid = models.CharField(max_length=10)      # "C1"
    category = models.CharField(max_length=20) # timeline|forensic|behavioral|financial
    text = models.CharField(max_length=240)

class ClueImplication(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="implications")
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE, related_name="implicates")
    suspect_sid = models.CharField(max_length=10)  # "S1"

class RedHerring(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="red_herrings")
    rid = models.CharField(max_length=10)  # "R1"
    text = models.CharField(max_length=200)

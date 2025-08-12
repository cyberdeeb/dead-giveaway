from django.db import models
from django.core.exceptions import ValidationError


class Case(models.Model):
    """Model representing a mystery case."""
    
    # Status choices for the case
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('solved', 'Solved'),
        ('unsolved', 'Unsolved'),
        ('archived', 'Archived'),
    ]
    
    # Difficulty choices
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    seed = models.CharField(max_length=100, help_text="Random seed for case generation")
    culprit_id = models.ForeignKey('Suspect', on_delete=models.CASCADE, related_name='culprit_cases', null=True, blank=True)
    timeline = models.JSONField(default=dict, help_text="Timeline of events in JSON format")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class Suspect(models.Model):
    """Model representing a suspect in the mystery game."""

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='suspects')
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    traits = models.JSONField(default=dict, help_text="Character traits in JSON format")
    motive = models.TextField()
    is_culprit = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.case.title})"
    
class Location(models.Model):
    """Model representing a location in the mystery game."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.case.title})"

class Clue(models.Model):
    """Model representing a clue in the mystery game."""

    # Clue Category choices
    CLUE_CATEGORY_CHOICES = [
        ('timeline', 'Timeline'),
        ('forensic', 'Forensic'),
        ('behavioral', 'Behavioral'),
        ('financial', 'Financial')
    ]   

    POINTS_TO = [
        ('culprit', 'Culprit'),
        ('decoy', 'Decoy'),
        ('neutral', 'Neutral')
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='clues')
    text = models.TextField()
    category = models.CharField(max_length=50, choices=CLUE_CATEGORY_CHOICES)
    weight = models.IntegerField(default=1, help_text="Weight of the clue for scoring")
    points_to = models.CharField(max_length=10, choices=POINTS_TO)
    evidence = models.JSONField(default=dict, help_text="Evidence related to the clue in JSON format")
    is_red_herring = models.BooleanField(default=False, help_text="Indicates if the clue is a red herring")

    def __str__(self):
        return f"{self.text} ({self.case.title})"
    

class Alibi(models.Model):
    """Model representing an alibi for a suspect in the mystery game."""

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='alibis')
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, related_name='alibis')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='alibis')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    verified = models.BooleanField(default=False)
    verified_by = models.JSONField(default=dict, help_text="Verified the alibi in JSON format")

    def __str__(self):
        return f"Alibi for {self.suspect.name} ({self.start_time} - {self.end_time})"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
    

class Guess(models.Model):
    """Model representing a guess made by a player in the mystery game."""

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='guesses')
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, related_name='guesses')
    rationale = models.TextField()
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guess by user in {self.case.title}"
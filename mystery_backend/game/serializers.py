# DRF serializers for Mystery Game API
from rest_framework import serializers
from .models import Case, Clue, Suspect, RedHerring, ClueImplication


class SuspectSerializer(serializers.ModelSerializer):
    """Basic suspect info - excludes culprit identity for gameplay."""

    class Meta:
        model = Suspect
        fields = ('sid', 'name', 'bio')


class ClueSerializer(serializers.ModelSerializer):
    """Clue data with list of suspects it implicates."""
    
    # Custom field to show which suspects this clue points toward
    implicates = serializers.SerializerMethodField()

    class Meta:
        model = Clue
        fields = ('cid', 'category', 'text', 'implicates')

    def get_implicates(self, obj):
        """Return suspect IDs that this clue implicates."""
        qs = ClueImplication.objects.filter(clue=obj).values_list("suspect_sid", flat=True)
        return list(qs)


class CasePublicSerializer(serializers.ModelSerializer):
    """Public case data with nested suspects, clues, and red herrings."""
    
    # Nested serializers for related objects
    suspects = SuspectSerializer(many=True, read_only=True)
    clues = ClueSerializer(many=True, read_only=True)
    red_herrings = serializers.SerializerMethodField()
    
    class Meta:
        model = Case
        # Culprit_id_hidden intentionally excluded for game
        fields = ("id","title","setting","difficulty",
                  "num_suspects","num_clues","num_red_herrings",
                  "suspects","clues","red_herrings","created_at")
    
    def get_red_herrings(self, obj):
        """Return false clues to mislead players."""
        return list(obj.red_herrings.values("rid","text"))
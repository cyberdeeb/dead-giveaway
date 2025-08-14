from rest_framework import serializers
from .models import Case, Clue, Suspect, RedHerring, ClueImplication

class SuspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspect
        fields = ('sid', 'name', 'bio')

class ClueSerializer(serializers.ModelSerializer):
    implicates = serializers.SerializerMethodField()

    class Meta:
        model = Clue
        fields = ('cid', 'category', 'text', 'implicates')

    def get_implicates(self, obj):
        qs = ClueImplication.objects.filter(clue=obj).values_list("suspect_sid", flat=True)
        return list(qs)

class CasePublicSerializer(serializers.ModelSerializer):
    suspects = SuspectSerializer(many=True, read_only=True)
    clues = ClueSerializer(many=True, read_only=True)
    red_herrings = serializers.SerializerMethodField()
    class Meta:
        model = Case
        fields = ("id","title","setting","difficulty",
                  "num_suspects","num_clues","num_red_herrings",
                  "suspects","clues","red_herrings","created_at")
    def get_red_herrings(self, obj):
        return list(obj.red_herrings.values("rid","text"))
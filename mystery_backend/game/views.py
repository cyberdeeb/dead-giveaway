from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from .config import get_difficulty_profile
from .models import Case, Suspect, Clue, ClueImplication, RedHerring
from .serializers import CasePublicSerializer
from .utils.generate_mystery import generate_mystery_plot
from .utils.validate_mystery import validate_mystery

class CaseCreateAPIView(APIView):
    def post(self, request):
        difficulty = request.query_params.get('difficulty') or request.data.get('difficulty') or 'medium'
        diff, profile = get_difficulty_profile(difficulty)

        raw_mystery = generate_mystery_plot(difficulty=diff)

        try:
            validated_mystery = validate_mystery(raw_mystery)
        except AssertionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            case = Case.objects.create(
                title=validated_mystery.title,
                setting=validated_mystery.setting,
                culprit_id_hidden=validated_mystery.culprit_id,
                difficulty=diff,
                num_suspects=profile['num_suspects'],
                num_clues=profile['num_clues'],
                num_red_herrings=profile['num_red_herrings'],
            )

            for suspect in validated_mystery.suspects:
                Suspect.objects.create(case=case, sid=suspect.id, name=suspect.name, bio=suspect.bio)

            for clue in validated_mystery.clues:
                clue_obj = Clue.objects.create(case=case, cid=clue.id, category=clue.category, text=clue.text)
                for sid in clue.implicates:
                    ClueImplication.objects.create(case=case, clue=clue_obj, suspect_sid=sid)

            for red_herring in validated_mystery.red_herrings:
                RedHerring.objects.create(case=case, rid=red_herring.id, text=red_herring.text) 

        return Response({'id': case.id}, status=status.HTTP_201_CREATED)


class CaseDetailAPIView(APIView):
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        return Response(CasePublicSerializer(case).data)


class GuessAPIView(APIView):
    def post(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        suspect_id = request.data.get("suspect_id")
        if not suspect_id:
            return Response({"error": "suspect_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not Suspect.objects.filter(case=case, sid=suspect_id).exists():
            return Response({"error": "Invalid suspect_id"}, status=status.HTTP_400_BAD_REQUEST)

        if suspect_id == case.culprit_id_hidden:
            return Response({"answer": True}, status=status.HTTP_200_OK)
        else:
            return Response({"answer": False}, status=status.HTTP_200_OK)

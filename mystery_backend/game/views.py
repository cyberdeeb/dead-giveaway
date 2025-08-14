from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .config import get_difficulty_profile
from .models import Case, Suspect, Clue, ClueImplication, RedHerring
from .serializers import CasePublicSerializer
from .utils.generate_mystery import generate_mystery_plot
from .utils.validate_mystery import validate_mystery

# Custom throttle classes for different operations
class CaseCreateThrottle(AnonRateThrottle):
    scope = 'case_create'

class CaseViewThrottle(AnonRateThrottle):
    scope = 'case_view'

class GuessThrottle(AnonRateThrottle):
    scope = 'guess'

class CaseCreateAPIView(APIView):
    throttle_classes = [CaseCreateThrottle, UserRateThrottle]
    
    @extend_schema(
        operation_id='create_case',
        summary='Create a new mystery case',
        description='Generate a new mystery case with AI-generated suspects, clues, and red herrings.',
        parameters=[
            OpenApiParameter(
                name='difficulty',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Difficulty level for the mystery case',
                enum=['easy', 'medium', 'hard'],
                default='medium',
                required=False,
            )
        ],
        responses={
            201: {
                'description': 'Case created successfully',
                'example': {'id': 1}
            },
            400: {
                'description': 'Bad request - validation error',
                'example': {'error': 'Invalid mystery data'}
            }
        }
    )
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
    throttle_classes = [CaseViewThrottle, UserRateThrottle]
    
    @extend_schema(
        operation_id='get_case',
        summary='Get mystery case details',
        description='Retrieve details of a specific mystery case including suspects, clues, and red herrings.',
        responses={
            200: CasePublicSerializer,
            404: {
                'description': 'Case not found',
                'example': {'detail': 'Not found.'}
            }
        }
    )
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        return Response(CasePublicSerializer(case).data)


class GuessAPIView(APIView):
    throttle_classes = [GuessThrottle, UserRateThrottle]
    
    @extend_schema(
        operation_id='submit_guess',
        summary='Submit a guess for the culprit',
        description='Submit your guess for who the culprit is in the mystery case.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'suspect_id': {
                        'type': 'string',
                        'description': 'ID of the suspect you think is the culprit (e.g., "S1", "S2")'
                    }
                },
                'required': ['suspect_id'],
                'example': {'suspect_id': 'S1'}
            }
        },
        responses={
            200: {
                'description': 'Guess processed successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'correct': {
                                    'type': 'boolean',
                                    'description': 'Whether the guess was correct'
                                },
                                'message': {
                                    'type': 'string',
                                    'description': 'Response message with feedback'
                                }
                            },
                            'required': ['correct', 'message']
                        },
                        'examples': {
                            'correct_guess': {
                                'summary': 'Correct guess',
                                'value': {
                                    'correct': True,
                                    'message': 'Congratulations! You solved the mystery. S2 was indeed the culprit!'
                                }
                            },
                            'incorrect_guess': {
                                'summary': 'Incorrect guess',
                                'value': {
                                    'correct': False,
                                    'message': 'Incorrect! S1 is not the culprit. Keep investigating!'
                                }
                            }
                        }
                    }
                }
            },
            400: {
                'description': 'Bad request',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'error': {
                                    'type': 'string',
                                    'description': 'Error message'
                                }
                            },
                            'required': ['error']
                        },
                        'examples': {
                            'missing_suspect_id': {
                                'summary': 'Missing suspect_id',
                                'value': {'error': 'suspect_id is required'}
                            },
                            'invalid_suspect_id': {
                                'summary': 'Invalid suspect ID',
                                'value': {'error': 'Invalid suspect_id for this case'}
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Case not found',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'detail': {
                                    'type': 'string',
                                    'description': 'Error detail message'
                                }
                            },
                            'required': ['detail']
                        },
                        'example': {'detail': 'Not found.'}
                    }
                }
            }
        }
    )
    def post(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        suspect_id = request.data.get("suspect_id")
        
        # Validate suspect_id is provided
        if not suspect_id:
            return Response({"error": "suspect_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate suspect_id exists in this case
        if not Suspect.objects.filter(case=case, sid=suspect_id).exists():
            return Response({"error": "Invalid suspect_id for this case"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the guess is correct
        is_correct = suspect_id == case.culprit_id_hidden
        
        return Response({
            "correct": is_correct,
            "message": f"Congratulations! You solved the mystery. {suspect_id} was indeed the culprit!" if is_correct else f"Incorrect! {suspect_id} is not the culprit. Keep investigating!"
        }, status=status.HTTP_200_OK)

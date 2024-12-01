from django.shortcuts import render
from StudentQuiz.models import TestScore
import json
from Home.models import Student

def display_scores(request):
    all_scores = TestScore.objects.select_related('student').order_by('student_id', '-id')
    latest_scores = {}

    for score in all_scores:
        if score.student_id not in latest_scores:
            latest_scores[score.student_id] = score         #display the latest scores for each student

    test_scores = list(latest_scores.values())

    test_scores_json = json.dumps([{
        'student_name': score.student.full_name,        #converting to JSON
        'score': score.score,
    } for score in test_scores])
    
    context = {
        'test_scores': test_scores,
        'test_scores_json': test_scores_json,
    }
    return render(request, 'progressreport.html', context)
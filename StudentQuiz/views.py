from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.http import HttpResponseRedirect
from CounselorQuiz.models import QuizQuestion, QuizOption
from django.urls import reverse 
from .models import TestScore
from Home.decorators import student_required
from django.contrib import messages

# Create your views here.

@student_required
def QuestionView(request):
    message = None
    if request.user.is_authenticated:
      questions = QuizQuestion.objects.exclude(quizoption__isnull=True).all()         #exclude the questions that their options are null
      if not questions.exists():  # Check if the list is empty
        message = "No questions are available at the moment. Please come back later"
        questions = None
      return render(request, 'studentquiz.html', {'questions': questions, 'message': message})
    
    else:
       message = 'You must be logged in to answer questions'
       messages.error(request, message)
       return redirect(reverse('Home:login'))

@student_required
def ScoreView(request):
    if request.method=='POST':
        total_score = 0
        highest_option_score = 0

        for question, option_id in request.POST.items():
            if question.startswith('question'):  
                try:    
                  selected_option = QuizOption.objects.get(id=option_id)   #get the selected option
                  total_score += selected_option.score
                except QuizOption.DoesNotExist:
                   message = 'Error! Please retake the quiz.'
                   messages.error(request, message)
                   return redirect('StudentQuiz:quiz')

        if request.user.is_authenticated:
          student = request.user.student 
          score = TestScore.objects.create(student=student, score=total_score)      #create a test score if the user is authenticated

          for question in QuizQuestion.objects.all():
            option_score = question.quizoption_set.order_by('-score').first()
            if option_score is not None:
                highest_option_score += option_score.score        #calculate the highest option score in the form (mathematical calculation)

          interval_size = highest_option_score/3
          normal_threshold = interval_size
          high_threshold = 2*interval_size         #setting a threshold for the quiz score to determine the mental of user

          request.session['total_score'] = total_score
          request.session['high_threshold'] = high_threshold
          request.session['normal_threshold'] = normal_threshold       #store the session variables
     
          return redirect('StudentQuiz:result')
        
        else:
           message = 'You must be logged in!'
           messages.error(request, message)
           return redirect(reverse('Home:login'))
        
    else:
      total_score = request.session.get('total_score')
      high_threshold = request.session.get('high_threshold')
      normal_threshold = request.session.get('normal_threshold')      #retrieve the session variables

        # Check if the session variables exist
      if total_score is None or high_threshold is None or normal_threshold is None:
        return redirect('StudentQuiz:quiz')

      return render(request, 'studentresult.html', {'total_score': total_score, 'high_threshold': high_threshold, 'normal_threshold': normal_threshold})


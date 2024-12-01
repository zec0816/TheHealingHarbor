from django.shortcuts import render, get_object_or_404, redirect
from .models import QuizQuestion, QuizOption
from Home.decorators import counselor_required

# Create your views here.
@counselor_required
def quiz_question_list(request):
    questions = QuizQuestion.objects.all()        #get all the questions from database
    return render(request, 'quiz_question_list.html', {'questions': questions})

@counselor_required
def quiz_question_create(request):
    if request.method == 'POST':
        counselor=request.user.counselor
        question_text = request.POST['question_text']
        question = QuizQuestion.objects.create(counselor=counselor, question_text=question_text)
        option_texts = request.POST.getlist('option_text')
        scores = request.POST.getlist('score')
        for i in range(len(option_texts)):
            option_text = option_texts[i]         #array handling data
            score = scores[i]
            QuizOption.objects.create(question=question, option_text=option_text, score=score)   #create optons
        return redirect('CounselorQuiz:quiz_question_list')
    return render(request, 'quiz_question_create.html')

@counselor_required
def quiz_question_update(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)    #404 if question not found
    options = question.quizoption_set.all()
    if request.method == 'POST':
        question_text = request.POST['question_text']
        question.question_text = question_text
        question.save()                                         #updating the question
        option_ids = request.POST.getlist('option_id')
        option_texts = request.POST.getlist('option_text')
        scores = request.POST.getlist('score')

        for i in range(len(option_ids)):
            option_id = option_ids[i]
            option_text = option_texts[i]            #array handling data for options
            score = scores[i]
            option = get_object_or_404(QuizOption, id=option_id)
            option.option_text = option_text                    #Update the option text and score in the QuizOption instance
            option.score = score
            option.save()

        return redirect('CounselorQuiz:quiz_question_list')
    return render(request, 'quiz_question_update.html', {'question': question, 'options': options})

@counselor_required
def quiz_question_delete(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)   #get the id of question to be deleted or 404 if not found
    if request.method == 'POST':
        question.delete()         #delete the question
        return redirect('CounselorQuiz:quiz_question_list')
    return render(request, 'quiz_question_delete.html', {'question': question})

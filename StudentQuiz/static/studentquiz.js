// cases when user reload page
var form = document.getElementById('quiz-form');
var formDisplayed = false;

window.addEventListener('beforeunload', function(event) {
  if (formDisplayed) {
    var submitButton = form.querySelector('input[type="submit"]');
    if (!submitButton.clicked) {
      event.preventDefault();
      event.returnValue = 'Are you sure you want to leave this page? Your history will be cleared';
    }
  }
});

window.onunload = function() {
  var submitButton = form.querySelector('input[type="submit"]');
  if (!submitButton.clicked) {
    history.replaceState({}, document.title, backURL);
    window.location.href = backURL;
  }
};


// show form after clicking start button
function showForm() {
  var startQuiz = document.querySelector('.StartQuiz');
  startQuiz.style.display = 'none';
  document.querySelector(".formStart").style.display = "block";
  formDisplayed = true;
  document.getElementById("quiz-form").reset();
}

form.addEventListener('submit', function() {
  var submitButton = form.querySelector('input[type="submit"]');
  submitButton.clicked = true;
});


//if question is selected, change the background color
function clickRadio(label) {
    var radioInput = label.querySelector('input[type="radio"]');
    var questionContainer = label.closest('.QuizQuestions');
    var selectedLabels = questionContainer.querySelectorAll('.radioOptions.selected');
    selectedLabels.forEach(function(selectedLabel) {
      if (selectedLabel !== label) {
        selectedLabel.classList.remove('selected');
      }
    }
    );
     
    if (radioInput.checked) {
      label.classList.add('selected');
    } else {
      label.classList.remove('selected');
    }
}



function validateForm() {                          //makeing sure every question is answered or else display error message
      var form = document.getElementById("quiz-form");
      var quizzes = form.getElementsByClassName("QuizQuestions")
      var isValid = true;

      for (var i = 0; i < quizzes.length; i++) {
        var quiz = quizzes[i];
        var inputs = quiz.getElementsByTagName("input");
        var isOptionSelected = false;

      for (var j = 0; j < inputs.length; j++) {
        var input = inputs[j]
        if (input.type === "radio" && input.checked) {
          isOptionSelected = true;
          break;
        }
      }

      if (!isOptionSelected) {
        quiz.classList.add("unanswered");
        error.style.display = "block";
        error.scrollIntoView({ behavior: 'smooth', block: 'start' });
        isValid = false;
      } else {
      quiz.classList.remove("unanswered");
      }
    }

      if (isValid) {
        error.style.display = "none";
      }

      return isValid;
}
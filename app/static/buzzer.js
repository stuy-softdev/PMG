window.addEventListener('DOMContentLoaded', () => {

let questionDP = "";
let ind = 0;
let startTime;
let clickTime;
let displayInterval;
let buttonBuzzer = document.createElement('button');
let answerForm = document.createElement('form');


function displayquestion() {

  if (questionDQ.length !== 0) {
    //console.log("hi" + questionDQ)
    displayInterval = setInterval(displayquestionInterval, 10);

  }

}


function displayquestionInterval() {

    if (ind < questionDQ.length) {
      questionDP += questionDQ[ind];
      ind++;
      document.getElementById("demo").innerHTML = questionDP;
    }

    else{
      clearInterval(displayInterval);
      buzzer();
    }

}


function buzzer() {

  startTime = Date.now();
  buttonBuzzer.style.backgroundColor = "red";
  buttonBuzzer.innerText = "Buzzer";
  buttonBuzzer.onclick = buzzerClick;
  document.body.appendChild(buttonBuzzer);

}


function buzzerClick() {

  clickTime = Date.now() - startTime;
  document.getElementById("time").innerHTML = String(clickTime);
  if (clickTime > 1000) { // SET TO IN IF STATEMENT CHECKING IF YOU PRESSED THE BUTTON FIRST

    createanswerForm();

  }

}

function createanswerForm() {
  console.log("asd")
  console.log(answer_choices)
  console.log(answer_choices[0])
  console.log(answer_choices[1])
  console.log(typeof answer_choices === 'string');

  // Shuffling the list of answer choices using the Knuth Shuffle (reordering elements by iterating from the end and swapping each element with a random one)
  for (var i = answer_choices.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = answer_choices[i];
    answer_choices[i] = answer_choices[j];
    answer_choices[j] = tmp;
  }

  // This prevents user from submitting multiple answers
  var already_answered = false;
  var answers_div = document.getElementById("display_answer_choices");

  function disableAllAnswers() {
    var btns = answers_div.querySelectorAll("button");
    btns.forEach(function(b) { b.disabled = true; });
  }

  // Creates a submit button for each answer choice
  answer_choices.forEach(function(choice) {
    var btn = document.createElement("button");
    btn.type = "button";
    // btn.textContent = decodeHtml(ansRaw);  //DECODEHTML WILL GET RID OF THE WEIRD SYMBOLS IN THE TEXT, WE WILL DO THAT LATER
    btn.textContent = choice;
    btn.className = "w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-8 px-4 rounded-lg transition duration-200 text-center text-lg";

    // when you click one of the choices, checks if it's correct, displays message about that, and makes NEXT button clickable
    btn.onclick = function() {
      if (already_answered) return;
      already_answered = true;

      // var pickedDecoded = decodeHtml(ansRaw); //DECODEHTML WILL GET RID OF THE WEIRD SYMBOLS IN THE TEXT, WE WILL DO THAT LATER
      var pickedDecoded = choice;
      document.getElementById("user_selected_answer").value = pickedDecoded;

      if (pickedDecoded === correct_answer) {
        document.getElementById("message").textContent = "Correct";
      } else {
        document.getElementById("message").textContent =
          "Incorrect. Correct answer: " + correct_answer;
      }

      disableAllAnswers();
      var nextBtn = document.getElementById("nextBtn");
      nextBtn.disabled = false;
      nextBtn.classList.remove("bg-gray-500", "cursor-not-allowed");
      nextBtn.classList.add("bg-indigo-500", "hover:bg-indigo-600", "cursor-pointer");
    };
    console.log("hi")
    console.log(btn)
    // adds to the HTML
    answers_div.appendChild(btn);
    answers_div.appendChild(document.createTextNode(" "));
    // answers_div.innerHTML += btn
  });
  /*
  for (var i = 0; i < answer_choices.length; i++) {
    document.getElementById("display_answer_choices").innerHTML += `
      <button type="button" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-8 px-4 rounded-lg transition duration-200 text-center text-lg">` +
        answer_choices[i] +
      `</button>`
  }
  */
  /*
  answerForm.id = "ansForm";



  const formInput = document.createElement("input");
  formInput.type = "text";
  formInput.placeholder = "Answer";
  const subButton = document.createElement("button");
  subButton.type = "submit";
  subButton.textContent = "Send";
  */
  /*
  answerForm.addEventListener('submit', (event) => {
    event.preventDefault();
    checkAnswer();
  });  //i needed a way to stop everything from refreshing after form submission and appr this is the main way to keep a site from refreshing



  answerForm.appendChild(formInput);
  answerForm.appendChild(subButton);
  document.body.appendChild(answerForm);
  */

}


  function checkAnswer() {
    if (document.getElementById("ansForm").value == "correctAnswer");
      console.log("hey this is correct")
  }

displayquestion();


});

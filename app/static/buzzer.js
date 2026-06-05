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

  for (var i = 0; i < answer_choices.length; i++) {
    document.getElementById("display_answer_choices").innerHTML += `
      <button type="button" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-8 px-4 rounded-lg transition duration-200 text-center text-lg">` +
        answer_choices[i] +
      `</button>`
  }
  /*
  answerForm.id = "ansForm";



  const formInput = document.createElement("input");
  formInput.type = "text";
  formInput.placeholder = "Answer";
  const subButton = document.createElement("button");
  subButton.type = "submit";
  subButton.textContent = "Send";
  */

  answerForm.addEventListener('submit', (event) => {
    event.preventDefault();
    checkAnswer();
  });  //i needed a way to stop everything from refreshing after form submission and appr this is the main way to keep a site from refreshing



  answerForm.appendChild(formInput);
  answerForm.appendChild(subButton);
  document.body.appendChild(answerForm);


}


  function checkAnswer() {
    if (document.getElementById("ansForm").value == "correctAnswer");
      console.log("hey this is correct")
  }

displayquestion();


});

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
  
    displayInterval = setInterval(displayquestionInterval, 250);

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
  if (clickTime > 1000) {

    createanswerForm();

  }
 
}

function createanswerForm() {

  answerForm.id = "ansForm";

  const formInput = document.createElement("input");
  formInput.type = "text";
  formInput.placeholder = "Answer";
  const subButton = document.createElement("button");
  subButton.type = "submit";
  subButton.textContent = "Send";

  answerForm.addEventListener('submit', (event) => {
    event.preventDefault();
    checkAnswer();
  });  //i needed a way to stop everything from refreshing after form submission and appr this is the main way to keep a site from refreshing

  
  
  answerForm.appendChild(formInput);
  answerForm.appendChild(subButton);
  document.body.appendChild(answerForm);


}


  function checkAnswer() {
    if (document.getElementById("ansForm").value == "correctAnswer";
    
  }


displayquestion();


});

window.addEventListener("DOMContentLoaded", () => {

  

  function displayquestion(questionDQ) {

    let letter = '';
    let questionDP = '';
    
    if (questionDQ.length != 0) {
      const questionInterval = setInterval(displayquestionIV(questionDQ), 500);
    }
    
    
  }


  function displayquestionIV(questionDQ_IV) {

    letter = questionDQ_IV.slice(0, 1);
    questionDP =+ letter;
    questionDQ_IV = questionDQ_IV.replace(letter, "");
    disp(questionDP);

    if (questionDQ.length == 0) {
      clearInterval(questionInterval);
      buzzer()
    }
    
  }


  function buzzer() {

    let startTime = Date().getTime();
    
    const buzzerB = document.createElement('button');
    
    buzzerB.addEventListener('click', buzzerClick());
    
  }


  function buzzerClick() {

    let stopwatch = Date().getTime() - startTime;
    
  }
  

  
}

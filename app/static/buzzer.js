window.addEventListener("DOMContentLoaded", () => {

  

  function displayquestion(questionDQ) { //gets string "questionDQ" from HTML file (imported from SQLite to HTML by python) 

    let letter = ''; 
    let questionDP = '';
    
    if (questionDQ.length != 0) {
      const questionInterval = setInterval(displayquestionIV(questionDQ), 500);
    }
    
    
  }


  function displayquestionIV(questionDQ_IV) { //"questionDQ" will be displayed letter-by-letter, with a letter appearing each .5 seconds until the entire question has been displayed

    letter = questionDQ_IV.slice(0, 1); //a letter will be taken from "QuestionDQ", added to "QuestionDP", and promptly displayed with "QuestionDP"
    questionDP =+ letter;
    questionDQ_IV = questionDQ_IV.replace(letter, "");
    disp(questionDP);

    if (questionDQ.length == 0) {
      clearInterval(questionInterval);
      buzzer() //once the question is fully displayed, the buzzer will appear
    }
    
  }


  function buzzer() {

    let startTime = Date().getTime();
    
    const buzzerB = document.createElement('button');
    
    buzzerB.addEventListener('click', buzzerClick());
    
  }


  function buzzerClick() { //when a player clicks the buzzer, the time it took them to click the buzzer will be made into a constant to be called by HTML

    const stopwatchTime = Date().getTime()
    const stopwatch = stopwatchTime - startTime;
    
  }
  

  
}

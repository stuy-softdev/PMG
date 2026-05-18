window.addEventListener("DOMContentLoaded", () => {

  

  function displayquestion(questionDQ) {

    let letter = '';
    let questionDP = '';
    
    while (questionDQ.length != 0) {
      const questionInterval = setInterval(displayquestionIV(questionDQ), 500);
    }
    else {
      clearInterval(questionInterval);
    }
    
  }


  function displayquestionIV(questionDQ_IV) {

    letter = questionDQ_IV.slice(0, 1);
    questionDP =+ letter;
    questionDQ_IV = questionDQ_IV.replace(letter, "");
    disp(questionDP);
    
  }
  

  
}

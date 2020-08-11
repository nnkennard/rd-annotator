QUESTIONS = Array();
CURRENT_HIGHLIGHT = null;

function clean_tokens(tokens){
  clean_tokens = Array();
  for (var token of tokens) {
    if (token == "CHUNK_SEP"){
       "<br/> <br />";
    } else if (token == "COM"){ return ",";}
  else {return token;}
  }
}

function constructPage() {
  redraw();
  console.log(tokens);
}

function getHighlightOffset(text, allTokens) {
  textTokens = text.toString().split(" ");
  for (var i = 0; i < allTokens.length; i++) {
    if (allTokens.slice(i, i + textTokens.length).join(" ") == text) {
      return { start: i, exclusive_end: i + textTokens.length };
    }
  }
  return { start: -1, exclusive_end: -1 };
}

function createQuestion(text, allTokens, comment){
  highlightOffset = getHighlightOffset(text, allTokens);
  question = {start: highlightOffset.start,
             exclusive_end:highlightOffset.exclusive_end,
             comment:comment,
             text:text.toString()}
  return question;
}

function consumeSelection() {
  putativeQuestion = createQuestion(window.getSelection(), tokens, document.getElementById("questionNotes").value);
  highlightCard = document.getElementById("highlightedCardSpan");
  selectionText = window.getSelection().toString();
  confirmQuestionButton = document.getElementById("confirmQuestionButton");
  if (putativeQuestion.start == -1) {
    confirmQuestionButton.disabled = true;
    highlightCard.innerHTML = selectionText.fontcolor("red");
  } else {
    confirmQuestionButton.disabled = false;
    highlightCard.innerHTML = selectionText.fontcolor("green");
    CURRENT_QUESTION = putativeQuestion;
  }
}

function confirmQuestion() {
  questionToConfirm = CURRENT_QUESTION;
  questionToConfirm.comment = document.getElementById("questionNotes").value;
  if (questionToConfirm.start > -1) {
    console.log("Pushing new question", questionToConfirm);
    QUESTIONS.push(questionToConfirm);
  }
  redraw();
}

function deleteQuestion(questionIndex){
  console.log("Trying to delete", questionIndex);
  QUESTIONS.splice(questionIndex, 1);
  redraw();
}

function redraw(tokens) {
  tokens = JSON.parse(document.getElementById("tokens").textContent);
  questions = JSON.parse(document.getElementById("questions").textContent);

  questionsTable = document.getElementById("questionsTable");
  questionsTable.innerHTML = "";
  for (var i = 0; i < questions.length; i++) {
    question = questions[i];
    questionsTable.innerHTML +=
      `<tr> <td><button type="button" class="close" aria-label="Close" onclick="deleteQuestion(`+i+`)">
  <span aria-hidden="true">&times;</span>
</button> </td> <td>` +
      question.text + `</td> <td> ` + question.comment +` </td> </tr>`
  }
  highlightQuestions(tokens, questions);
}

function done(){
  alert(JSON.stringify(QUESTIONS));
}

function highlightQuestions(tokens, questions) {
  sorted_questions = questions.sort(function (a, b) {
    return a.start - b.start;
  });
  // Check for overlaps
  for (var i = 0; i < sorted_questions.length - 1; i++) {
    curr_question = sorted_questions[i];
    next_question = sorted_questions[i + 1];
    console.log(i, next_question.start, curr_question.end);
    if (next_question.start < curr_question.exclusive_end) {
      alert("Highlights in this example may be misleading due to overlaps");
      break;
    }
  }

  updated_tokens = Array();
  token_idx = 0;
  for (var i = 0; i < sorted_questions.length; i++) {
    curr_question = sorted_questions[i];
    console.log(i, curr_question);
    while (token_idx < curr_question.start) {
      updated_tokens.push(token_fixer(tokens[token_idx]));
      token_idx += 1;
    }
    updated_tokens.push("<mark>");
    while (token_idx < curr_question.exclusive_end) {
      updated_tokens.push(token_fixer(tokens[token_idx]));
      token_idx += 1;
    }
    updated_tokens.push("</mark>");
  }
  while (token_idx < tokens.length) {
    updated_tokens.push(token_fixer(tokens[token_idx]));
    token_idx += 1;
  }

  textCard = document.getElementById("textCard");
  textCard.innerHTML = updated_tokens.join(" ");
}



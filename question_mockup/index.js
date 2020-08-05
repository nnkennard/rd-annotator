QUESTIONS = Array();
CURRENT_HIGHLIGHT = null;

function constructPage() {
  redraw();
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

function redraw() {
  questionsTable = document.getElementById("questionsTable");
  questionsTable.innerHTML = "";
  for (var i = 0; i < QUESTIONS.length; i++) {
    question = QUESTIONS[i];
    questionsTable.innerHTML +=
      `<tr> <td><button type="button" class="close" aria-label="Close" onclick="deleteQuestion(`+i+`)">
  <span aria-hidden="true">&times;</span>
</button> </td> <td>` +
      question.text + `</td> <td> ` + question.comment +` </td> </tr>`
  }
  highlightQuestions();
}

function done(){
  alert(JSON.stringify(QUESTIONS));
}

function highlightQuestions() {
  sorted_questions = QUESTIONS.sort(function (a, b) {
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
      updated_tokens.push(tokens[token_idx]);
      token_idx += 1;
    }
    updated_tokens.push("<mark>");
    while (token_idx < curr_question.exclusive_end) {
      updated_tokens.push(tokens[token_idx]);
      token_idx += 1;
    }
    updated_tokens.push("</mark>");
  }
  while (token_idx < tokens.length) {
    updated_tokens.push(tokens[token_idx]);
    token_idx += 1;
  }

  textCard = document.getElementById("textCard");
  textCard.innerHTML = updated_tokens.join(" ");
}


tokens = [
  "Lorem",
  "ipsum",
  "dolor",
  "sit",
  "amet",
  ",",
  "consectetur",
  "adipiscing",
  "elit",
  ".",
  "Maecenas",
  "nisi",
  "lorem",
  ",",
  "semper",
  "consequat",
  "consequat",
  "id",
  ",",
  "interdum",
  "vel",
  "purus",
  ".",
  "Phasellus",
  "ipsum",
  "tortor",
  ",",
  "adipiscing",
  "nec",
  "egestas",
  "sed",
  ",",
  "rhoncus",
  "sed",
  "urna",
  ".",
  "Suspendisse",
  "ultrices",
  "neque",
  "felis",
  ".",
  "Maecenas",
  "id",
  "orci",
  "ut",
  "lectus",
  "luctus",
  "lacinia",
  "quis",
  "et",
  "mauris",
  ".",
  "Ut",
  "pretium",
  ",",
  "ipsum",
  "in",
  "hendrerit",
  "consequat",
  ",",
  "mauris",
  "lorem",
  "pulvinar",
  "nulla",
  ",",
  "vel",
  "tristique",
  "lorem",
  "ligula",
  "eget",
  "nisi",
  ".",
  "e",
  "Proin",
  "pulvinar",
  "nibh",
  "vel",
  "felis",
  "tempor",
  "eget",
  "ornare",
  "lorem",
  "egestas",
  "?",
  "Morbi",
  "molestie",
  "viverra",
  "turpis",
  ",",
  "pulvinar",
  "tristique",
  "diam",
  "mollis",
  "non",
  ".",
  "Phasellus",
  "facilisis",
  "justo",
  "a",
  "ipsum",
  "faucibus",
  "lacinia",
  ".",
  "Quisque",
  "sit",
  "amet",
  "ultrices",
  "nulla",
  "."
];




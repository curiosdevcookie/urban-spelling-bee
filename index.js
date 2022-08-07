const APIurl = 'https://api.urbandictionary.com/v0/define?term=';

const controller = new AbortController()
const signal = controller.signal

function abortFetching() {
  console.log('Now aborting');
  controller.abort()
}

function setInnerHTMLtextarea(id, APIValue) {
  const term = document.getElementById('input-word').value;
  fetchData(term);
  document.getElementById(id).innerHTML = APIValue;
  abortFetching()
}

async function fetchData(term) {
  const response = await fetch(APIurl + term, {
    method: 'get',
    signal: signal,
  });
  if (!response.ok) {
    console.log(response.status, response.statusText);
  } else {
    const {
      list: [{
        definition,
        example,
      }]
    } = await response.json();
    console.log(definition, example);

    setInnerHTMLtextarea('definition-area', definition);
    setInnerHTMLtextarea('example-area', example);
  }
}


const letter1 = document.getElementById('b1');
letter1.addEventListener('click', letterValueInput);

const letter2 = document.getElementById('b2');
letter2.addEventListener('click', letterValueInput);

const letter3 = document.getElementById('b3');
letter3.addEventListener('click', letterValueInput);

const letter4 = document.getElementById('b4');
letter4.addEventListener('click', letterValueInput);

const letter5 = document.getElementById('b5');
letter5.addEventListener('click', letterValueInput);

const letter6 = document.getElementById('b6');
letter6.addEventListener('click', letterValueInput);

const letter7 = document.getElementById('b7');
letter7.addEventListener('click', letterValueInput);

function letterValueInput() {
  const input = document.getElementById('input-word');
  input.value += this.innerText;
}

const deleteButton = document.getElementById('delete');
deleteButton.addEventListener('click', deleteLetter);

function deleteLetter() {
  const input = document.getElementById('input-word');
  input.value = input.value.slice(0, -1);
};

const buttonSubmit = document.getElementById('submit');
buttonSubmit.addEventListener('click', submitWord);

function submitWord() {
  const term = document.getElementById('input-word').value;
  fetchData(term);
}

const buttonDefinition = document.getElementById('word-definition-button');
buttonDefinition.addEventListener('click', setInnerHTMLtextarea);

const buttonExample = document.getElementById('word-example-button');
buttonExample.addEventListener('click', setInnerHTMLtextarea);
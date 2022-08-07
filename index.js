const APIurl = 'https://api.urbandictionary.com/v0/define?term=';


async function fetchData(term) {
  const response = await fetch(APIurl + term);
  if (!response.ok) {
    console.log(response.status, response.statusText);
  } else {
    const {
      list: [{
        definition
      }]
    } = await response.json();
    console.log(definition);
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
  const input = document.getElementById('inputPlaceholder');
  input.value += this.innerText;
}

const deleteButton = document.getElementById('delete');
deleteButton.addEventListener('click', deleteLetter);

function deleteLetter() {
  const input = document.getElementById('inputPlaceholder');
  input.value = input.value.slice(0, -1);
};

const buttonSubmit = document.getElementById('submit');
buttonSubmit.addEventListener('click', submitWord);

function submitWord() {
  const term = document.getElementById('inputPlaceholder').value;
  fetchData(term);
}

const buttonDefinition = document.getElementById('wordDefinition');
buttonDefinition.addEventListener('click', definitionClick);

function definitionClick() {
  const definitionWord = document.getElementById('inputPlaceholder').value;
  fetchData(definitionWord);
  const definitionArea = document.getElementById('definitionArea');
  definitionArea.innerText = `${definition}`;
};
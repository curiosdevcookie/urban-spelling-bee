


const APIurl = 'https://api.urbandictionary.com/v0/define?term=';


async function fetchData(term) {
  const response = await fetch(APIurl + term);
  if (!response.ok) {
    console.log(response.status, response.statusText);
  } else {
    const data = await response.json();
    console.log(data);
  }
}



function submitWord() {
  const term = document.getElementById('inputPlaceholder').value;
  fetchData(term);
}

const buttonSubmit = document.getElementById('submit');
buttonSubmit.addEventListener('click', submitWord);


const letter1 = document.getElementById('b1');
letter1.addEventListener('click', letterValueLetter2);

function letterValueLetter2() {
  const letter2 = document.getElementById('b2');
  letter2.value = document.getElementById('inputPlaceholder');
}
const letter2 = document.getElementById('b2').innerText;
console.log(letter2.innerText);
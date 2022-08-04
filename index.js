
const options = {
  method: 'GET',
  headers: {
    'X-RapidAPI-Key': '8ed74aaddbmsh603e89d846e3da8p12b46bjsnaf1fb978e6e1',
    'X-RapidAPI-Host': 'mashape-community-urban-dictionary.p.rapidapi.com'
  }
};

const APIurl = 'https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=';

function fetchDefinition(term) {
  return fetch(APIurl + term, options)
    .then(response => {
      return response.json();
    })
    .then(data => {
      const definition = data.definition;

      if (definition) {
        return definition;
      } else {
        return 'No definition found';
      }
    })
    .catch(err => {
      return 'Error fetching definition';
    }
    );
}

// document.selectElement('#inputPlaceholder').addEventListener('submit', function (e) {
function submit() {
  const input = document.getElementById('inputPlaceholder');
  let term = input.value;

}

  // fetch('https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=cougar', options)
  //   .then(response => response.json())
  //   .then(response => console.log(response))
  //   .catch(err => console.error(err));



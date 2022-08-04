const options = {
  method: 'GET',
  headers: {
    'X-RapidAPI-Key': '8ed74aaddbmsh603e89d846e3da8p12b46bjsnaf1fb978e6e1',
    'X-RapidAPI-Host': 'mashape-community-urban-dictionary.p.rapidapi.com'
  }
};

fetch('https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=cougar', options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));



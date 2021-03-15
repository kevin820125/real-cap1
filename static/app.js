async function showRecipe(){
    cock = document.querySelector('#cock')
    for(let i = 0 ; i < 6 ; i++){
        
        drink = await axios.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
        cockName = drink.data.drinks[0].strDrink
        cockUrl = drink.data.drinks[0].strDrinkThumb
        namediv = document.createElement('div')
        namediv.className = "col-6 col-sm-3 mx-auto"
        namediv.style = 'width: 200px;'
        photodiv = document.createElement('div')
        a = document.createElement('a')
        a.href = `/cocktail/${cockName}`
        img = document.createElement('img')
        img.src = cockUrl
        img.className =' img-fluid mx-auto'
        a.append(img)
        // console.log(a)
        namediv.append(a)
        photodiv.append(cockName)
        // console.log(namediv)
        cock.append(namediv)
        namediv.append(photodiv)

        sessionStorage.setItem(`cocktail_name${i}` , cockName)
        sessionStorage.setItem(`cock_url${i}` , cockUrl)
    }
}







function shuffle(array){
  var i = array.length,
  j = 0,
  temp;
  while (i--) {
    j = Math.floor(Math.random() * (i+1));
    // swap randomly chosen element with current element
    temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}
return array;
}



async function showSimilarCocktail(){
    type = document.querySelector('#glassType').textContent
    cock = document.querySelector('#recommanded')
    
    drink = await axios.get(`https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=${type}`)
    drinksList = drink.data.drinks
    console.log(drinksList)
    shuffle(drinksList)
    for(let i = 0 ; i < 6 ; i++){
      a = document.createElement('a')
      img = document.createElement('img')
      img.style = 'width:60px;height:60px'
      img.className = 'img-fluid mx-auto'
      div = document.createElement('div')
      div.className = 'col-6 col-sm-3 mx-auto mb-3'
      div.style = 'width: 200px;'
      img.src = drinksList[i].strDrinkThumb
      cockName = drinksList[i].strDrink
      a.href = `/cocktail/${cockName}`
      a.append(img)
      div.append(a)
      div.append(cockName)
      cock.append(div)
      // cock.append(cockName)
      // cock.append(a)
  }
}


















addToFav = document.querySelector('#favorite-cocktail')
if(addToFav){addToFav.addEventListener('click' , addfav)
cocktailId = addToFav.getAttribute('cockid')
async function addfav(evt){
    add_cock = await axios.post('/addcocktail' , {"cocktail_id" : cocktailId})
    handleResponse(add_cock)
}}




function handleResponse(resp){
  console.log(resp.data)
  btn = document.querySelector('#favorite-cocktail')
  if(resp.data === 'Unfavorited'){
    btn.classList = 'btn btn-success'
    btn.textContent = 'add to favorited'
  }
  if(resp.data === 'add to favorite'){
    btn.classList = 'btn btn-danger'
    btn.textContent = 'Unfavorited'
  }
}

















// axios.post('/addcocktail')
//   .catch(function (error) {
//     if (error.response) {
//       // The request was made and the server responded with a status code
//       // that falls out of the range of 2xx
//       console.log(error.response.data);
//       console.log(error.response.status);
//       console.log(error.response.headers);
//     } else if (error.request) {
//       // The request was made but no response was received
//       // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
//       // http.ClientRequest in node.js
//       console.log(error.request);
//     } else {
//       // Something happened in setting up the request that triggered an Error
//       console.log('Error', error.message);
//     }
//     console.log(error.config);
//   });
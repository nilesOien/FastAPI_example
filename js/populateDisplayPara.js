
// javaScript function to populate the paragraph where
// the pets that match your criteria are displayed.
// The details of the pets are obtained from the
// queryAnimals FastAPI endpoint in JSON format.


// This is a global variable so it can be referenced in other functions.
let selectedAnimals;

// Has to be an async function for the fetch() of data to work.
async function populateDisplayPara(needToSelect = false) {

 // Clear any earlier selections.
 clearSelected();

 // URL is something like :
 // /queryAnimals?minCost=5&maxCost=500&desiredType=Cat
 // Returned JSON is something like :
 // [
 //  {
 //   "animalType": "Cat",
 //   "animalBreed": "Tabby",
 //   "cost": 10,
 //   "desc": "The classic cat",
 //   "fullImage": "Tabby_full.jpg",
 //   "thumbnail": "Tabby_thumb.jpg"
 //   "numInStock": 10
 // },
 // {
 //   "animalType": "Cat",
 //   "animalBreed": "Siamese",
 //   "cost": 30,
 //   "desc": "Actual cat may not be from Siam",
 //   "fullImage": "Siamese_full.jpg",
 //   "thumbnail": "Siamese_thumb.jpg"
 //   "numInStock": 10
 //  }
 // ]

 // Assemble the URL where we get the data from the server.
 let url = "/queryAnimals"
 let sepChar="?";

 let petType = document.getElementById('petTypeSelector').value; 
 if (petType != "Any"){
  url += sepChar + "desiredType=" + petType;
  sepChar="&";
 }

 let minCost = document.getElementById('minCost').value;
 if (minCost.length > 0){
  url += sepChar + "minCost=" + minCost;
  sepChar="&";
 }

 let maxCost = document.getElementById('maxCost').value;
 if (maxCost.length > 0){
  url += sepChar + "maxCost=" + maxCost;
  sepChar="&";
 }

 // Go get the data.
 let response = await fetch(url);

 if (response.status != 200) {
  alert(response.statusText);
  return;
 }

 let data = await response.text();
 selectedAnimals=JSON.parse(data);

 // Display the data. First, the count of matching pets.
 document.getElementById('countPara').innerHTML="Found " + selectedAnimals.length + " matches."

 // Then, the table of pets that can be selected. Put together the HTML.
 let petTableHTML="";
 let needToStartRow=true;
 for(let i=0; i < selectedAnimals.length; i++){
  if (needToStartRow){
   needToStartRow=false;
   petTableHTML += "<tr>";
  }
  petTableHTML += "<td>" + selectedAnimals[i].animalBreed + " (" + selectedAnimals[i].animalType + ")<br>cost ";
  petTableHTML += selectedAnimals[i].cost + "<br>";

  // Note that the global imageURL variable below was set in the petStore.html template.
  petTableHTML += "<IMG SRC=\"" + imageURL + selectedAnimals[i].thumbnail + "\"><br>";
  petTableHTML += "<br><input type=\"button\" value=\"Select\" onClick=\"selectPet(";
  petTableHTML += i;

  petTableHTML += ");\">";

  petTableHTML += "</td>";

  if (((i+1) % 6) == 0){
   needToStartRow=true;
   petTableHTML += "</tr>";
  }

 }

 // Send the HTML to the paragraph in the document.
 document.getElementById('petTable').innerHTML=petTableHTML;

 // If a selection was already being displayed, we need to
 // update that in case the number in stock was changed.
 if (needToSelect){
  selectPet(globalIndex)
 }

 return;
}


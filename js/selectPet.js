
// Function to adjust the number in stock.
// Called by both the "Buy" and "Restock" functions.
// A quantity integer, qi, is passed in. If it's positive
// we're restocking (adding pets to the inventory), negative
// means we're buying.
//
// Function has to be async because we're going to the server for data
// with fetch(). See FastAPI_example.py for server side.
async function adjustStock(qi){

 let url='/adjustStock';

 // Assemble the JSON we want to send as part of the POST endpoint.
 let dataToSend = {
  animalType: selectedAnimals[globalIndex].animalType,
  animalBreed: selectedAnimals[globalIndex].animalBreed,
  adjustment: qi
 };

 // Assemble the headers we need for POST with JSON.
 let options = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataToSend)
 };

 // Get the status message via the POST endpoint.
 let response = await fetch(url, options );

 if (response.status != 200) {
  alert(response.statusText);
  return;
 }

 let data = await response.text();
 message=JSON.parse(data);
 // Show the message in an alert() pop up.
 alert(message.status);

 // Repopulate the display paragraph and the selected pet paragraph
 // (by passing true here).
 populateDisplayPara(true);

 return;

}

// Small function that gets the string entered
// in the quantity text box, makes sure it's an integer, and
// passes it to the adjustStock() function. We come here
// when the "restock" button is clicked.
function restock() {
 let q = document.getElementById('Quantity').value;
 if (q.length == 0){
  alert('Please enter a quantity');
  return;
 }
 let qi = parseInt(q);
 adjustStock(qi);
 return;
}

// Small funtion that gets the string entered
// in the quantity text box, makes sure it's an integer,
// negates it, and then
// passes it to the adjustStock() function. We come here
// when the "buy" button is clicked.
function buy() {
 let q = document.getElementById('Quantity').value;
 if (q.length == 0){
  alert('Please enter a quantity');
  return;
 }
 let qi = parseInt(q);
 qi = -qi;
 adjustStock(qi);
 return;
}

// Global variable
let globalIndex;

// Function called when the user selects a pet. Displays the
// selected pet in the paragraph at the bottom of the page.
function selectPet(index) {

 // Make a global copy of the index for later use.
 globalIndex=index;

 // Assemble the HTML.
 let html = "<HR>";
 html += selectedAnimals[index].animalBreed + " (" + selectedAnimals[index].animalType + ") cost : " + selectedAnimals[index].cost + "<br>";

 // Note that the global imageURL variable below was set in the petStore.html template.
 html += "<IMG SRC=\"" + imageURL + selectedAnimals[index].fullImage + "\"><br>";
 html += selectedAnimals[index].desc + "<br>";
 html += selectedAnimals[index].numInStock + " in stock<br>";
 html += "<label for=\"Quantity\">Quantity : </label>";
 html += "<input maxlength=\"5\" size=\"5\" type=\"text\" id=\"Quantity\" name=\"Quantity\"> "
 html += "<input type=\"button\" value=\"Buy\" onClick=\"buy();\"> ";
 html += "<input type=\"button\" value=\"Restock\" onClick=\"restock();\"> ";
 html += "<input type=\"button\" value=\"Clear\" onClick=\"clearSelected();\">";

 // Send the HTML to the paragraph.
 document.getElementById('selectedPara').innerHTML=html;

 return;
}


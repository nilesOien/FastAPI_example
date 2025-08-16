
// javaScript that populates the drop down menu
// of available pet types by getting the available pet
// types from the server.
//
// Has to be an async function for the fetch() of data
// from the server to work.
async function populateSelector() {

 // Get data from the server by visiting the FastAPI endpoint.
 // Reply looks something like this :
 //
 // [
 //  {
 //    "animalType": "Cat",
 //    "num": 5
 //  },
 //  {
 //    "animalType": "Dog",
 //    "num": 4
 //  }
 // ]

 let response = await fetch('/listAnimalTypes');

 if (response.status != 200) {
  alert(response.statusText);
  return;
 }

 let data = await response.text();
 let reply=JSON.parse(data);

 // OK, assemble the HTML for the drop down menu.
 let selectorHTML="";
 for(let i=0; i < reply.length; i++){
  // alert(reply[i].animalType + " (" + reply[i].num + ")");
  selectorHTML += "<option value=\"" + reply[i].animalType + "\">" + reply[i].animalType + " (" + reply[i].num + ") </option>";
 }

 // Add the "Any" option to indicate that we don't care about pet type.
 selectorHTML += "<option value=\"Any\">Any</option>";

 // Send the HTML to the document.
 document.getElementById('petTypeSelector').innerHTML=selectorHTML;

 // Populate the display paragraph where the pets are shown.
 populateDisplayPara();

 return;
}


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction(name) {
    document.getElementById(name).classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.nav-selection')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function for_checkbox_phys(){

  let div = document.getElementById('physical-person-block');
  let entity = document.getElementById('entity');
  let entity_div = document.getElementById('entity-block');

  if(this.checked){
      div.style.display = 'block';
      entity.checked = false;
      entity_div.style.display = 'none'
  }
  else
    div.style.display = 'none';
}


function for_checkbox_entity(){

  let div = document.getElementById('entity-block');
  let phys = document.getElementById('physical-person');
  let phys_div = document.getElementById('physical-person-block');

  if(this.checked){
    div.style.display = 'block';
    phys.checked = false;
    phys_div.style.display = 'none'
  }
  else
    div.style.display = 'none';
}

document.getElementById('physical-person').onchange = for_checkbox_phys
document.getElementById('entity').onchange = for_checkbox_entity
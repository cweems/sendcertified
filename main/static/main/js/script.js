var placeSearch, autocompleteFrom, autocompleteTo;
var componentForm = {
  street_number: ['id_sender_street_number', 'id_recipient_street_number', 'short_name'],
  route: ['id_sender_route', 'id_recipient_route', 'short_name'],
  locality: ['id_sender_locality', 'id_recipient_locality', 'long_name'],
  administrative_area_level_1: ['id_sender_state', 'id_recipient_state', 'short_name'],
  country: ['id_sender_country', 'id_recipient_country', 'short_name'],
  postal_code: ['id_sender_postal_code', 'id_recipient_postal_code', 'short_name']
};

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  $('#from-field').focus(function(){
    if(autocompleteFrom === undefined){
      console.log('not defined');
      autocompleteFrom = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById('from-field')),
        {types: ['geocode']});
        autocompleteFrom.addListener('place_changed', fillInFromAddress);
    }
  })

  $('#to-field').focus(function(){
    if(autocompleteTo === undefined){
      autocompleteTo = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById('to-field')),
        {types: ['geocode']});

        autocompleteTo.addListener('place_changed', fillInToAddress);
    }
  })
}

function fillInFromAddress() {
  // Get the place details from the autocompleteFrom object.
  var place = autocompleteFrom.getPlace();
  for (var component in componentForm) {
    var id = componentForm[component][0];
    document.getElementById(id).value = '';
    document.getElementById(id).disabled = false;
  }

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm.hasOwnProperty(addressType)) {
      var format = componentForm[addressType][2]
      var val = place.address_components[i][format];
      document.getElementById(componentForm[addressType][0]).value = val;
    }
  }
}

function fillInToAddress() {
  // Get the place details from the autocompleteFrom object.
  var place = autocompleteTo.getPlace();

  for (var component in componentForm) {
    var id = componentForm[component][1];
    document.getElementById(id).value = '';
    document.getElementById(id).disabled = false;
  }

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var format = componentForm[addressType][2]
      var val = place.address_components[i][format];
      document.getElementById(componentForm[addressType][1]).value = val;
    }
  }
}

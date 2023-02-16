// This sample uses the Autocomplete widget to help the user select a
// place, then it retrieves the address components associated with that
// place, and then it populates the form fields with those details.
// This sample requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script
// src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function success(position) {
    geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    moveToAddress(null) 
}

function error() {

}

function moveToAddress(title) {
    deleteMarkers();

    map.panTo(geolocation);

    marker = new google.maps.Marker({
        map: map,
        draggable: true,
        position: geolocation,
        zoom: 17,
        animation: google.maps.Animation.DROP,
        title: title,
        draggable: true 
    });

    markers.push(marker)

    google.maps.event.addListener(marker, 'dragend', function () {
        geolocation.lat = marker.getPosition().lat().toFixed(6);
        geolocation.lng = marker.getPosition().lng().toFixed(6);

        markerDragEnded();
    });

    //
    // Update hidden values
    //
    document.getElementById('latitude').value = geolocation.lat;
    document.getElementById('longitude').value = geolocation.lng;
}

function markerDragEnded() {

}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}

var placeSearch, autocomplete, geolocation, map;
var markers = [];

var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};

function initMap() {
    //
    // Initialize geolocation
    //
    geolocation = {
        lat: -12.104696,
        lng: -77.051985
    };

    //
    // Init map
    //
    map = new google.maps.Map(document.getElementById('map-container'), {
        center: geolocation,
        zoom: 17,
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    //
    // Check current location according to browser
    //
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    }

    // Create the autocomplete object, restricting the search predictions to
    // geographical location types.
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'));

    // Avoid paying for data that you don't need by restricting the set of
    // place fields that are returned to just the address components.
    autocomplete.setFields(['address_component', 'geometry']);

    // When the user selects an address from the drop-down, populate the
    // address fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    //
    // Get the place details from the autocomplete object.
    //
    var place = autocomplete.getPlace();

    //
    // Move map to new address
    //
    geolocation.lat = place.geometry.location.lat();
    geolocation.lng = place.geometry.location.lng();

    moveToAddress(null)
        
    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the place details,
    // and then fill-in the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
        }
    }
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle(
                { center: geolocation, radius: position.coords.accuracy });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}

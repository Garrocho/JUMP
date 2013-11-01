var map;

// link: https://developers.google.com/maps/documentation/javascript/geocoding?hl=pt-br

function iniciar() {
    var mapOptions = {
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    // Try HTML5 geolocation
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            var infowindow = new google.maps.Marker({
                map: map,
                position: pos,
                title: 'Você está aqui!'
            });
            map.setCenter(pos);
            obterDadosLocalizacao(pos);
        }, function() {
            handleNoGeolocation(true);
            });
    }else{
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }
}

function handleNoGeolocation(errorFlag) {
    if(errorFlag) {
        var content = 'Erro no serviço de geolocaliazção.';
    }else{
        var content = 'Seu navegador não suporta o serviço de geolocalização.';
    }

    var options = {
        map: map,
        position: new google.maps.LatLng(60, 105),
        content: content
    };
    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

function obterDadosLocalizacao(pos){
    var geocoder = new google.maps.Geocoder();
    var infowindow = new google.maps.InfoWindow();
    var marker;    
    geocoder.geocode({'latLng': pos}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[1]) {
          map.setZoom(11);
          marker = new google.maps.Marker({
              position: pos,
              map: map
          });
          infowindow.setContent(results[1].formatted_address);
          infowindow.open(map, marker);
        }
      } else {
        alert("Erro no serviço de geolocalização: " + status);
      }
    });
}

google.maps.event.addDomListener(window, 'load', iniciar);

var map;

// link: https://developers.google.com/maps/documentation/javascript/geocoding?hl=pt-br

function iniciar() {
    var cidade = obterParametroGet("localizacao");
    var mapOptions = {
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    // Try HTML5 geolocation
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position) {
           /* var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            var infowindow = new google.maps.Marker({
                map: map,
                position: pos,
                title: 'Você está aqui!'
            });
            map.setCenter(pos);
            obterDadosLocalizacao(pos);*/
            obterDadosLocalizacao(cidade);
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

function obterDadosLocalizacao(cidade){
    /*var geocoder = new google.maps.Geocoder();
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
    });*/
    var geocoder = new google.maps.Geocoder();
    var infowindow = new google.maps.InfoWindow();
    geocoder.geocode( { 'address': cidade}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
        infowindow.setContent(obterParametroGet("jogador") + ", você Está Aqui!");
        infowindow.open(map, marker);      
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });    
}

google.maps.event.addDomListener(window, 'load', iniciar);

function urlDecode(string, overwrite){
    if(!string || !string.length){
        return {};
    }
    var obj = {};
    var pairs = string.split('&');
    var pair, name, value;
    var lsRegExp = /\+/g;
    for(var i = 0, len = pairs.length; i < len; i++){
        pair = pairs[i].split('=');
        name = unescape(pair[0]);
        value = unescape(pair[1]).replace(lsRegExp, " ");
        if(overwrite !== true){
            if(typeof obj[name] == "undefined"){
                obj[name] = value;
            }else if(typeof obj[name] == "string"){
                obj[name] = [obj[name]];
                obj[name].push(value);
            }else{
                obj[name].push(value);
            }
        }else{
            obj[name] = value;
        }
    }
    return obj;
}

function obterParametroGet(param){
	var wl = window.location.href;
	var params = urlDecode(wl.substring(wl.indexOf("?")+1));
	return(params[param]);
}

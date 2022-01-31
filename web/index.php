<!DOCTYPE html>
<html>
  <head>
    <link href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>

    <title>MotMot GPS Car Tracker</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
    #overMap { 
        position: absolute; 
        bottom: 10px; 
        left: 10px; 
        z-index: 99;
        } 

    #overMapTextField { 
      position: absolute; 
      bottom: 10px; 
      right: 80px; 
      height: 55px;
      width: 130px;
      visibility: hidden;
      background-color: white;
      z-index: 99;
      } 

    #checkButton { 
      position: absolute; 
      bottom: 10px; 
      right: 10px; 
      height: 55px;
      width: 50px;
      visibility: hidden;
      background-color: white;
      z-index: 99;
    }

    #map {
        height: 100%;
    }
    
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
    }

    .mdc-top-app-bar {
        background-color: #323639;
    }

    .app-fab--absolute {
        position: fixed;
        bottom: 1rem;
        right: 1rem;
    }

    #markerLayer img {
        animation: pulse .5s infinite alternate;
        -webkit-animation: pulse .5s infinite alternate;
    }

    keyframes pulse { 
	    to { 
		    transform: scale(0.5);
		    -webkit-transform: scale(0.5);  
	    }
    } 

    @media(min-width: 1024px) {
      .app-fab--absolute {
      bottom: 1.5rem;
      right: 1.5rem;
    }

    </style>
  </head>
  <body>
    
    <header class="mdc-top-app-bar">
      <div class="mdc-top-app-bar__row">
        <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
          <a href="#" class="material-icons mdc-top-app-bar__navigation-icon">menu</a>
            <span class="mdc-top-app-bar__title">MotMot GPS Car Tracker</span>
          </section>
          <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
            <a onclick="currentLocation()" class="material-icons mdc-top-app-bar__action-item" aria-label="Current Location" alt="Current Location">gps_fixed</a>
          </section>
      </div>
    </header>
  

    <div id="map" class="map"></div>

    <div id="overMap">
      <button style="background-color:#323639" class="mdc-fab mdc-fab--extended" aria-label="History" onclick="showOverMapTextField()">
        <span class="material-icons mdc-fab__icon">history</span>
        <span class="mdc-fab__label">History</span>
      </button>
    </div>

    <div id="overMapTextField" class="mdc-text-field mdc-text-field--outlined mdc-text-field--with-trailing-icon">
      <input class="mdc-text-field__input" id="userInput">
      <div class="mdc-notched-outline">
        <div class="mdc-notched-outline__leading"></div>
        <div class="mdc-notched-outline__notch">
          <label class="mdc-floating-label">DD/MM/YYYY</label>
        </div>
        <div class="mdc-notched-outline__trailing"></div>
      </div>
    </div>

    <button id="checkButton" style="background-color:#323639" class="mdc-button mdc-button--raised" type="submit" onclick="searchDate();">check</button>

    <?php
    $file = "latlng.txt";
    $fileContent = file_get_contents($file);
    $latlng = explode(" ", $fileContent);

    /* header("Refresh:15"); */
    ?>

    <script>

      var lat = <?php echo $latlng[0] ?>;
      var lng = <?php echo $latlng[1] ?>;
      var timeV = "<?php echo $latlng[2] ?>";
      var dateV = "<?php echo $latlng[3] ?>";
      var satV = "<?php echo $latlng[4] ?>";

      function initMap() {
        // Styles a map in night mode.

        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: lat, lng: lng},
          zoom: 17,
          disableDefaultUI: true,
          styles: [
            {
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#f5f5f5"
              }
              ]
            },
            {
              "elementType": "labels.icon",
              "stylers": [
              {
                "visibility": "off"
              }
              ]
            },
            {
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#616161"
              }
              ]
            },
            {
              "elementType": "labels.text.stroke",
              "stylers": [
              {
                "color": "#f5f5f5"
              }
              ]
            },
            {
              "featureType": "administrative.land_parcel",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#bdbdbd"
              }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#eeeeee"
              }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#757575"
              }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#e5e5e5"
              }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#9e9e9e"
              }
              ]
            },
            {
              "featureType": "road",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#ffffff"
              }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#757575"
              }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#dadada"
              }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#616161"
              }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#9e9e9e"
              }
              ]
            },
            {
              "featureType": "transit.line",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#e5e5e5"
            }
            ]
            },
            {
              "featureType": "transit.station",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#eeeeee"
              }
              ]
            },
            {
              "featureType": "water",
              "elementType": "geometry",
              "stylers": [
              {
                "color": "#c9c9c9"
              }
              ]
            },
            {
              "featureType": "water",
              "elementType": "labels.text.fill",
              "stylers": [
              {
                "color": "#9e9e9e"
              }
              ]
            }
          ]
            
          
        });

        var markerImage = {
          url: 'currentLocation.svg',
          size: new google.maps.Size(185.5, 185.5),
          anchor: new google.maps.Point(92.75, 92.75),
          scaledSize: new google.maps.Size(185.5, 185.5)
        };

        marker = new google.maps.Marker({
          map: map,
          position: {lat: lat, lng: lng},
          icon: markerImage,
          optimized: false
        });

        var overlay = new google.maps.OverlayView();
        
        overlay.draw = function () {
          this.getPanes().markerLayer.id='markerLayer';
        };
        overlay.setMap(map);

        this.inner = function() {

          marker.setMap(null);

          var data = <?php echo json_encode($latlng); ?>;
          var checkDate = data.includes(document.getElementById("userInput").value);
          var dateIndex = data.indexOf(document.getElementById("userInput").value);

          var locateLat = <?php echo $latlng[0] ?>;
          var locateLng = <?php echo $latlng[1] ?>;

          var locationMarkerImage = {
            url: 'previousLocation.svg',
            size: new google.maps.Size(185.5, 185.5),
            anchor: new google.maps.Point(92.75, 92.75),
            scaledSize: new google.maps.Size(185.5, 185.5)
          };

          locationMarker = new google.maps.Marker({
            map: map,
            position: {lat: locateLat, lng: locateLng},
            icon: locationMarkerImage,
            optimized: false
          });

         overlay.setMap(map);
          
        }


      }

      function showOverMapTextField() {
        var overMapTextField = document.getElementById("overMapTextField");
        if (overMapTextField.style.visibility === "visible") {
          overMapTextField.style.visibility = "hidden";
          checkButton.style.visibility = "hidden";
        } else {
          overMapTextField.style.visibility = "visible";
          checkButton.style.visibility = "visible";
        }
      }

      function searchDate() {

        var initMapObject = new initMap();

        initMapObject.inner();

      }

      function currentLocation() {
        initMap();
      }

    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB3erFGWrzEQ3W9hRAoX4tX17v9WqH6B8A&callback=initMap" sync defer></script>
  </body>
</html>

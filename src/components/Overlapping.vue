<template>
<div>
<div class="main-div">
<div style="width: 100%;">
  <div class="MapView">
    <GmapMap
        ref="mapRef"
        :center=centreLocation
        :zoom="10"
        map-type-id="terrain"
        style="width: 100%; height: 450px"
    >
    <GmapMarker
        :key="index"
        v-for="(m, index) in markers"
        :position="m"
        :clickable="true"
        :draggable="false"
        v-bind:icon="getMarkerIcon(index)"
        @click="markerZoom(m ,index)"
    />
    <GmapMarker
        :position="centreLocation"
        :clickable="true"
        :draggable="false"
        icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        @click="markerZoom(m)"
    />
    <GmapMarker
        :position="locationOne"
        :clickable="true"
        :draggable="false"
        icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        @click="markerZoom(m)"
    />
    <GmapMarker
        :position="locationTwo"
        :clickable="true"
        :draggable="false"
        icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
        @click="markerZoom(m)"
    />
    </GmapMap>
    <div class="container">
        <h3 style="margin: 10px; text-align: center;">Find spots that are within two separate location lockdown radiuses</h3>
    <div class="row">
      <div style="width: 100%">
          
        <div class="card " style="border: none;">
          <div class="card-body">
            <form v-on:submit.prevent="createGeocoder()">  
            <div class="form-label-group" style="margin-bottom: 10px;">
            <input v-model="inputAddressOne" type="text" id="inputLocation" class="form-control" placeholder="Enter the first location" style="margin-bottom: 10px" required>
            <input v-model="inputAddressTwo" type="text" id="inputLocation" class="form-control" placeholder="Enter the second location" style="margin-bottom: 10px" required>
            </div>
            <button @click="createGeocoder()" class="btn btn-lg btn-primary btn-block text-uppercase" type="submit">
            <span v-if="!loading">Find spots</span>
            <span
                v-else
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
            ></span>
            </button>
            </form>
            <div style="display: relative; margin-top: 10px;">
                <p v-if="error == true" class="text-danger" style="text-align: center;">{{errorText}}</p>
                <p class="lead" style="text-align: center;">All skatespot data sourced from www.skateboard.com.au</p>
                <h6 v-if="markers.length > 0" style="text-align: center;">Click a marker to see more info about a spot.</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
  
  
</div>
<div v-if="activeIndex != null" class="spot-div">
    <b-card @click="markerZoom(markers[activeIndex], activeIndex)" v-bind:img-src="markers[activeIndex].img" img-alt="Card image" img-top embed-responsive embed-responsive-16by9>
        <h5>{{markers[activeIndex].name}}</h5>
        <p>{{markers[activeIndex].address}}</p>
        <a class="card-link" style="color: black; text-decoration: underline;" v-bind:href="markers[activeIndex].link">{{markers[activeIndex].link}}</a>
    </b-card>
</div>

</div>
<div v-if="markers.length > 0" style="width: 100%; margin: 20px;">
      <h4 style="margin-bottom: 20px;">All spots within 5km:</h4>
       <div class="list-group" style="margin-top: 0px;">
          <a v-for="(marker, index) in markers" :key="index" v-bind:class="{active: (activeIndex == index)}" @click="markerZoom(marker, index)" class="list-group-item list-group-item-action flex-column align-items-start">
            <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-1"> {{marker.name}} </h5>
            </div>
            <p class="mb-1"> {{marker.address}} </p> 
            <a class="card-link" style="color: black; text-decoration: underline;" v-bind:href="marker.link">{{marker.link}}</a>
          </a>
        </div>
</div>
</div>
</template>
<script>
import {gmapApi} from 'vue2-google-maps';
import {Client, Status} from "@googlemaps/google-maps-services-js";
import axios from 'axios';
import spotJSON from '../assets/spots.json'
import getDistance from 'geolib/es/getDistance';

export default {
    name: "MapView",
    data: function() {
        return {
            centreLocation: {lat: -37.8136, lng: 144.9631}, // Default to centre of Melbourne
            locationOne: {lat: -37.8136, lng: 144.9631},
            locationTwo: {lat: -37.8136, lng: 144.9631},
            markers: [],
            address: '',
            loading: false,
            inputAddressOne: '',
            inputAddressTwo: '',
            latLng: null,
            lockdownRadiusOne: null,
            lockDownRadiusTwo: null,
            spots: spotJSON,
            activeIndex: null,
            loading: false,
            error: false,
            errorText: "Error: Could not identify location.",
            radiusMarkers: []
        }
    },
    computed: {
        google: gmapApi
    },
    methods: {
        storeResults(coordinates) {
            this.latLng = coordinates;
        },
        getAddress() {
            var address = ''
            this.loading = true;
        },
        panToLocation(coordinates) {
            this.$refs.mapRef.$mapPromise.then((map) => {
                map.panTo(coordinates)
            })
        },
        createRadius(location) {
            this.$refs.mapRef.$mapPromise.then((map) => {
                const radiusRef = new this.google.maps.Circle({
                    strokeColor: "#4da6ff",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#4da6ff",
                    fillOpacity: 0.35,
                    map,
                    center: location,
                    radius: 5000
                })
                this.radiusMarkers.push(radiusRef);
            }) 
        },
        loadSpots(locationOne, locationTwo) {
            this.markers = [];
            for (var i = 0; i < this.spots.length; i++ ) {
                var coordObject = {latitude: this.spots[i]['lat'], longitude: this.spots[i]['lng']}
                var distance1 = getDistance(coordObject, locationOne)
                var distance2 = getDistance(coordObject, locationTwo)
                if ((distance1 < 5000) && (distance2 < 5000)) {
                    this.markers.push(this.spots[i])
                }
            }
            // Get midpoint
            var lat = (locationOne['lat'] + locationTwo['lat']) / 2
            var lng = (locationOne['lng'] + locationTwo['lng']) / 2
            this.panToLocation({lat: lat, lng: lng})
            console.log(this.markers)
        },
        markerZoom(position, index) {
            this.activeIndex = index 
            this.$refs.mapRef.$mapPromise.then((map) => {
                map.panTo(position);
                map.setZoom(13);

            })
        },
        getMarkerIcon(index) {
            if (index == this.activeIndex) {
                return "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            } else {
                return "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
            }
        },
        async createGeocoder() { 
            this.loading = true;
            this.error = false;
            this.activeIndex = null;
            this.markers.length = 0;
            // Address One
            this.$refs.mapRef.$mapPromise.then((map) => {
                // Clear previous radii
                for (var i=0; i < this.radiusMarkers.length; i++) {
                    this.radiusMarkers[i].setMap(null)
                }

                var geocoder = new this.google.maps.Geocoder()
                const geoResponse = geocoder.geocode({'address': this.inputAddressOne}, (results, status) => {
                    if (status == 'OK') {
                        this.locationOne = {lat: results[0].geometry.location.lat(), lng: results[0].geometry.location.lng()} // Get coordinates
                        this.createRadius(this.locationOne)
                    } else {
                        this.error = true;
                        this.errorText = "Error: Could not identify location.";
                        this.markers = [];
                        this.centreLocation = {lat: -37.8136, lng: 144.9631}; // Default back to centre of Melbourne
                        this.panToLocation(this.centreLocation);
                        map.setZoom(10);
                    }
                
                
                })
                const geoResponse2 = geocoder.geocode({'address': this.inputAddressTwo}, (results, status) => {
                    if (status == 'OK') {
                        this.locationTwo = {lat: results[0].geometry.location.lat(), lng: results[0].geometry.location.lng()} // Get coordinates
                        this.createRadius(this.locationTwo)
                        map.setZoom(12);
                        this.loadSpots(this.locationOne, this.locationTwo)
                    } else {
                        this.error = true;
                        this.errorText = "Error: Could not identify location.";
                        this.markers = [];
                        this.centreLocation = {lat: -37.8136, lng: 144.9631}; // Default back to centre of Melbourne
                        this.panToLocation(this.centreLocation);
                        map.setZoom(10);
                    }
                    
                })
            var locations = [this.locationOne, this.locationTwo]
            
            //
            
            this.loading = false;
            })
            // Address Two
            
        },
    },
    mounted () {
    // At this point, the child GmapMap has been mounted, but
    // its map has not been initialized.
    // Therefore we need to write mapRef.$mapPromise.then(() => ...)
    this.$refs.mapRef.$mapPromise.then((map) => {
      map.panTo(this.centreLocation)
      //this.loadSpots({latitude: -37.8954254, longitude: 145.2743309})
    })
    
  },
  created() {
      
  }
}
</script>

<style>
.card-img-top {
    height: 60vh;
    object-fit: cover;
}
.main-div {
    display: flex;
}
.spot-div {
    width: 40%; 
    margin-left: 20px;
    margin-right: 20px; 
    margin-bottom: 20px;
}
@media only screen and (max-width: 480px) {
    .main-div {
        flex-wrap: wrap;
    }
    .spot-div {
        width: 100%; 
        margin-left: 20px;
        margin-right: 20px; 
        margin-bottom: 20px;
    }
}
</style>
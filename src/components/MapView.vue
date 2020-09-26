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
    </GmapMap>
    <div class="container">
    <div class="row">
      <div style="width: 100%">
        <div class="card " style="border: none;">
          <div class="card-body">
            <form v-on:submit.prevent="createGeocoder()">
            <div class="form-label-group" style="margin-bottom: 10px;">
            <input v-model="inputAddress" type="text" id="inputLocation" class="form-control" placeholder="Enter a location to show spots within 5km" required>
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
                <p class="lead" style="text-align: center;">All skatespot data sourced from www.skateboard.com.au</p>
                <h6 v-if="markers.length > 0" style="display: absolute; left: 50%; top: 50%; text-align: center;">Click a marker to see more info about a spot.</h6>
                <p v-if="error == true" style="text-align: center;" class="text-danger">Error: Could not identify location.</p>
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
        <a class="card-link" style="color: black; text-decoration: underline;" v-bind:href="'https://www.google.com/maps/dir/'+markers[activeIndex].lat+','+markers[activeIndex].lng">Get Directions</a>
        <br>
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
import AWS from 'aws-sdk';

export default {
    name: "MapView",
    data: function() {
        return {
            centreLocation: {lat: -37.8136, lng: 144.9631}, // Default to centre of Melbourne
            markers: [],
            address: '',
            loading: false,
            inputAddress: '',
            latLng: null,
            lockdownRadius: null,
            spots: spotJSON,
            activeIndex: null,
            loading: false,
            error: false
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
                map.panTo(this.centreLocation)
            })
        },
        createRadius(location) {
            this.$refs.mapRef.$mapPromise.then((map) => {
                //map.panTo(this.centreLocation)
                if (this.lockdownRadius != null) {
                    this.lockdownRadius.setMap(null)
                }
                this.lockdownRadius = new this.google.maps.Circle({
                    strokeColor: "#4da6ff",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: "#4da6ff",
                    fillOpacity: 0.35,
                    map,
                    center: location,
                    radius: 5000
                })
            })
        },
        loadSpots(location) {
            this.markers = [];
            for (var i = 0; i < this.spots.length; i++ ) {
                var coordObject = {latitude: this.spots[i]['lat'], longitude: this.spots[i]['lng']}
                var distance = getDistance(coordObject, location)
                if (distance < 5000) {
                    this.markers.push(this.spots[i])
                }
                    
            }
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
            this.$refs.mapRef.$mapPromise.then((map) => {
                var geocoder = new this.google.maps.Geocoder()
                const geoResponse = geocoder.geocode({'address': this.inputAddress}, (results, status) => {
                if (status == 'OK') {
                    console.log(results)
                    this.centreLocation = {lat: results[0].geometry.location.lat(), lng: results[0].geometry.location.lng()} // Get coordinates
                    console.log(this.centreLocation)
                    this.panToLocation(this.centreLocation);
                    map.setZoom(12);
                    this.loadSpots(this.centreLocation);
                    this.createRadius(this.centreLocation);
                } else {
                    this.error = true;
                    this.lockdownRadius.setMap(null);
                    this.markers = [];
                    this.centreLocation = {lat: -37.8136, lng: 144.9631}; // Default back to centre of Melbourne
                    this.panToLocation(this.centreLocation);
                    map.setZoom(10);
                }
                this.loading = false;
            })
            })
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
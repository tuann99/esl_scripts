// Reqyirements:
// 1. Node.js
// 2. Express.js
// 3. CORS
// 4. jquery
// 5. turf.js
// 6. leaflet.js
// 7. bootstrap

// import modules
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const path = require('path');
const fetch = require('node-fetch');
const turf = require('@turf/turf');
const L = require('leaflet');

function determineZone(latitude, longitude) {
    var point = turf.point([longitude, latitude]);
    zone_150_coordinates = zone_150m.features.geometry.coordinates[0];
    console.log(zone_150_coordinates.head(5));
    const zone_150_poly = turf.polygon([zone_150_coordinates]);

    if (turf.booleanPointInPolygon(point, zone_150_poly)) {
        return '150m';
    } else {
        return 'Outside of defined zones';
    }};

function addMarker(address, latitude, longitude, status) {
    var marker = L.marker([latitude, longitude]).addTo(map_b050d8bf79c9302e69199415b6cac5ef);
    marker.bindPopup('Address: '+ address + '<br>Latitude: ' + latitude + '<br>Longitude: ' + longitude + '<br>Within any zones: ' + status).openPopup();
}

function geocodeAddress(address) {
    const rawAddress = address;
    var formattedAddress = address.replace(/ /g, '+');
    console.log(formattedAddress);

    // https://cors-anywhere.herokuapp.com/
    var url = `http://localhost:8080/https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=${formattedAddress}&benchmark=2020&format=json&key=78b4381afeb5c414911e858cb258011f812052f3`;
    // var url = `http://localhost:3000/?address=${formattedAddress}&benchmark=2020&format=json&key=78b4381afeb5c414911e858cb258011f812052f3`;
    console.log(url);
    
    // 1441 Sunnyside Ave Flint MI 48503
    const getJSON = async url => {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = response.json();
            return data;
        } catch (error) {
            console.error('Catch Error:', error);
        }
    };

    console.log("Fetching data from census API...")
    
    getJSON(url).then(data => {
        if (data.result.addressMatches.length > 0) {
            console.log("Data fetched successfully, and matches found for the address");
            const longitude = data.result.addressMatches[0].coordinates.x;
            const latitude = data.result.addressMatches[0].coordinates.y;

            console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
            let point = turf.point([longitude, latitude]);
            // console.log(Object.keys(zone_150m));
            // console.log(Object.keys(zone_150m.features[0]));
            
            var firstFeature = zone_150m.features[0];
            var zone_150_coordinates = firstFeature.geometry.coordinates;
            let polygon = turf.polygon(zone_150_coordinates);
            console.log(zone_150_coordinates);
            let isInside = turf.booleanPointInPolygon(point, polygon);
            console.log(isInside);

            addMarker(rawAddress, latitude, longitude, isInside);
            // var zone_150_coordinates = zone_150m.features.geometry.coordinates[0];
            // console.log(zone_150_coordinates);
            
            // var zone = determineZone(latitude, longitude);
            // addMarker(latitude, longitude);
            
            // document.getElementById('result').innerHTML += '<tr><td>' + address + '</td><td>' + zone + '</td></tr>';
        } else {
            alert('No matches found for this address');
        }
    });
}

function searchAddress() {
    var address = document.getElementById('address').value;
    geocodeAddress(address);
}
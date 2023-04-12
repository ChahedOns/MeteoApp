<template>
  <div>
    <div class="button-container">
      <button class="button-temp" @click="toggleTemperatureMap">Toggle Temperature Map</button>
      <button class="button-rain" @click="toggleRainMap">Toggle Rain Map</button>
    </div>
    <div ref="mapContainer" style="height: 400px; width: 400px;"></div>
  </div>
</template>
<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet/dist/images/marker-icon.png';
import 'leaflet/dist/images/marker-icon-2x.png';
import 'leaflet/dist/images/marker-shadow.png';

export default {
  name: 'TemperatureMap',
  data() {
    return {
      map: null,
      temperatureLayer: null,
      temperatureLayerVisible: false,
      rainLayerVisible: false,
      apiKey: 'e1d249091bc4e5afc3580b698bdecc7c',
    };
  },
  mounted() {
    this.map = L.map(this.$refs.mapContainer).setView([48.856613, 2.352222], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(this.map);

    this.temperatureLayer = L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${this.apiKey}`, {
      attribution: '&copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    });
    this.rainLayer = L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${this.apiKey}`, {
      attribution: '&copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    });

    // Create a marker at the specified location

    const marker = L.marker([48.856613, 2.352222], {
      icon: L.icon({
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41]
      })
    }).addTo(this.map);

    // Add a popup to the marker
    marker.bindPopup("<b>Hello !</b><br>You are currently here :D").openPopup();
  },
  methods: {
    toggleTemperatureMap() {
      if (this.temperatureLayerVisible) {
        this.map.removeLayer(this.temperatureLayer);
      } else {
        this.map.addLayer(this.temperatureLayer);
        this.map.removeLayer(this.rainLayer);
      }
      this.temperatureLayerVisible = !this.temperatureLayerVisible;
    },
    toggleRainMap() {
      if (this.temperatureLayerVisible) {
        this.map.removeLayer(this.rainLayer);
      } else {
        this.map.addLayer(this.rainLayer);
        this.map.removeLayer(this.temperatureLayer);
      }
      this.temperatureLayerVisible = !this.temperatureLayerVisible;
    },
  },
};
</script>
<style scoped>
.button-container {
  display: flex;
  justify-content: center;
  margin-bottom: 7px;
}

.button-temp {
  background-color: #FF5733;
  border: none;
  color: white;

  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
}
.button-rain {
  background-color: #00BFFF;
  border: none;
  color: white;

  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 5px;
}
</style>
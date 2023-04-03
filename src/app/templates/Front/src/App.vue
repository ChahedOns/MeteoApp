<template>
  <div id="app" class="app">
    <transition name="fade" mode="out-in" appear>
      <div class="card">
        <WeatherSearch />
        <WeatherMain />
        <WeatherInfo />
        <WeekChart :forecastData="getForecastData"/>
      </div>
    </transition>
    <WeatherAnimate />
    <div class="footer-text">
      <button>Log In</button>
      <button>Sign up !</button>
    </div>
  </div>
</template>

<script>

import WeatherSearch from "@/components/WeatherSearch";
import WeatherMain from "@/components/WeatherMain";
import WeatherInfo from "@/components/WeatherInfo";
import WeatherAnimate from "@/components/WeatherAnimate";
import { mapGetters, mapActions } from "vuex";
import WeekChart from "@/components/WeekChart";
export default {
  name: "App",
  components: {
    WeekChart,
    WeatherSearch,
    WeatherMain,
    WeatherInfo,
    WeatherAnimate,
  },
  computed: {
    ...mapGetters(["isSearched", "getForecastData"])
  },
  methods: {
    ...mapActions(["fetchWeatherData","fetchForecastData"]),
    async initData() {
       await this.fetchWeatherData(this.$store.state.defaultSearch);
       await this.fetchForecastData(this.$store.state.defaultSearch);
    },
  },
  created() {
    this.initData();
  }
};
</script>

<style lang="less">
@import url("https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,700;0,800;0,900;1,300;1,500&display=swap");
:root {
  --cardWidth: 360px;
  --darkColor: #666;
  --grayColor: #999;
  --cardBgColor: #f1f1f1;
  --cloudAnimateTime: 150s;
  --clearAnimationTime: 120s;
  --snowAnimateTime: 15s;
  --rainAnimateTime: 70s;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Jost", sans-serif;
}
body {
  background-color: fade(#000, 30);
  overflow: hidden;
}
.app {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.card {
  max-width: var(--cardWidth);
  width: 100%;
  padding: 40px;
  margin: 20px;
  border-radius: 20px;
  box-shadow: 0 0 70px fade(black, 30);
  z-index: 9999;
  background-color: var(--cardBgColor);

  @media (max-height: 767px) {
    padding: 30px;
  }
}

@media (max-width: 480px) {
  .card {
    padding: 30px;
  }
}

.footer-text {
  position: absolute;
  bottom: 50px;
  left: 0;
  right: 0;
  margin: auto;
  text-align: center;
  button {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    margin: 0 10px;
    cursor: pointer;
    font-size: 16px;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
    &:hover {
      background-color: #388e3c;
    }
  }
}
</style>

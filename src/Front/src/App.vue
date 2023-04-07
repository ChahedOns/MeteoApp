<template>
  <div id="app" class="app">
    <transition name="fade" mode="out-in" appear>
      <div class="card">
        <WeatherSearch />
        <WeatherMain />
        <WeatherInfo />
        <WeekChart :forecastData="getForecastData"/>
        <button  @click="toggleLoginSignupModal">Login / Sign Up</button>
      </div>
    </transition>
    <transition name="fade" mode="out-in">
      <div v-if="showLoginSignup" class="modal-wrapper">
        <div class="modal-backdrop" @click="toggleLoginSignupModal"></div>
        <div class="modal-content">
          <LoginSignup />
          <button @click="toggleLoginSignupModal">Close</button>
        </div>
      </div>
    </transition>
    <WeatherAnimate />
  </div>
</template>

<script>

import WeatherSearch from "@/components/WeatherSearch";
import WeatherMain from "@/components/WeatherMain";
import WeatherInfo from "@/components/WeatherInfo";
import WeatherAnimate from "@/components/WeatherAnimate";
import { mapGetters, mapActions } from "vuex";
import WeekChart from "@/components/WeekChart";
import LoginSignup from "@/components/LoginSignup";
export default {
  name: "App",
  components: {
    WeekChart,
    WeatherSearch,
    WeatherMain,
    WeatherInfo,
    WeatherAnimate,
    LoginSignup
  },
  data() {
    return {
      showLoginSignup: false,
      showButton: true
    };
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
    toggleLoginSignupModal() {
      this.showLoginSignup = !this.showLoginSignup;
      this.showButton = false;
    }
  },

  created() {
    this.initData();
  }
};
</script>

<style lang="less">
@import url("https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,700;0,800;0,900;1,300;1,500&display=swap");
:root {
  --cardWidth: 725px;
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
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
}

.modal-content {
  position: relative;
  z-index: 1;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
}

button {
  padding: 10px;
  margin: 10px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  background-color: var(--darkColor);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease-in-out;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
  }
}

</style>
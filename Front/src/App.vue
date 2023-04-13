<template>
  <div id="app" class="app">
    <transition name="fade" mode="out-in" appear>
      <div class="card">
        <WeatherSearch />
        <div class="history-stuff" v-if="isLoggedIn" @click="toggleHistoryModal">Check your history here !</div>
        <div class="history-stuff"  @click="toggleMapModal">Check your weather map here !</div>
        <transition name="fade" mode="out-in">
          <div v-if="showMap" class="modal-wrapper">
            <div class="modal-backdrop" @click="toggleMapModal"></div>
            <div class="modal-content">
              <WeatherMap />
            </div>
          </div>
        </transition>
        <WeatherMain />
        <WeatherInfo />
        <WeekChart :forecastData="getForecastData"/>


        <div class="button-container">
          <button v-if="!isLoggedIn " @click="toggleLoginModal" class="login">Log In</button>
          <button v-if="!isLoggedIn " @click="toggleSignupModal" class="signup">Sign Up</button>
          <button v-if="isLoggedIn " @click="logout">Log Out</button>
        </div>

      </div>
    </transition>
    <transition name="fade" mode="out-in">
      <div v-if="showLogin" class="modal-wrapper">
        <div class="modal-backdrop" @click="toggleLoginModal"></div>
        <div class="modal-content">
          <LogIn :isLoggedIn="isLoggedIn" @close="handleCloseLogInModal" @login-status-changed="isLoggedIn = $event"  @login-failed="isLoggedIn = false"/>
        </div>
      </div>
    </transition>

    <transition name="fade" mode="out-in">
      <div v-if="showSignup" class="modal-wrapper">
        <div class="modal-backdrop" @click="toggleSignupModal"></div>
        <div class="modal-content">
          <SignUp  @close="handleCloseSignUpModal"/>
        </div>
      </div>
    </transition>
    <transition name="fade" mode="out-in">
      <div v-if="showHistory" class="modal-wrapper">
        <div class="modal-backdrop" @click="toggleHistoryModal"></div>
        <div class="modal-content">
          <HistoryData />
        </div>
      </div>
    </transition>
    <NotIfs v-if="isLoggedIn"/>

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

import LogIn from "@/components/LogIn";
import SignUp from "@/components/SignUp";
import axios from "axios";
import NotIfs from "@/components/NotIfs";
import HistoryData from "@/components/HistoryData";
import WeatherMap from "@/components/WeatherMap";



export default {
  name: "App",
  components: {
    WeekChart,
    WeatherSearch,
    WeatherMain,
    WeatherInfo,
    WeatherAnimate,
    LogIn,
    SignUp,
    NotIfs,
    HistoryData,
    WeatherMap


  },
  data() {
    return {
      showSignup: false,
      showLogin: false,
      showButton: true,
      isLoggedIn: false,
      showHistory: false,
      showMap: false
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

    toggleLoginModal(){
      this.showLogin = !this.showLogin;
      this.showButton = false;
    },
    toggleMapModal(){
      this.showMap = !this.showMap;
      this.showButton = false;
    },

    toggleSignupModal(){
      this.showSignup = !this.showSignup;
      this.showButton = false;
    },
    toggleHistoryModal() {
      this.showHistory = !this.showHistory;
      this.showButton = false;
    },
    handleCloseLogInModal() {
      this.showLogin = false;
      this.showButton = true;
    },
    handleCloseSignUpModal() {
      this.showSignup = false;
      this.showButton = true;
    },
    logout() {
      axios.post('http://127.0.0.1:5000/logout')
          .then(response => {
            // Handle successful logout
            localStorage.removeItem('token');
            this.isLoggedIn = false;
            this.responseMessage = response.data;
            console.log(response.data);
          })
          .catch(error => {
            // Handle logout error
            console.error(error);
            this.responseMessage = error.response.data
          });
    },



  },

  created() {
    const token = localStorage.getItem('token');
    if (token) {
      this.isLoggedIn = true;
    }
    this.initData();
  }
};
</script>
<style lang="less">
@import url("https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,700;0,800;0,900;1,300;1,500&display=swap");
:root {
  --cardWidth: 725px;
  --cardHeight: 825px;
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
.history-stuff {
  display: inline-block;
  text-decoration: none;
  border-bottom: 2px solid #000;
  border-color: #00ADEF;
  cursor: pointer;
  text-align: center;
  width: 225px;
  margin-left: 32.5%;
  margin-top: 15px;
}

.history-stuff:hover {
  background-color: #00ADEF;
  color: #fff;
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
  overflow-y: auto;
}

.card {
  max-width: var(--cardWidth);
  max-height: var(--cardHeight);
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
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #3e8e41;
}

button:focus {
  outline: none;
  box-shadow: 0 0 0 2px #ddd;
}


button.login, button.signup {
  background-color: #2196F3;
}

button.login:hover, button.signup:hover {
  background-color: #0b7dda;
}
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}


</style>
import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    apiBase: "https://api.openweathermap.org/data/2.5/",
    apiKey: "e1d249091bc4e5afc3580b698bdecc7c",
    defaultSearch: "Tunis",
    search: "",
    isError: false,
    weatherData: {},
    forecastData: [],
  },
  getters: {
    getWeatherMain(state) {
      const { temp, feelsLike, description, icon, info } = state.weatherData;
      return {
        temp,
        feelsLike,
        description,
        info,
        icon,
      };
    },
    getWeatherInfo(state) {
      const { wind, clouds, humidity } = state.weatherData;
      return {
        wind,
        clouds,
        humidity,
      };
    },
    getWeatherCountry(state) {
      return state.weatherData.country;
    },
    getForecastData(state) {
      return state.forecastData.map(forecast => ({
        temp: forecast.temp,
        date: forecast.date
      }));
    },
    isSearched(state) {
      return state.search !== "";
    },
    getError(state) {
      return state.isError;
    },
  },
  mutations: {
    ["SET_SEARCH"](state, search) {
      state.search = search.toLowerCase();
    },
    ["SET_WEATHER_DATA"](state, data) {
      state.weatherData = data;
    },
    ["SET_ERROR"](state, value) {
      state.isError = value;
    },
    ["SET_FORECAST_DATA"](state, data) {
      state.forecastData = data;
    },
  },
  actions: {
    //rnrn
    async fetchWeatherData({ commit, state }, search) {
      try {
        commit("SET_SEARCH", search);
        const response = await axios.get(
            `${state.apiBase}weather?q=${search}&units=metric&APPID=${state.apiKey}`
        );
        const newWeatherData = {
          name: response.data.name,
          temp: response.data.main.temp,
          tempMin: response.data.main.temp_min,
          tempMax: response.data.main.temp_max,
          feelsLike: response.data.main.feels_like,
          description: response.data.weather[0].description,
          icon: response.data.weather[0].icon.substring(0, 2),
          info: response.data.weather[0].main,
          wind: response.data.wind.speed,
          humidity: response.data.main.humidity,
          clouds: response.data.clouds.all,
          country: response.data.sys.country,
        };

        commit("SET_WEATHER_DATA", newWeatherData);
        commit("SET_ERROR", false);
      } catch (error) {
        console.log(error);
        commit("SET_ERROR", true);
        commit("SET_WEATHER_DATA", {});
      }
    },
    //prévision
    async fetchForecastData({ commit, state }, search) {
      try {
        commit("SET_SEARCH", search);
        const response = await axios.get(
            `${state.apiBase}forecast?q=${search}&units=metric&APPID=${state.apiKey}`
        );
        const forecastData = [];
        const forecastList = response.data.list;

        for (let i = 0; i < forecastList.length; i += 8) {
          const forecast = forecastList[i];
          forecastData.push({
            date: forecast.dt_txt,
            temp: forecast.main.temp,
            tempMin: forecast.main.temp_min,
            tempMax: forecast.main.temp_max,
            feelsLike: forecast.main.feels_like,
            description: forecast.weather[0].description,
            icon: forecast.weather[0].icon.substring(0, 2),
            info: forecast.weather[0].main,
            wind: forecast.wind.speed,
            humidity: forecast.main.humidity,
            clouds: forecast.clouds.all,
          });
        }

        commit("SET_FORECAST_DATA", forecastData);
        commit("SET_ERROR", false);
      } catch (error) {
        console.log(error);
        commit("SET_ERROR", true);
        commit("SET_FORECAST_DATA", []);
      }
    },
  },
});

export default store;

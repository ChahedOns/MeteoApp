<template>
  <div class="weather-search">
    <input
        type="text"
        placeholder="Search City"
        class="search-control"
        v-model.trim="search"
        @keyup.enter="getData"
    />
    <span class="country" v-if="isSearched">({{getWeatherCountry}})</span>
    <div class="error" v-if="getError">No results found! fix it try again.</div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import axios from "axios";
export default {
  data() {
    return {
      search: this.$store.state.search
    };
  },
  computed: {
    ...mapGetters(["isSearched", "getWeatherCountry", "getError"])
  },
  methods: {
    ...mapActions(["fetchWeatherData", "fetchForecastData"]),
    getData() {
      this.fetchWeatherData(this.search);
      this.fetchForecastData(this.search);
      //Search thang
      axios.post('http://127.0.0.1:5000/weather', {
        city: this.search,
        user_id: localStorage.getItem('user_id')
      })
          .then(response => {
            console.log(response.data)
          })
          .catch(error => {
            console.log(error.response.data)
          })

    }
  },

};
</script>

<style lang="less" scoped>
.weather-search {
  position: relative;
  padding-left: 23%;
  .search-control {
    width: 70%;
    height: 50px;
    border: 2px solid fade(black, 10);
    border-radius: 100px;
    outline: none;
    background-color: transparent;
    font-size: 16px;
    padding-left: 20px;
    padding-right: 25px;
    transition: all 0.4s;
    &::placeholder {
      color: fade(black, 60);
    }
    &:focus {
      background-color: #fff;
      box-shadow: 0 8px 16px fade(black, 25);
      border-color: fade(black, 5);
      font-weight: 600;
      &::placeholder {
        font-weight: 400;
      }
    }
  }
  .error {
    position: absolute;
    color: red;
    text-align: center;
    bottom: -35px;
    left: 0;
    right: 0;
    margin: auto;
    font-size: 14px;
  }
  .country {
    position: relative;
    top: 50%;
    right: 40px;
    transform: translateY(-50%);
    color: var(--grayColor);
  }
}
</style>
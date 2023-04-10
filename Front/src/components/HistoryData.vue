<template>
  <div class="container">
    <form class="form" v-on:submit.prevent="getCountryHistory">
      <label for="city" class="form-label">Please search a city or click on the button below to get all your history !</label>
      <div class="form-input-group">
        <input type="text" v-model="city" id="city" name="city" class="form-input" required>
        <button type="submit" class="form-button">Get History</button>
      </div>
    </form>
    <div class="list-container">
      <ul class="list">
        <li v-if="response.length === 0 && getCountryHistoryCalled" class="list-item no-data-message">
          You haven't searched this city yet !
        </li>
        <li v-if="response.length === 0 && getAllHistoryCalled " class="list-item no-data-message">
          You haven't searched anything so far :(
        </li>
        <li v-for="item in response" :key="item.id" class="list-item">
          <div class="list-item-city">{{ item.city }}</div>
          <div class="list-item-data">{{ item.data.main.temp }}°C</div>
          <div class="list-item-date">{{ formatDate(item.date) }}</div>
        </li>
      </ul>
    </div>
    <button class="button" @click="getAllHistory">Get All History</button>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment'

export default {
  data() {
    return {
      city: '',
      response: [],
      getCountryHistoryCalled: false,
      getAllHistoryCalled: false
    };
  },
  methods: {
    getCountryHistory() {
      axios.post('http://127.0.0.1:5000/historique', {
        user_id: localStorage.getItem('user_id'),
        city: this.city
      })
          .then(response => {
            console.log(response.data);
            this.response = response.data;
            this.getCountryHistoryCalled = true
            this.getAllHistoryCalled = false
          })
          .catch(error => {
            console.error('Error:', error);
          });
    },
    async getAllHistory() {
      try {
        const userId = localStorage.getItem('user_id'); // Get user ID from local storage
        const response = await axios.get('http://127.0.0.1:5000/historique', {
          params: {
            user_id:  userId
          }
        });
        this.response = response.data;
        this.getCountryHistoryCalled = true
        this.getAllHistoryCalled = false

      } catch (error) {
        console.log(error);
      }
    },
    formatDate(date) {
      if (!date) {
        return "";
      }

      // convert to CET timezone
      const dateTime = moment.utc(date).utcOffset("+01:00");

      // format the date
      return dateTime.format("DD/MM/YY HH:mm");
    }
  }
};
</script>
<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.form {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  max-width: 275px;
  font-weight: bold;
  color: #333;
  font-size: 16px;
}

.form-input-group {
  display: flex;
  align-items: center;
}

.form-input {
  flex: 1;
  margin-right: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 1rem;
}

.form-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 3px;
  background-color: #007aff;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  display: none;
}

.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 3px;
  background-color: #007aff;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 65px;
  margin-top: 20px;
}

.list-container {
  max-height: 300px; /* Set a fixed height for the container */
  overflow-y: auto; /* Add scrolling to the container */
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.list-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 3px;
  background-color: #fae2ff;
  color: #514949;
}

.list-item-city {
  flex: 1;
  margin-right: 0.5rem;
  font-weight: bold;
}

.list-item-data {
  margin-right: 0.5rem;
  color: #7676c8;
}

.list-item-date {
  color: #999999;
  font-size: 0.8rem;
}
.list-item.no-data-message {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80px;
  border: none;
  color: #721c24;
  font-weight: bold;
}
</style>
<template>
  <div>
    <form v-on:submit.prevent="getCountryHistory">
      <label for="city">City:</label>
      <input type="text" v-model="city" id="city" name="city" required>
      <button type="submit">Get History</button>
    </form>
    <button @click="getAllHistory">Get All History</button>
    <ul>
      <li v-for="item in response" :key="item.id">
        {{ item.city }} - {{ item.data.main.temp}}°C - {{formatDate(item.date)}}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment'

export default {
  data() {
    return {
      city: '',
      response: []
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
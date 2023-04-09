<template>
  <div>
    <form v-on:submit.prevent="getHistory">
      <label for="city">City:</label>
      <input type="text" v-model="city" id="city" name="city" required>
      <button type="submit">Get History</button>
    </form>
    <ul>
      <li v-for="item in response" :key="item.id">
        {{ item.city }} - {{ item.data.main.temp}}°C - {{item.date}}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      city: '',
      response: []
    };
  },
  methods: {
    getHistory() {
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
    }
  }
};
</script>
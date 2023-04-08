<template>
  <div class="notifications">
    <div class="notification-bell" @click="getNotifications">
      <span class="notification-count">{{ notificationCount }}</span>
    </div>
    <ul class="notification-list">
      <li v-for="notification in notifications" :key="notification.id">
        {{ notification.message }}
      </li>
    </ul>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "NotIfs",
  data() {
    return {
      notifications: [],
      notificationCount: 0
    };
  },
  methods: {
    async getNotifications() {
      try {
        const userId = localStorage.getItem('user_id'); // Get user ID from local storage
        const response = await axios.get('http://127.0.0.1:5000/notifications', {
          params: {
            user_id:  userId
          }
        });
        this.notifications = response.data;
        this.notificationCount = this.notifications.length;
      } catch (error) {
        console.log(error);
      }
    }
  }
};
</script>
<style scoped>
.notifications {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.notification-bell {
  position: relative;
  width: 40px;
  height: 40px;
  background-color: #fff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.notification-count {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: red;
  color: #fff;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.notification-list {
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  padding: 10px;
  width: 300px;
  list-style: none;
  display: none;
}

.notification-list li {
  margin-bottom: 10px;
}

.notifications:hover .notification-list {
  display: block;
}
</style>
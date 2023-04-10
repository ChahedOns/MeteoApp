<template>
  <div class="notifications">
    <div class="notification-bell" @click="getNotifications">
      <span class="notification-count">{{ notificationCount }}</span>
    </div>
    <transition name="fade">
      <ul class="notification-list" v-if="notifications.length">
        <div class="notification-title">Here are your notifications for today!</div>
        <li v-for="notification in notifications" :key="notification.id">
          <div class="notification-item">
            <h2 class="location">{{ notification.location }}:</h2>
            <span class="message">{{notification.message}}</span>
          </div>
        </li>
      </ul>
    </transition>
  </div>
</template>




<script>
import axios from "axios";

export default {
  name: "NotIfs",
  data() {
    return {
      notifications: {},
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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
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
  transition: all 0.3s ease;
}
.notification-bell:hover {
  transform: scale(1.2);
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
  border-radius: 5px;
}

.notification-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.notification-item .location {
  color: #E843A0; /* dark gray */
  font-size: 18px;
  text-align: justify;
  margin: 0;
}

.notification-item .message {
  color: #2C2C2C; /* gray */
  font-size: 18px;
  margin: 0;
}

.notifications:hover .notification-list {
  display: block;
}

.notification-bell:before {
  content: "\f0f3"; /* bell icon */
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  font-size: 20px;
  color: #3b3b3b; /* dark gray */
}

.notification-title {
  text-align: center;
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #EC1F65; /* dark gray */
}
</style>

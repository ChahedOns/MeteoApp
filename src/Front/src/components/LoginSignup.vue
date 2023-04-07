<template>
  <div>
    <button v-if="!isLoggedIn && !showLoginModal && !showSignupModal" @click="showLoginModal = true">Log In</button>
    <button v-if="!isLoggedIn && !showLoginModal && !showSignupModal" @click="showSignupModal = true">Sign Up</button>
    <button v-if="isLoggedIn" @click="logout">Logout</button>

    <!-- Login Modal -->
    <div v-if="showLoginModal" class="modal">
      <div class="modal-content">
        <h2>Log In</h2>
        <form>
          <div>
            <label for="login-email">Email:</label>
            <input type="email" id="login-email" name="mail" required>
          </div>
          <div>
            <label for="login-password">Password:</label>
            <input type="password" id="login-password" name="pwd" required>
          </div>
          <div>
            <button type="submit" @click.prevent="login">Log In</button>
            <button @click="showLoginModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Signup Modal -->
    <div v-if="showSignupModal" class="modal">
      <div class="modal-content">
        <h2>Sign Up</h2>
        <form>
          <div>
            <label for="signup-email">Email:</label>
            <input type="email" id="signup-email" name="mail" required>
          </div>
          <div>
            <label for="signup-password">Password:</label>
            <input type="password" id="signup-password" name="pwd" required>
          </div>
          <div>
            <label for="signup-birth-date">Birth Date:</label>
            <input type="date" id="signup-birth-date" name="birth-date" required>
          </div>
          <div>
            <label for="signup-name">Name:</label>
            <input type="text" id="signup-name" name="name" required>
          </div>
          <div>
            <label for="signup-location">Location:</label>
            <input type="text" id="signup-location" name="location" required>
          </div>
          <div>
            <button type="submit" @click.prevent="signup">Sign Up</button>
            <button @click="showSignupModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const { localStorage } = window;

export default {
  data() {
    return {
      isLoggedIn: false,
      showLoginModal: false,
      showSignupModal: false
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      this.isLoggedIn = true;
    }
  },
  methods: {
    login(event) {
      const formData = new FormData(event.target);
      axios.post('http://127.0.0.1:5000/login', formData)
          .then(response => {
            // Handle successful login
            console.log(response.data);
            localStorage.setItem('token', response.data.token);
            this.isLoggedIn = true;
            this.showLoginModal = false;
            event.target.reset();
            // User info
            axios.get('http://127.0.0.1:5000/profile')
                .then(response => {
                  console.log(response.data);
                })
                .catch(error => {
                  console.log(error);
                });
          })
          .catch(error => {
            // Handle login error
            console.error(error);
          });
    },
    signup(event) {
      const formData = new FormData(event.target);
      axios.post('http://127.0.0.1:5000/register', formData)
          .then(response => {
            // Handle successful signup
            localStorage.setItem('token', response.data.token);
            this.isLoggedIn = true;
            this.showSignupModal = false;
            console.log(response.data);
          })
          .catch(error => {
            // Handle signup error
            console.error(error);
          });
    },
    logout() {
      axios.post('http://127.0.0.1:5000/logout')
          .then(response => {
            // Handle successful logout
            localStorage.removeItem('token');
            this.isLoggedIn = false;
            console.log(response.data);
          })
          .catch(error => {
            // Handle logout error
            console.error(error);
          });
    },
  }
}
</script>
<template>
  <!-- Login Modal -->
  <div v-if="showLoginModal" class="modal">
    <div class="modal-content">
      <h2 v-if="!isLoggedIn">Log In</h2>
      <form ref="loginForm" id="login-form" v-if="!isLoggedIn">
        <div>
          <label for="login-email">Email:</label>
          <input type="email" id="login-email" name="mail" required>
        </div>
        <div>
          <label for="login-password">Password:</label>
          <input type="password" id="login-password" name="pwd" required>
        </div>
        <div>
          <div>
            <p v-if="responseMessage" class="error-message">{{responseMessage}}</p>
          </div>
          <button type="submit" @click.prevent="login" class="btn-primary">Log In</button>
          <button @click.prevent="closeModal" class="btn-secondary">Cancel</button>
        </div>
      </form>
      <div v-if="isLoggedIn">
        <p class="welcome-message">Welcome, you have successfully logged in!</p>
        <button @click.prevent="closeModal" class="btn-secondary">Close</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import Vue from "vue";
const { localStorage } = window;

export default {
  data() {
    return {
      isLoggedIn: false,
      showLoginModal: true,
      responseMessage: null,
      showSuccessMessage: false
    }
  },

  methods: {
    login() {
      const formData = new FormData(document.getElementById('login-form'));
      axios.post('http://127.0.0.1:5000/login', formData)
          .then(response => {
            // Handle successful login
            console.log(response.data);
            localStorage.setItem('token', response.data.token);
            this.isLoggedIn = !!response.data.token;
            console.log('Before setting isLoggedIn:', this.isLoggedIn);
            this.responseMessage = response.data;
            console.log(this.responseMessage)
            if (response.status === 200) {
              this.isLoggedIn = true;
              this.$refs.loginForm.reset();
              this.responseMessage = response.data;
              this.showSuccessMessage = true;
              this.$emit('login-status-changed', true);
            }
            console.log(this.isLoggedIn);
          })
          .catch(error => {
            // Handle login error
            console.error(error);
            console.log(this.isLoggedIn);
            this.responseMessage = error.response.data
            this.isLoggedIn = false;

            Vue.nextTick(() => {
              this.$emit('login-failed', false);
            });
          });
    },
    closeModal() {
      this.showLoginModal = false;
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.modal input[type='email'],
.modal input[type='password']{
  width: 100%;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border-radius: 0.25rem;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

.modal button[type='submit'] {
  background: #007aff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  margin-right: 1rem;
}

.modal button[type='submit']:hover {
  background: #006ae6;
}

.modal button[type='button'] {
  background: white;
  color: #007aff;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: 1px solid #007aff;
  cursor: pointer;
}

.modal button[type='button']:hover {
  background: #007aff;
  color: white;
}

.modal label {
  display: block;
  text-align: left;
}

.modal div {
  margin-bottom: 1rem;
}

.modal h2 {
  margin-top: 0;
}
.btn-primary {
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  margin-right: 1rem;
}

.btn-primary:hover {
  background-color: #006ae6;
}

.btn-secondary {
  background-color: white;
  color: #007aff;
  border: 1px solid #007aff;
  border-radius: 0.25rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
}

.btn-secondary:hover {
  background-color: #007aff;
  color: white;
}

/* Welcome message styles */
.modal p.welcome-message {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007aff;
  margin: 1rem 0;
  text-align: center;
  text-transform: uppercase;
}
.error-message {
  color: red;
  font-weight: bold;
}

</style>
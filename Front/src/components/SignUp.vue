<template>
  <div class="modal">
    <div v-if="showSignupModal" class="modal-content">
      <h2>Sign Up</h2>
      <form ref="singupForm" id="signup-form" v-if="!isLoggedIn">
        <div>
          <label for="signup-email">Email:</label>
          <input type="email" id="signup-email" name="mail" required>
        </div>
        <div>
          <label for="signup-name">Name:</label>
          <input type="text" id="signup-name" name="name" required>
        </div>
        <div>
          <label for="signup-password">Password:</label>
          <input type="password" id="signup-password" name="pwd" required>
        </div>
        <div>
          <label for="signup-birth_date">Birth Date:</label>
          <input type="date" id="signup-birth_date" name="birth_date" required>
        </div>
        <div>
          <label for="signup-location">Location:</label>
          <input type="text" id="signup-location" name="location" required>
        </div>
        <div>
          <label for="signup-cities">Cities (separated by a colon ':'):</label>
          <input type="text" id="signup-cities" name="cities" required>
        </div>
        <div>
          <p v-if="responseMessage" class="error-message">{{responseMessage}}</p>
        </div>
        <div>
          <button type="submit" @click.prevent="signup" class="btn-primary">Sign Up</button>
          <button @click.prevent="closeModal" class="btn-secondary">Cancel</button>
        </div>
      </form>
      <div v-if="isLoggedIn">
        <p class="welcome-message">Welcome aboard, You have successfully Signed In !</p>
        <button @click.prevent="closeModal" class="btn-secondary">Close</button>
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
      showSignupModal: true,
      responseMessage: null
    }
  },
  methods: {
    signup() {
      const formData = new FormData(document.getElementById('signup-form'));
      axios.post('http://127.0.0.1:5000/register', formData)
          .then(response => {
            // Handle successful signup
            localStorage.setItem('token', response.data.token);
            this.responseMessage = response.data;
            if(response.status === 200) {
              this.isLoggedIn = true;
              console.log(response.data);
              this.responseMessage = response.data;
            }
          })
          .catch(error => {
            // Handle signup error
            console.error(error);
            this.responseMessage = error.response.data
          });
    },
    closeModal() {
      this.showSignupModal = false;
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
.modal input[type='text'],
.modal input[type='password'],
.modal input[type='date'] {
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

.modal div.response {
  margin-top: 1rem;
  color: red;
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
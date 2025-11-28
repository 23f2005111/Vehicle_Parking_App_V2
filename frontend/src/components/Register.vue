<template>
  <div class="register-container">
    
    <!-- Success/Error Message -->
    <div v-if="message" class="alert" :class="messageType">
      {{ message }}
    </div>

    <!-- Register Form -->
    <div class="register-box">
      <h3>Register</h3>
      
      <form @submit.prevent="registerUser">
        
        <div class="mb-3">
          <label>Email</label>
          <input type="email" v-model="email" placeholder="Enter Email" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="Enter Password" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Username</label>
          <input type="text" v-model="username" placeholder="Enter Username"  class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Address</label>
          <input type="text" v-model="address" placeholder="Enter Address" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Pincode</label>
          <input type="text" v-model="pincode" placeholder="Enter Pincode" class="form-control" maxlength="6" required>
        </div>

        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>

      <div class="mt-3 text-center">
        <router-link to="/login">Already have an account? Login</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  
  data() {
    return {
      // Form fields
      email: '',
      password: '',
      username: '',
      address: '',
      pincode: '',
      
      // Message display
      message: '',
      messageType: ''
    };
  },
  
  methods: {
    registerUser() {
      // Call backend API
      axios.post('http://localhost:5000/register', {
        email: this.email,
        password: this.password,
        username: this.username,
        address: this.address,
        pincode: this.pincode
      })
      .then((response) => {
        // Success! Show success message
        this.message = response.data.message;
        this.messageType = 'alert-success';
        
        // Redirect to login after 2 seconds
        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);
      })
      .catch((error) => {
        // Error! Show error message
        this.message = error.response.data.message;
        this.messageType = 'alert-danger';
      });
    }
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  min-width: 300px;
  padding: 15px;
  border-radius: 5px;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.register-box {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 450px;
}

h3 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-control {
  border-radius: 5px;
  padding: 10px;
}

.btn-primary {
  background: #667eea;
  border: none;
  padding: 12px;
  font-weight: 600;
  border-radius: 5px;
}

.btn-primary:hover {
  background: #764ba2;
}

a {
  color: #667eea;
  text-decoration: none;
}

a:hover {
  color: #764ba2;
}
</style>
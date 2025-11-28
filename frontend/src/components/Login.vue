<template>
  <div class="login-page">
    
    <!-- Success/Error Message -->
    <div v-if="message" class="alert" :class="messageType">
      {{ message }}
    </div>

    <!-- Login Form -->
    <div class="login-container">
      <h3 class="text-center mb-3">Park It Up Login</h3>
      
      <form @submit.prevent="loginUser">
        
        <div class="mb-3">
          <label><b>Login as:</b></label>
          <select v-model="role" class="form-select" required>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div class="mb-3">
          <label><b>Email:</b></label>
          <input type="email" v-model="email" class="form-control" placeholder="Enter Email" required>
        </div>

        <div class="mb-3">
          <label><b>Username:</b></label>
          <input type="text" v-model="username" class="form-control" placeholder="Enter Username" required>
        </div>

        <div class="mb-3">
          <label><b>Password:</b></label>
          <input type="password" v-model="password" class="form-control" placeholder="Enter password" required>
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>

      <div class="text-center mt-3">
        <router-link to="/register">Create a new account</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  
  data() {
    return {
      // Form fields
      role: 'user',
      email:'',
      username: '',
      password: '',
      
      // Message display
      message: '',
      messageType: ''
    };
  },
  
  methods: {
    loginUser() {
      // Call backend API
      axios.post('http://localhost:5000/login', {
        role: this.role,
        email: this.email,
        username: this.username,
        password: this.password
      })
      .then((response) => {
        // Success! Store the JWT token
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('role', response.data.role);
        localStorage.setItem('user_id', response.data.user_id);
        localStorage.setItem('username', response.data.username);
        localStorage.setItem('email',response.data.email)
        
        // Show success message
        this.message = response.data.message;
        this.messageType = 'alert-success';
        
        // Redirect based on role
        setTimeout(() => {
          if (response.data.role === 'admin') {
            this.$router.push('/admin');
          } else {
            this.$router.push(`/user/${response.data.user_id}`);
          }
        }, 1000);
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
.login-page {
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

.login-container {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h3 {
  color: #333;
  font-weight: 600;
}

label {
  color: #555;
}

.form-select,
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
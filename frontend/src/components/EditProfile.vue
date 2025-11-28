
<template>
  <div class="edit-profile-page">
    
    <div class="form-container">
      <h4 class="mb-4 text-primary">Edit Profile</h4>
      
      <form @submit.prevent="updateProfile">
        
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" v-model="username" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <input type="text" v-model="address" class="form-control">
        </div>

        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input type="text" v-model="pincode" class="form-control" maxlength="6">
        </div>

        <div class="mb-3">
          <label class="form-label">Email (cannot change)</label>
          <input type="email" class="form-control" :value="email" disabled>
        </div>

        <div class="d-flex justify-content-between">
          <router-link :to="`/user/${userId}`" class="btn btn-secondary">Cancel</router-link>
          <button type="submit" class="btn btn-primary">Update</button>
        </div>
        
      </form>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditProfile',
  
  data() {
    return {
      userId: null,
      username: '',
      email: '',
      address: '',
      pincode: ''
    };
  },
  
  created() {
    // Get user ID from route
    this.userId = this.$route.params.id;
    
    // Fetch user details
    this.fetchUserDetails();
  },
  
  methods: {
    fetchUserDetails() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to get user details
      axios.get(`http://localhost:5000/user/edit/${this.userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Fill form with existing data
        this.username = response.data.username;
        this.email = response.data.email;
        this.address = response.data.address;
        this.pincode = response.data.pincode;
      })
      .catch((error) => {
        console.error('Error fetching user details:', error);
        alert('Failed to fetch user details');
      });
    },
    
    updateProfile() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to update profile
      axios.post(`http://localhost:5000/user/edit/${this.userId}`, {
        username: this.username,
        address: this.address,
        pincode: this.pincode
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Update localStorage with new username
        localStorage.setItem('username', this.username);
        
        // Success! Show message and redirect
        alert(response.data.message);
        this.$router.push(`/user/${this.userId}`);
      })
      .catch((error) => {
        // Error! Show error message
        alert(error.response?.data?.message || 'Failed to update profile');
        console.error(error);
      });
    }
  }
};
</script>

<style scoped>
.edit-profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.edit-profile-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
  pointer-events: none;
}

.form-container {
  max-width: 550px;
  width: 100%;
  background: white;
  padding: 50px 40px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 1;
}

/* Decorative top bar */
.form-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 0 0 4px 4px;
}

h4 {
  text-align: center;
  font-weight: 600;
  margin-bottom: 35px;
  color: #1a1a1a;
  font-size: 1.8rem;
}

.text-primary {
  color: #1a1a1a !important;
}

.mb-3 {
  margin-bottom: 25px;
}

.form-label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 0.95rem;
  display: block;
}

.form-control {
  border-radius: 8px;
  border: 1.5px solid #d1d5db;
  padding: 12px 16px;
  font-size: 1rem;
  color: #1a1a1a;
  background: white;
  transition: all 0.2s;
  width: 100%;
}

.form-control:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
  color: #6b7280;
  border-color: #e5e7eb;
}

.d-flex {
  display: flex;
  margin-top: 35px;
  gap: 15px;
}

.justify-content-between {
  justify-content: space-between;
}

.btn-primary,
.btn-secondary {
  padding: 13px 32px;
  font-weight: 600;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  flex: 1;
}

.btn-primary {
  background: #667eea;
  color: white;
  border: none;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #374151;
}

/* Responsive */
@media (max-width: 768px) {
  .form-container {
    padding: 40px 25px;
  }
  
  h4 {
    font-size: 1.5rem;
  }

  .d-flex {
    flex-direction: column-reverse;
  }
}
</style>
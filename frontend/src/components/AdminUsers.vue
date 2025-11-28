<template>
  <div class="admin-users-page">
    
    <!-- Header -->
    <header>
      <div class="left-nav">
        <div class="left">Welcome Admin</div>
        <nav>
          | <router-link to="/admin">Home</router-link> |
          <router-link to="/admin/users">Users</router-link> |
          <router-link to="/admin/summary">Summary</router-link> |
        </nav>
      </div>
      <div class="right">
        <a @click="logout" href="#">Logout</a>
      </div>
    </header>

    <!-- Users Table -->
    <div class="container">
      <h3 class="text-center mb-4 text-primary">Registered Users</h3>

      <div v-if="users.length > 0">
        <table class="table table-bordered table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Address</th>
              <th>Pincode</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.address }}</td>
              <td>{{ user.pincode }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="alert alert-warning text-center">
        No users registered yet.
      </div>

      <div class="text-center mt-4">
        <router-link to="/admin" class="btn btn-secondary">Back to Dashboard</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminUsers',
  
  data() {
    return {
      users: []  // Store all users here
    };
  },
  
  created() {
    // When component loads, fetch users
    this.fetchUsers();
  },
  
  methods: {
    fetchUsers() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API
      axios.get('http://localhost:5000/admin/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Store users data
        this.users = response.data.users;
      })
      .catch((error) => {
        console.error('Error fetching users:', error);
        alert('Failed to fetch users');
      });
    },
    
    logout() {
      // Clear all stored data
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      
      // Redirect to login page
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.admin-users-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  padding-bottom: 50px;
}

/* Subtle pattern overlay */
.admin-users-page::before {
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

header {
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.left-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.left {
  font-weight: bold;
  font-size: 1.1rem;
}

nav a {
  color: white;
  text-decoration: none;
  margin: 0 5px;
  transition: opacity 0.2s;
}

nav a:hover {
  opacity: 0.8;
}

.right a {
  color: white;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  transition: all 0.2s;
}

.right a:hover {
  background: rgba(255, 255, 255, 0.3);
}

.container {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

h3 {
  font-weight: 600;
  color: #1a1a1a;
  background: white;
  padding: 20px;
  border-radius: 10px 10px 0 0;
  margin-bottom: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.text-primary {
  color: #1a1a1a !important;
}

.mb-4 {
  margin-bottom: 0 !important;
}

.table {
  background: white;
  border-radius: 0 0 10px 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 30px;
}

.table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.table th {
  padding: 15px;
  font-weight: 600;
  border: none;
}

.table td {
  padding: 15px;
  vertical-align: middle;
  color: #1a1a1a;
  border-color: #e5e7eb;
}

.table tbody tr {
  transition: background-color 0.2s;
}

.table tbody tr:hover {
  background-color: #f9fafb;
}

.table-bordered {
  border: none;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.02);
}

.alert-warning {
  background: white;
  border: none;
  color: #1a1a1a;
  padding: 30px;
  border-radius: 10px;
  font-size: 1.1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 30px;
}

.btn-secondary {
  background: white;
  border: none;
  padding: 12px 35px;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  color: #667eea;
  display: inline-block;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 20px 10px;
  }
  
  .table {
    font-size: 0.85rem;
  }
  
  header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
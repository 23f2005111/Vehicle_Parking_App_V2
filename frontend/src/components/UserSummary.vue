<template>
  <div class="user-summary-page">
    
    <!-- Header -->
    <header>
      <div class="left-nav">
        <div class="left">Welcome {{ username }}</div>
        <nav>
          | <router-link :to="`/user/${userId}`">Home</router-link> |
          <router-link :to="`/user/summary/${userId}`">Summary</router-link> |
          <a @click="logout" href="#">Logout</a> |
        </nav>
      </div>
      <div class="right">
        <router-link :to="`/user/edit/${userId}`">Edit Profile</router-link>
      </div>
    </header>

    <div class="container mt-4">
      <h2 class="text-center mb-4">User Summary Dashboard</h2>

      <!-- Stats Boxes -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="stat-box bg1">Total Reservations: {{ totalReservations }}</div>
        </div>
        <div class="col-md-6">
          <div class="stat-box bg2">Total Spent: ₹{{ totalSpent }}</div>
        </div>
      </div>

      <!-- Chart -->
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h5 class="text-center mb-3">Bookings Per Lot</h5>
          <canvas id="usageChart"></canvas>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'UserSummary',
  
  data() {
    return {
      userId: null,
      username: '',
      totalReservations: 0,
      totalSpent: 0,
      usageData: []
    };
  },
  
  created() {
    // Get user ID from route
    this.userId = this.$route.params.id;
    this.username = localStorage.getItem('username');
    
    // Fetch summary data
    this.fetchSummary();
  },
  
  methods: {
    fetchSummary() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API
      axios.get(`http://localhost:5000/user/summary/${this.userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Store data
        this.username = response.data.username;
        this.totalReservations = response.data.total_reservations;
        this.totalSpent = response.data.total_spent;
        this.usageData = response.data.usage_data;
        
        // Create chart after data is loaded
        this.$nextTick(() => {
          this.createChart();
        });
      })
      .catch((error) => {
        console.error('Error fetching summary:', error);
        alert('Failed to fetch summary data');
      });
    },
    
    createChart() {
      // Extract labels and counts from usageData
      const labels = this.usageData.map(item => item.lot);
      const counts = this.usageData.map(item => item.count);
      
      // Create chart
      const ctx = document.getElementById('usageChart');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'No. of Reservations',
            data: counts,
            backgroundColor: 'rgba(255, 159, 64, 0.6)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    },
    
    logout() {
      // Clear all stored data
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      
      // Redirect to login page
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.user-summary-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 50px;
  position: relative;
}

/* Subtle pattern overlay */
.user-summary-page::before {
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

header .left-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

header .left {
  font-weight: bold;
  font-size: 1.1rem;
}

header nav a {
  margin: 0 5px;
  text-decoration: none;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

header nav a:hover {
  opacity: 0.8;
}

header .right a {
  text-decoration: none;
  color: white;
  font-weight: 500;
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  transition: all 0.2s;
}

header .right a:hover {
  background: rgba(255, 255, 255, 0.3);
}

.container {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.mt-4 {
  margin-top: 30px;
}

h2 {
  font-weight: 600;
  color: white;
  margin-bottom: 40px;
  font-size: 2rem;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 30px;
}

.mb-3 {
  margin-bottom: 20px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.col-md-6 {
  flex: 1;
  min-width: 250px;
}

.col-md-8 {
  flex: 1;
  max-width: 900px;
}

.justify-content-center {
  justify-content: center;
}

.stat-box {
  padding: 25px 20px;
  color: white;
  font-weight: bold;
  border-radius: 12px;
  font-size: 1.4rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.bg1 { 
  background: linear-gradient(135deg, #6c5ce7 0%, #5a4bc7 100%);
}

.bg2 { 
  background: linear-gradient(135deg, #00cec9 0%, #00b8af 100%);
}

h5 {
  font-weight: 600;
  color: #1a1a1a;
  padding: 15px;
  background: white;
  border-radius: 10px 10px 0 0;
  margin-bottom: 0;
}

canvas {
  background-color: white;
  border-radius: 0 0 10px 10px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 20px 10px;
  }
  
  h2 {
    font-size: 1.6rem;
  }
  
  .stat-box {
    font-size: 1.2rem;
  }
  
  header {
    flex-direction: column;
    gap: 15px;
  }
  
  .row {
    flex-direction: column;
  }
}
</style>
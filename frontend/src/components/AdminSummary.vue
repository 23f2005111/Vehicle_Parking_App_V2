<template>
  <div class="admin-summary-page">
    
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

    <div class="container mt-4">
      <h2 class="text-center mb-4">Admin Summary Dashboard</h2>

      <!-- Stats Boxes -->
      <div class="row text-center mb-4">
        <div class="col-md-3">
          <div class="stat-box bg-lots">Total Lots: {{ totalLots }}</div>
        </div>
        <div class="col-md-3">
          <div class="stat-box bg-spots">Total Spots: {{ totalSpots }}</div>
        </div>
        <div class="col-md-3">
          <div class="stat-box bg-occupied">Occupied: {{ totalOccupied }}</div>
        </div>
        <div class="col-md-3">
          <div class="stat-box bg-available">Available: {{ totalAvailable }}</div>
        </div>
      </div>

      <!-- Revenue -->
      <div class="text-center mb-5">
        <h4>Total Revenue Collected: ₹{{ totalRevenue }}</h4>
      </div>

      <!-- Charts -->
      <div class="row">
        <div class="col-md-6">
          <h5 class="text-center">Revenue per Lot</h5>
          <canvas id="revenueChart"></canvas>
        </div>
        <div class="col-md-6">
          <h5 class="text-center">Occupancy per Lot</h5>
          <canvas id="occupancyChart"></canvas>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'AdminSummary',
  
  data() {
    return {
      totalLots: 0,
      totalSpots: 0,
      totalOccupied: 0,
      totalAvailable: 0,
      totalRevenue: 0,
      revenueByLot: [],
      occupancyByLot: []
    };
  },
  
  created() {
    // Fetch summary data
    this.fetchSummary();
  },
  
  methods: {
    fetchSummary() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API
      axios.get('http://localhost:5000/admin/summary', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Store data
        this.totalLots = response.data.total_lots;
        this.totalSpots = response.data.total_spots;
        this.totalOccupied = response.data.total_occupied;
        this.totalAvailable = response.data.total_available;
        this.totalRevenue = response.data.total_revenue;
        this.revenueByLot = response.data.revenue_by_lot;
        this.occupancyByLot = response.data.occupancy_by_lot;
        
        // Create charts after data is loaded
        this.$nextTick(() => {
          this.createRevenueChart();
          this.createOccupancyChart();
        });
      })
      .catch((error) => {
        console.error('Error fetching summary:', error);
        alert('Failed to fetch summary data');
      });
    },
    
    createRevenueChart() {
      // Extract labels and values from revenueByLot
      const labels = this.revenueByLot.map(item => item.lot);
      const values = this.revenueByLot.map(item => item.revenue);
      
      // Create revenue chart
      const ctx = document.getElementById('revenueChart');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Revenue',
            data: values,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
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
    
    createOccupancyChart() {
      // Extract labels and values from occupancyByLot
      const labels = this.occupancyByLot.map(item => item.lot);
      const occupied = this.occupancyByLot.map(item => item.occupied);
      const available = this.occupancyByLot.map(item => item.available);
      
      // Create occupancy chart
      const ctx = document.getElementById('occupancyChart');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Occupied',
              data: occupied,
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            },
            {
              label: 'Available',
              data: available,
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' }
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
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.admin-summary-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 50px;
  position: relative;
}

/* Subtle pattern overlay */
.admin-summary-page::before {
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
  cursor: pointer;
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
  max-width: 1400px;
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

h4 {
  font-weight: 600;
  color: white;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 10px;
  font-size: 1.5rem;
}

h5 {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 15px;
  padding: 15px;
  background: white;
  border-radius: 10px 10px 0 0;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.col-md-3 {
  flex: 1;
  min-width: 200px;
}

.col-md-6 {
  flex: 1;
  min-width: 300px;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 30px;
}

.mb-5 {
  margin-bottom: 40px;
}

.stat-box {
  padding: 25px 20px;
  color: white;
  font-weight: bold;
  border-radius: 12px;
  font-size: 1.3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.stat-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.bg-lots { 
  background: linear-gradient(135deg, #6c63ff 0%, #5a52d5 100%);
}

.bg-spots { 
  background: linear-gradient(135deg, #00b894 0%, #00a382 100%);
}

.bg-occupied { 
  background: linear-gradient(135deg, #fd7272 0%, #fc5c5c 100%);
}

.bg-available { 
  background: linear-gradient(135deg, #0984e3 0%, #0770c9 100%);
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
    font-size: 1.1rem;
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
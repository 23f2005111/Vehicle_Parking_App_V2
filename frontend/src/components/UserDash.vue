<template>
  <div class="user-dashboard-page">
    
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

        <!-- CSV EXPORT BUTTON - Only show if reservations exist -->
        <button 
          v-if="reservations.length > 0"
          class="btn btn-light btn-sm ms-3" 
          @click="startCSVExport"
        >
          Export CSV
        </button>
      </div>
    </header>

    <div class="container mt-4">

      <!-- Parking History Section -->
      <h3 class="section-title mb-3 text-primary">Recent Parking History</h3>
      
      <div v-if="reservations.length > 0">
        <table class="table table-bordered text-center">
          <thead>
            <tr>
              <th>Reservation ID</th>
              <th>Lot ID</th>
              <th>Spot Number</th>
              <th>Location</th>
              <th>Vehicle No</th>
              <th>Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in reservations" :key="res.id">
              <td>{{ res.id }}</td>
              <td>{{ res.lot_id }}</td>
              <td>{{ res.spot_number }}</td>
              <td>{{ res.lot_name }}</td>
              <td>{{ res.vehicle_number }}</td>
              <td>{{ formatDate(res.parking_timestamp) }}</td>
              <td>
                <div v-if="res.status === 'completed'" class="d-flex justify-content-center gap-2">
                  <button class="btn btn-success btn-sm" disabled>Parked Out</button>
                  <button @click="removeReservation(res.id)" class="btn btn-danger btn-sm">Remove</button>
                </div>
                <router-link v-else :to="`/user/release/${res.id}`" class="btn btn-warning btn-sm">
                  Release
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <p v-else class="text-muted text-center">No parking history found.</p>

      <!-- Available Parking Lots Section -->
      <h3 class="section-title mt-5 mb-3 text-primary">Available Parking Lots</h3>
      
      <div v-if="lots.length > 0">
        <table class="table table-bordered text-center">
          <thead>
            <tr>
              <th>Lot ID</th>
              <th>Lot Location</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Availability</th>
              <th>Price per Hour</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td>{{ lot.name }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.pincode }}</td>
              <td>{{ lot.available }}</td>
              <td>₹{{ lot.price }}</td>
              <td>
                <router-link 
                  v-if="lot.available > 0" 
                  :to="`/user/book/${lot.id}/${userId}`" 
                  class="btn btn-primary btn-sm"
                >
                  Book
                </router-link>
                <span v-else class="text-muted">Full</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <p v-else class="text-muted text-center">No parking lots available at the moment.</p>

    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  
  data() {
    return {
      userId: null,
      username: '',
      reservations: [],
      lots: [],
      csvTaskId: null,
      csvStatus: null
    };
  },
  
  created() {
    this.userId = this.$route.params.id || localStorage.getItem('user_id');
    this.username = localStorage.getItem('username');
    this.fetchDashboard();
  },
  
  methods: {
    startCSVExport() {
      const token = localStorage.getItem('token');

      axios.post(
        `http://localhost:5000/user/export_csv/${this.userId}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then(res => {
        this.csvTaskId = res.data.task_id;
        this.csvStatus = "processing";
        alert("CSV export started. Please wait...");
        this.checkCSVTask();
      })
      .catch(() => {
        alert("Failed to start CSV export");
      });
    },

    checkCSVTask() {
      if (!this.csvTaskId) return;

      const token = localStorage.getItem('token');

      const interval = setInterval(() => {
        axios.get(
          `http://localhost:5000/user/csv_status/${this.csvTaskId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        .then(res => {
          if (res.data.status === "completed") {
            clearInterval(interval);
            this.csvStatus = "done";
            this.downloadCSV(res.data.filename);
          }
          else if (res.data.status === "failed") {
            clearInterval(interval);
            this.csvStatus = "failed";
            alert("CSV generation failed");
          }
        });
      }, 2000);
    },

    downloadCSV(filename) {
      window.location.href = `http://localhost:5000/user/download_csv/${filename}`;
    },

    fetchDashboard() {
      const token = localStorage.getItem('token');
      
      axios.get(`http://localhost:5000/user/${this.userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        this.username = response.data.user.username;
        this.reservations = response.data.reservations;
        this.lots = response.data.lots;
      })
      .catch(() => {
        alert('Failed to fetch dashboard data');
      });
    },

    removeReservation(resId) {
      if (!confirm('Delete this reservation?')) return;
      
      const token = localStorage.getItem('token');
      
      axios.post(`http://localhost:5000/user/remove/${resId}`, {}, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      .then((response) => {
        alert(response.data.message);
        this.fetchDashboard();
      })
      .catch(() => {
        alert('Failed to remove reservation');
      });
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      this.$router.push('/login');
    }
  }
};
</script>



<style scoped>
.user-dashboard-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 50px;
  position: relative;
}

/* Subtle pattern overlay */
.user-dashboard-page::before {
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
  cursor: pointer;
  transition: opacity 0.2s;
}

nav a:hover {
  opacity: 0.8;
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.right a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  transition: all 0.2s;
}

.right a:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-light {
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: none;
  font-weight: 600;
}

.btn-light:hover:not(:disabled) {
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-light:disabled {
  background: rgba(255, 255, 255, 0.4);
  color: #999;
  cursor: not-allowed;
  opacity: 0.6;
}

.container {
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.section-title {
  font-weight: 600;
  color: #1a1a1a;
  background: white;
  padding: 15px 20px;
  border-radius: 10px 10px 0 0;
  margin-bottom: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.text-primary {
  color: #1a1a1a !important;
}

.table {
  background: white;
  border-radius: 0 0 10px 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 40px;
}

.table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.table th {
  padding: 15px 12px;
  font-weight: 600;
  font-size: 0.95rem;
  border: none;
}

.table td {
  padding: 12px;
  vertical-align: middle;
  color: #1a1a1a;
  font-size: 0.95rem;
  border-color: #e5e7eb;
}

.table tbody tr {
  transition: background-color 0.2s;
}

.table tbody tr:hover {
  background-color: #f9fafb;
}

.btn {
  font-weight: 600;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 0.9rem;
  padding: 6px 16px;
}

.btn-primary {
  background: #667eea;
  border: none;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.btn-warning {
  background: #ffc107;
  border: none;
  color: #1a1a1a;
}

.btn-warning:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

.btn-success {
  background: #28a745;
  border: none;
  color: white;
}

.btn-danger {
  background: #dc3545;
  border: none;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-1px);
}

.d-flex {
  display: flex;
}

.justify-content-center {
  justify-content: center;
}

.gap-2 {
  gap: 8px;
}

.text-muted {
  color: white !important;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 10px;
  font-size: 1.1rem;
  text-align: center;
}

.mt-5 {
  margin-top: 50px;
}

.mb-3 {
  margin-bottom: 15px;
}

.ms-3 {
  margin-left: 10px;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 20px 10px;
  }
  
  .table {
    font-size: 0.85rem;
  }
  
  .section-title {
    font-size: 1.2rem;
    padding: 12px 15px;
  }
  
  header {
    flex-direction: column;
    gap: 15px;
  }
  
  .right {
    flex-direction: column;
  }
}
</style>
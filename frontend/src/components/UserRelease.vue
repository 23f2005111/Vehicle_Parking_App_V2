<template>
  <div class="release-page">
    <div class="release-container">
      <div class="card">
        <h3 class="text-center text-warning">Release the parking spot</h3>
        
        <form @submit.prevent="releaseSpot">

          <label>Lot ID:</label>
          <input type="text" :value="reservation.lot_id" disabled>

          <label>Spot Number:</label>
          <input type="text" :value="reservation.spot_number" disabled>

          <label>Vehicle Number:</label>
          <input type="text" :value="reservation.vehicle_number" disabled>

          <label>Parking Time:</label>
          <input type="text" :value="formatDateTime(reservation.parking_timestamp)" disabled>

          <label>Releasing Time:</label>
          <input type="text" :value="formatDateTime(reservation.current_time)" disabled>

          <label>Hours Parked:</label>
          <input type="text" :value="reservation.hours_parked" disabled>

          <label>Total Cost:</label>
          <input type="text" :value="`₹${reservation.total_cost}`" disabled>

          <div class="btn-group">
            <button type="submit" class="btn-release">Release</button>
            <router-link :to="`/user/${userId}`" class="btn-cancel">Cancel</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRelease',
  
  data() {
    return {
      userId: null,
      resId: null,
      reservation: {
        lot_id: '',
        spot_number: '',
        vehicle_number: '',
        parking_timestamp: '',
        current_time: '',
        hours_parked: 0,
        total_cost: 0
      }
    };
  },
  
  created() {
    // Get reservation ID from route
    this.resId = this.$route.params.id;
    this.userId = localStorage.getItem('user_id');
    
    // Fetch release details
    this.fetchReleaseDetails();
  },
  
  methods: {
    fetchReleaseDetails() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to get release details
      axios.get(`http://localhost:5000/user/release/${this.resId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Store reservation details
        this.reservation = response.data;
      })
      .catch((error) => {
        console.error('Error fetching release details:', error);
        alert('Failed to fetch reservation details');
        this.$router.push(`/user/${this.userId}`);
      });
    },
    
    releaseSpot() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to release the spot
      axios.post(`http://localhost:5000/user/release/${this.resId}`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Success! Show message and redirect
        alert(`${response.data.message}\nTotal Cost: ₹${response.data.total_cost}`);
        this.$router.push(`/user/${this.userId}`);
      })
      .catch((error) => {
        // Error! Show error message
        alert('Failed to release spot');
        console.error(error);
      });
    },
    
    formatDateTime(dateString) {
      // Convert ISO string to readable format
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.release-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.release-container {
  width: 100%;
  max-width: 500px;
}

.card {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

h3 {
  margin-bottom: 30px;
  font-weight: 600;
}

.text-warning {
  color: #ffc107 !important;
}

form label {
  display: block;
  font-weight: 500;
  color: #555;
  margin-top: 15px;
  margin-bottom: 5px;
}

form input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #e9ecef;
  cursor: not-allowed;
}

.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
  justify-content: center;
}

.btn-release {
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
}

.btn-release:hover {
  background: #218838;
}

.btn-cancel {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.btn-cancel:hover {
  background: #5a6268;
  color: white;
}
</style>
<template>
  <div class="spot-info-page">
    <div class="card">
      <h4>Occupied Parking Spot Details</h4>
      
      <div class="mb-3">
        <label class="form-label">Reservation ID:</label>
        <input type="text" class="form-control" :value="spotInfo.reservation_id" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Spot Number:</label>
        <input type="text" class="form-control" :value="spotInfo.spot_number" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Customer ID:</label>
        <input type="text" class="form-control" :value="spotInfo.user_id" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Customer Username:</label>
        <input type="text" class="form-control" :value="spotInfo.username" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Customer Email:</label>
        <input type="text" class="form-control" :value="spotInfo.email" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Vehicle Number:</label>
        <input type="text" class="form-control" :value="spotInfo.vehicle_number" disabled>
      </div>

      <div class="mb-3">
        <label class="form-label">Date/Time of Parking:</label>
        <input type="text" class="form-control" :value="formatDateTime(spotInfo.parking_timestamp)" disabled>
      </div>

      <div class="text-center">
        <router-link to="/admin" class="btn btn-primary">Close</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SpotInfo',
  
  data() {
    return {
      spotInfo: {
        reservation_id: '',
        spot_number: '',
        user_id: '',
        username: '',
        email: '',
        vehicle_number: '',
        parking_timestamp: ''
      }
    };
  },
  
  created() {
    // Get lot_id and spot_number from route
    const lotId = this.$route.params.lot_id;
    const spotNumber = this.$route.params.spot_number;
    
    // Fetch spot info
    this.fetchSpotInfo(lotId, spotNumber);
  },
  
  methods: {
    fetchSpotInfo(lotId, spotNumber) {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API
      axios.get(`http://localhost:5000/admin/spot_info/${lotId}/${spotNumber}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Check if there's an active reservation
        if (response.data.reservation) {
          this.spotInfo = {
            reservation_id: response.data.reservation.id,
            spot_number: response.data.spot_number,
            user_id: response.data.reservation.user.id,
            username: response.data.reservation.user.username,
            email: response.data.reservation.user.email,
            vehicle_number: response.data.reservation.vehicle_number,
            parking_timestamp: response.data.reservation.parking_timestamp
          };
        } else {
          alert(response.data.message || 'No active reservation');
          this.$router.push('/admin');
        }
      })
      .catch((error) => {
        console.error('Error fetching spot info:', error);
        alert('Failed to fetch spot information');
        this.$router.push('/admin');
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
.spot-info-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.card {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 500px;
}

h4 {
  text-align: center;
  margin-bottom: 30px;
  color: #667eea;
  font-weight: 600;
}

.form-label {
  font-weight: 500;
  color: #555;
  margin-bottom: 5px;
}

.form-control {
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: #e9ecef;
  cursor: not-allowed;
  padding: 10px;
}

.btn-primary {
  background: #667eea;
  border: none;
  padding: 12px 40px;
  border-radius: 5px;
  font-weight: 600;
  text-decoration: none;
  color: white;
  display: inline-block;
  margin-top: 20px;
}

.btn-primary:hover {
  background: #764ba2;
  color: white;
}
</style>
<template>
  <div class="booking-page">
    
    <div class="card">
      <h4 class="text-center mb-4">Book Parking Spot</h4>

      <form @submit.prevent="reserveSpot">

        <div class="mb-3">
          <label class="form-label">User ID</label>
          <input type="text" class="form-control" :value="userId" disabled>
        </div>

        <div class="mb-3">
          <label class="form-label">Lot ID</label>
          <input type="text" class="form-control" :value="lotId" disabled>
        </div>

        <div class="mb-3">
          <label class="form-label">Spot Number</label>
          <input type="text" class="form-control" :value="spotNumber" disabled>
        </div>

        <div class="mb-3">
          <label class="form-label">Vehicle Number</label>
          <input 
            type="text" 
            v-model="vehicleNumber" 
            class="form-control" 
            placeholder="Enter vehicle number (e.g., MH01AB1234)" 
            required
          >
        </div>
      
        <div class="button-group">
          <router-link :to="`/user/${userId}`" class="btn btn-secondary">Cancel</router-link>
          <button type="submit" class="btn btn-primary">Reserve Spot</button>
        </div>

      </form>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserBooking',
  
  data() {
    return {
      userId: null,
      lotId: null,
      spotNumber: null,
      vehicleNumber: ''
    };
  },
  
  created() {
    // Get lot_id and user_id from route parameters
    this.lotId = this.$route.params.lot_id;
    this.userId = this.$route.params.user_id;
    
    // Fetch booking details
    this.fetchBookingDetails();
  },
  
  methods: {
    fetchBookingDetails() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to get available spot
      axios.get(`http://localhost:5000/user/book/${this.lotId}/${this.userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Get the spot number from response
        this.spotNumber = response.data.spot.spot_number;
      })
      .catch((error) => {
        console.error('Error fetching booking details:', error);
        alert(error.response?.data?.message || 'No available spots in this lot!');
        // Redirect back to dashboard
        this.$router.push(`/user/${this.userId}`);
      });
    },
    
    reserveSpot() {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to reserve the spot
      axios.post('http://localhost:5000/user/reserve', {
        user_id: this.userId,
        lot_id: this.lotId,
        spot_number: this.spotNumber,
        vehicle_number: this.vehicleNumber
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Success! Show message and redirect
        alert(response.data.message);
        this.$router.push(`/user/${this.userId}`);
      })
      .catch((error) => {
        // Error! Show error message
        alert(error.response?.data?.message || 'Failed to reserve spot');
        console.error(error);
      });
    }
  }
};
</script>

<style scoped>
.booking-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
}

/* Subtle pattern overlay */
.booking-page::before {
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

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 50px 40px;
  width: 100%;
  max-width: 550px;
  position: relative;
  z-index: 1;
}

/* Decorative top bar */
.card::before {
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
  font-weight: 600;
  color: #1a1a1a;
  font-size: 1.8rem;
  margin-bottom: 35px;
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
  width: 100%;
  transition: all 0.2s;
}

.form-control:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
  color: #6b7280;
  border-color: #e5e7eb;
}

.form-control:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.button-group {
  display: flex;
  gap: 15px;
  margin-top: 35px;
  justify-content: space-between;
}

.btn {
  padding: 13px 32px;
  font-weight: 600;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  border: none;
  flex: 1;
}

.btn-primary {
  background: #667eea;
  color: white;
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
  .card {
    padding: 40px 25px;
  }
  
  h4 {
    font-size: 1.5rem;
  }

  .button-group {
    flex-direction: column-reverse;
  }
}
</style>
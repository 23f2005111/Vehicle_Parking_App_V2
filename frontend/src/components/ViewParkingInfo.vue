<template>
  <div class="view-parking-page p-4 bg-light">
    
    <div class="container text-center">
      <h3 class="mb-4 text-primary">Reservation Details</h3>

      <div class="row justify-content-center">
        <div class="col-md-6">
          <table class="table table-bordered">
            <tbody>
              <tr>
                <th>User Name</th>
                <td>{{ reservation.username }}</td>
              </tr>
              <tr>
                <th>User Email</th>
                <td>{{ reservation.email }}</td>
              </tr>
              <tr>
                <th>Vehicle Number</th>
                <td>{{ reservation.vehicle_number }}</td>
              </tr>
              <tr>
                <th>Parking Time</th>
                <td>{{ formatDateTime(reservation.parking_timestamp) }}</td>
              </tr>
              <tr>
                <th>Lot ID</th>
                <td>{{ reservation.lot_id }}</td>
              </tr>
              <tr>
                <th>Spot Number</th>
                <td>{{ reservation.spot_number }}</td>
              </tr>
            </tbody>
          </table>

          <router-link to="/admin" class="btn btn-secondary mt-3">Back to Dashboard</router-link>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewParking',
  
  data() {
    return {
      reservation: {  // data info
        username: '',
        email: '',
        vehicle_number: '',
        parking_timestamp: '',
        lot_id: '',
        spot_number: ''
      }
    };
  },
  
  created() {
    // get lot_id and spot_number from route
    const lotId = this.$route.params.lot_id;
    const spotNumber = this.$route.params.spot_number;
    
    // fetch the reservation details
    this.fetchReservationDetails(lotId, spotNumber);
  },
  
  methods: {
    fetchReservationDetails(lotId, spotNumber) {
      // get JWT token
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
          this.reservation = {
            username: response.data.reservation.user.username,
            email: response.data.reservation.user.email,
            vehicle_number: response.data.reservation.vehicle_number,
            parking_timestamp: response.data.reservation.parking_timestamp,
            lot_id: lotId,
            spot_number: spotNumber
          };
        } else {
          alert(response.data.message || 'No active reservation');
          this.$router.push('/admin');
        }
      })
      .catch((error) => {
        console.error('Error fetching reservation details:', error);
        alert('Failed to fetch reservation details');
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
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.view-parking-page {
  min-height: 100vh;
}

h3 {
  font-weight: 600;
}

.text-primary {
  color: #667eea !important;
}

.table {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.table th {
  background: #f8f9fa;
  font-weight: 600;
  text-align: left;
  padding: 15px;
  width: 45%;
}

.table td {
  text-align: left;
  padding: 15px;
}

.btn-secondary {
  background: #6c757d;
  border: none;
  padding: 10px 30px;
  font-weight: 600;
  text-decoration: none;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  color: white;
}
</style>
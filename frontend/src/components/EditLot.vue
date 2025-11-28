<template>
  <div class="edit-lot-page bg-light">
    
    <div class="container mt-5">
      <div class="card p-4 shadow">
        <h3 class="text-center mb-4 text-warning">Edit Parking Lot</h3>
        
        <form @submit.prevent="updateLot">
          
          <div class="mb-3">
            <label class="form-label">Prime Location Name</label>
            <input type="text" v-model="name" class="form-control" placeholder="Enter Location" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea v-model="address" class="form-control" rows="3" placeholder="Enter Address" required></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Pincode</label>
            <input 
              type="text" 
              v-model="pincode" 
              class="form-control" 
              pattern="^\d{6}$" 
              inputmode="numeric" 
              maxlength="6" 
              placeholder="Enter Pincode"
              title="Enter a valid 6-digit PIN code" 
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Price (per hour)</label>
            <input type="number" step="0.01" v-model="price" class="form-control" placeholder="Enter Price" required>
          </div>

          <div class="mb-4">
            <label class="form-label">Maximum Spots</label>
            <input type="number" v-model="max_spots" class="form-control" placeholder="Enter Max Spot" required>
            <small class="text-muted">Currently occupied: {{ occupied_count }}</small>
          </div>

          <div class="text-center">
            <router-link to="/admin" class="btn btn-secondary">Cancel</router-link>
            <button type="submit" class="btn btn-primary">Update</button>
          </div>
          
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditLot',
  
  data() {
    return {
      // Form fields
      name: '',
      address: '',
      pincode: '',
      price: '',
      max_spots: '',
      occupied_count: 0
    };
  },
  
  created() {
    // Get lot ID from route parameter
    const lotId = this.$route.params.id;
    this.fetchLotDetails(lotId);
  },
  
  methods: {
    fetchLotDetails(lotId) {
      // Get JWT token
      const token = localStorage.getItem('token');
      
      // Call backend API to get lot details
      axios.get(`http://localhost:5000/admin/edit_lot/${lotId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Fill form with existing data
        const lot = response.data;
        this.name = lot.name;
        this.address = lot.address;
        this.pincode = lot.pincode;
        this.price = lot.price;
        this.max_spots = lot.max_spots;
        this.occupied_count = lot.occupied_count;
      })
      .catch((error) => {
        console.error('Error fetching lot details:', error);
        alert('Failed to fetch lot details');
      });
    },
    
    updateLot() {
      // Validation: Cannot reduce spots below occupied count
      if (parseInt(this.max_spots) < this.occupied_count) {
        alert(`❌ You cannot reduce total spots below the currently occupied count (${this.occupied_count}).`);
        return;
      }
      
      // Get JWT token and lot ID
      const token = localStorage.getItem('token');
      const lotId = this.$route.params.id;
      
      // Call backend API to update lot
      axios.post(`http://localhost:5000/admin/edit_lot/${lotId}`, {
        name: this.name,
        address: this.address,
        pincode: this.pincode,
        price: parseFloat(this.price),
        max_spots: parseInt(this.max_spots)
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Success! Show message and redirect
        alert(response.data.message);
        this.$router.push('/admin');
      })
      .catch((error) => {
        // Error! Show error message
        alert(error.response?.data?.message || 'Failed to update parking lot');
        console.error(error);
      });
    }
  }
};
</script>

<style scoped>
.edit-lot-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.edit-lot-page::before {
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

.container {
  width: 100%;
  max-width: 700px;
  position: relative;
  z-index: 1;
}

.mt-5 {
  margin-top: 0;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 50px 80px;
  margin: 0 auto;
}

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

.p-4 {
  padding: 0 !important;
}

.shadow {
  box-shadow: none !important;
}

h3 {
  font-weight: 700;
  color: #1f2937;
  font-size: 2rem;
  margin-bottom: 40px;
  text-align: center;
  letter-spacing: -0.5px;
}

.text-warning {
  color: #1f2937 !important;
}

form {
  padding: 0 30px;
}

.mb-3, .mb-4 {
  margin-bottom: 28px;
}

.form-label {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 10px;
  font-size: 1rem;
  display: block;
}

.form-control {
  border-radius: 10px;
  border: none;
  padding: 14px 18px;
  font-size: 1rem;
  color: #1f2937;
  width: 100%;
  transition: all 0.2s;
  background-color: #f3f4f6;
  font-weight: 400;
}

.form-control::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.form-control:focus {
  border: none;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
  background-color: #f3f4f6;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
}

.text-muted {
  display: block;
  margin-top: 10px;
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

.text-center {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 40px;
}

.btn {
  padding: 14px 55px;
  font-weight: 600;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  min-width: 140px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #e5e7eb;
  color: #4b5563;
  border: none;
}

.btn-secondary:hover {
  background: #d1d5db;
  color: #374151;
  transform: translateY(-1px);
}

.ms-2 {
  margin-left: 0 !important;
}

@media (max-width: 768px) {
  .card {
    padding: 40px 30px;
  }
  
  h3 {
    font-size: 1.65rem;
  }

  .text-center {
    flex-direction: column-reverse;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
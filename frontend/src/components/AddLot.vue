<template>
  <div class="add-lot-page">
    
    <div class="container">
      <div class="card">
        <h3 class="text-center mb-4">New Parking Lot</h3>
        
        <form @submit.prevent="addLot">
          
          <div class="mb-3">
            <label class="form-label">Prime Location Name</label>
            <input type="text" v-model="name" placeholder="Enter Location" class="form-control" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea v-model="address" placeholder="Enter Address" class="form-control" rows="3" required></textarea>
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
              title="Enter a valid 6-digit PIN code" 
              placeholder="Enter Pincode"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Price (per hour)</label>
            <input type="number" placeholder="Enter Price" step="0.01" v-model="price" class="form-control" required>
          </div>

          <div class="mb-4">
            <label class="form-label">Maximum Spots</label>
            <input type="number" placeholder="Enter Max Spot" v-model="max_spots" class="form-control" required>
          </div>

          <div class="text-center">
            <router-link to="/admin" class="btn btn-secondary">Cancel</router-link>
            <button type="submit" class="btn btn-primary">Add Lot</button>
          </div>
          
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddLot',
  
  data() {
    return {
      // Form fields
      name: '',   // all data info
      address: '',
      pincode: '',
      price: '',
      max_spots: ''
    };
  },
  
  methods: {
    addLot() {
      // get JWT token
      const token = localStorage.getItem('token');
      
      // call backend API
      axios.post('http://localhost:5000/admin/add_lot', {
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
        // success message
        alert(response.data.message);
        this.$router.push('/admin');
      })
      .catch((error) => {
        // error info
        alert('Failed to add parking lot');
        console.error(error);
      });
    }
  }
};
</script>

<style scoped>
.add-lot-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.add-lot-page::before {
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
  max-width: 600px;
  position: relative;
  z-index: 1;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 50px 40px;
  margin: 0 auto;
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

h3 {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 1.8rem;
  margin-bottom: 35px;
}

.mb-3, .mb-4 {
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

.form-control:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.text-center {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 35px;
}

.btn {
  padding: 13px 50px;
  font-weight: 600;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  min-width: 160px;
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
  
  h3 {
    font-size: 1.5rem;
  }

  .text-center {
    flex-direction: column-reverse;
  }
}
</style>
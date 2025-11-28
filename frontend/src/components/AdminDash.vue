
<template>
  <div class="admin-page">
    
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

    <h2>Parking Lots</h2>

    <!-- Parking Lots List -->
    <div class="parking-lots">
      <div v-if="lots.length > 0" class="lots-container">
        <div v-for="lot in lots" :key="lot.id" class="lot">
          <h4>Location: {{ lot.name }}</h4>

          <!-- Edit/Delete Buttons -->
          <div class="actions d-flex gap-2 mt-2 justify-content-center">
            <router-link :to="`/admin/edit_lot/${lot.id}`" class="btn btn-primary btn-sm">Edit</router-link>
            
            <button 
              v-if="lot.occupied === 0" 
              @click="deleteLot(lot.id)" 
              class="btn btn-danger btn-sm"
            >
              Delete
            </button>
            <button v-else class="btn btn-secondary btn-sm" disabled>Disabled</button>
          </div>

          <!-- Status -->
          <div class="status">
            (Occupied : {{ lot.occupied }}/{{ lot.max_spots }})
          </div>

          <!-- Spots Display -->
          <div class="spots">
            <div v-for="n in lot.max_spots" :key="n" class="spot-wrapper">
              <router-link 
                v-if="isSpotOccupied(lot, n)" 
                :to="`/admin/spot_info/${lot.id}/${n}`" 
                class="spot occupied"
              >
                O
              </router-link>
              <div v-else class="spot available" @click="showAlert">A</div>
            </div>
          </div>
        </div>
      </div>

      <p v-else style="text-align: center; margin-top: 40px; font-size: 1.2rem; color: #777;">
        No lots available.
      </p>
    </div>

    <!-- Add Lot Button -->
    <div class="add-lot-container">
      <router-link to="/admin/add_lot" class="add-lot-btn">+ Add Lot</router-link>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  
  data() {
    return {
      lots: []  // Store all parking lots here
    };
  },
  
  created() {
    // When component loads, fetch parking lots
    this.fetchLots();
  },
  
  methods: {
    fetchLots() {
      // Get JWT token from localStorage
      const token = localStorage.getItem('token');
      
      // Call backend API with token in header
      axios.get('http://localhost:5000/admin', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        // Store lots data
        this.lots = response.data.lots;
      })
      .catch((error) => {
        console.error('Error fetching lots:', error);
        alert('Failed to fetch parking lots');
      });
    },
    
    deleteLot(lotId) {
      // Confirm before deleting
      if (!confirm('Are you sure you want to delete this lot?')) {
        return;
      }
      
      const token = localStorage.getItem('token');
      
      axios.post(`http://localhost:5000/admin/delete_lot/${lotId}`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then((response) => {
        alert(response.data.message);
        // Refresh the lots list
        this.fetchLots();
      })
      .catch((error) => {
        alert('Failed to delete lot');
      });
    },
    
    isSpotOccupied(lot, spotNumber) {
      return spotNumber <= lot.occupied;
    },
    
    showAlert() {
      alert('No active reservation');
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
.admin-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-bottom: 50px;
  position: relative;
}

/* Subtle pattern overlay */
.admin-page::before {
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

h2 {
  text-align: center;
  margin: 40px 0 30px 0;
  color: white;
  font-size: 2rem;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.parking-lots {
  padding: 0 30px;
  position: relative;
  z-index: 1;
}

.lots-container {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  justify-content: center;
}

.lot {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 360px;
  transition: transform 0.2s;
}

.lot:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.lot h4 {
  text-align: center;
  color: #667eea;
  margin-bottom: 15px;
  font-weight: 600;
  font-size: 1.1rem;
}

.actions {
  margin-bottom: 15px;
}

.d-flex {
  display: flex;
}

.gap-2 {
  gap: 10px;
}

.justify-content-center {
  justify-content: center;
}

.mt-2 {
  margin-top: 10px;
}

.btn {
  padding: 8px 20px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-1px);
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
  cursor: not-allowed;
  opacity: 0.6;
}

.status {
  text-align: center;
  font-weight: 600;
  color: #374151;
  margin: 15px 0;
  font-size: 0.95rem;
}

.spots {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.spot {
  width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-size: 1.1rem;
  transition: all 0.2s;
}

.spot.occupied {
  background-color: #dc3545;
}

.spot.occupied:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.spot.available {
  background-color: #28a745;
}

.spot.available:hover {
  background-color: #218838;
  transform: scale(1.05);
}

.add-lot-container {
  text-align: center;
  margin-top: 40px;
  position: relative;
  z-index: 1;
}

.add-lot-btn {
  display: inline-block;
  background: white;
  color: #667eea;
  padding: 15px 45px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.add-lot-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.25);
}

/* Responsive */
@media (max-width: 768px) {
  .parking-lots {
    padding: 0 15px;
  }
  
  .lot {
    width: 100%;
    max-width: 360px;
  }
  
  h2 {
    font-size: 1.6rem;
  }
  
  header {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
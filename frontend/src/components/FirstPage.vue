<template>
  <div class="home-page">
    
    <!-- Navbar -->
    <nav class="navbar">
      <div class="navbar-container">
        <a class="navbar-brand" href="#">🚗 Park It Up</a>
        <div class="nav-buttons">
          <router-link to="/login" class="btn btn-login me-2">Login</router-link>
          <router-link to="/register" class="btn btn-register">Register</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Welcome to Park It Up</h1>
        <p class="hero-subtitle">Your intelligent solution to hassle-free parking</p>
        <!-- <div class="hero-buttons">
          <button class="btn btn-primary-cta">Get Started</button>
          <button class="btn btn-secondary-cta">Learn More</button>
        </div> -->
      </div>
      <div class="hero-decoration"></div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <div class="container">
        <div class="section-header">
          <h2>Why Choose Park It Up?</h2>
          <p>Everything you need for smarter parking</p>
        </div>
        
        <div class="features-grid">
          
          <div class="feature-card">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-map-marker-alt"></i>
              </div>
              <div class="icon-bg"></div>
            </div>
            <h5>Find Nearby Spots</h5>
            <p>Locate available parking near your destination instantly with our smart location system.</p>
          </div>

          <div class="feature-card">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-car-side"></i>
              </div>
              <div class="icon-bg"></div>
            </div>
            <h5>Reserve in Advance</h5>
            <p>Secure your parking with advance bookings and guarantee availability whenever you need it.</p>
          </div>

          <div class="feature-card">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-chart-bar"></i>
              </div>
              <div class="icon-bg"></div>
            </div>
            <h5>View Usage & History</h5>
            <p>Track your parking history and payments through an intuitive dashboard with detailed insights.</p>
          </div>

        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <h3>Smart</h3>
            <p>Parking Solution</p>
          </div>
          <div class="stat-item">
            <h3>Easy</h3>
            <p>Booking System</p>
          </div>
          <div class="stat-item">
            <h3>Fast</h3>
            <p>Spot Locator</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="cta-section">
      <div class="cta-content">
        <h2>Ready to Park Smarter?</h2>
        <p>Join thousands of users enjoying hassle-free parking</p>
        <router-link to="/register" class="btn btn-cta-large">Sign Up Now</router-link>
        <!-- <button class="btn btn-cta-large">Sign Up Now</button> -->
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h5>Park It Up</h5>
            <p>Making parking simple and efficient</p>
          </div>
          <div class="footer-links">
            <a href="#">About</a>
            <a href="#">Contact</a>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2025 Park It Up. All rights reserved.</p>
        </div>
      </div>
    </footer>

  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f4f6f9;
  font-family: 'Segoe UI', sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Navbar */
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-brand {
  color: white;
  font-weight: bold;
  font-size: 1.7rem;
  text-decoration: none;
  letter-spacing: -0.5px;
}

.nav-buttons {
  display: flex;
  gap: 12px;
}

.btn-login {
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 28px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 0.95rem;
  display: inline-block;
}

.btn-login:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-register {
  background: #ffc107;
  color: #333;
  border: none;
  padding: 10px 28px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 0.95rem;
  display: inline-block;
}

.btn-register:hover {
  background: #e0a800;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(224, 168, 0, 0.2);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 120px 20px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-decoration {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(30px); }
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 700px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  letter-spacing: -1px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.4rem;
  opacity: 0.95;
  margin-bottom: 40px;
  font-weight: 300;
  letter-spacing: 0.3px;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary-cta {
  background: #ffc107;
  color: #333;
  border: none;
  padding: 15px 40px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(255, 193, 7, 0.3);
}

.btn-primary-cta:hover {
  background: #e0a800;
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(255, 193, 7, 0.4);
}

.btn-secondary-cta {
  background: transparent;
  color: white;
  border: 2px solid white;
  padding: 13px 38px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary-cta:hover {
  background: white;
  color: #667eea;
  transform: translateY(-3px);
}

/* Features Section */
.features-section {
  padding: 80px 20px;
  background-color: #f4f6f9;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 15px;
  font-weight: 700;
}

.section-header p {
  font-size: 1.1rem;
  color: #666;
  opacity: 0.8;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
}

.feature-card {
  background: white;
  border-radius: 15px;
  padding: 50px 30px 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  border-top: 4px solid;
  border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
}

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
}

.card-header {
  position: relative;
  margin-bottom: 30px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon {
  font-size: 2.5rem;
  color: #667eea;
  position: relative;
  z-index: 2;
}

.icon-bg {
  position: absolute;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.feature-card h5 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
}

.feature-card p {
  color: #666;
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 25px;
}

.feature-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.feature-link:hover {
  color: #764ba2;
  gap: 12px;
}

/* Stats Section */
.stats-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  text-align: center;
}

.stat-item h3 {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.stat-item p {
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 500;
}

/* CTA Section */
.cta-section {
  padding: 80px 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 15px;
  font-weight: 700;
}

.cta-content p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 35px;
  opacity: 0.8;
}

.btn-cta-large {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16px 50px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.btn-cta-large:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 45px rgba(102, 126, 234, 0.4);
}

/* Footer */
.footer {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 50px 20px 20px;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
  align-items: start;
}

.footer-section h5 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  font-weight: 600;
}

.footer-section p {
  opacity: 0.9;
  font-size: 0.95rem;
}

.footer-links {
  display: flex;
  gap: 30px;
  justify-content: flex-end;
}

.footer-links a {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
  font-weight: 500;
}

.footer-links a:hover {
  opacity: 0.7;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 25px;
  text-align: center;
  opacity: 0.85;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .section-header h2 {
    font-size: 2rem;
  }

  .navbar-brand {
    font-size: 1.4rem;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn-primary-cta,
  .btn-secondary-cta {
    width: 100%;
    max-width: 300px;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .footer-links {
    justify-content: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
<template>
  <div class="home">
    <h1>Data Management Application</h1>
    <p>Welcome to the Django + Vue.js Single Page Application</p>
    
    <div class="nav-cards">
      <div class="card" @click="$router.push('/items')">
        <h2>Items</h2>
        <p>Manage your items inventory</p>
      </div>
      
      <div class="card" @click="$router.push('/customers')">
        <h2>Customers</h2>
        <p>Manage customer information</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #42b983;
  margin-bottom: 10px;
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  border-color: #42b983;
}

.card h2 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.card p {
  margin: 0;
  color: #666;
}
</style>

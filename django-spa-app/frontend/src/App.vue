<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">Data Manager</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">HomePage</router-link>
          <router-link to="/items" class="nav-link">Items</router-link>
          <router-link to="/customers" class="nav-link">Customers</router-link>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #f5f5f5;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}

.navbar {
  background-color: #2c3e50;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-brand {
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
}

.nav-brand:hover {
  color: #42b983;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #42b983;
}

.nav-link.router-link-active {
  background-color: #42b983;
}

.main-content {
  padding: 20px 0;
  min-height: calc(100vh - 60px);
}
</style>

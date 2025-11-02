<script setup>
// import HelloWorld from './components/HelloWorld.vue'
// import LoginPage from './components/LoginPage.vue';
import FootPage from './components/FootPage.vue';
import NavPage from './components/NavPage.vue';
// import AdminPage from './components/AdminPage.vue';
</script>

<template>
  <NavPage />
  <!-- <LoginPage/> -->
  <!-- <AdminPage /> -->
  <router-view />
  <FootPage />
  
</template>

<style scoped>
 
</style>

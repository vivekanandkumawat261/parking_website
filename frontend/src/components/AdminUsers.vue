<template>
  <div class="admin-container">
    <!-- Header -->
    <header class="admin-header">
      <div class="left">
        <span class="welcome">Welcome to Admin</span>
      </div>
      <nav class="nav-links">
          <RouterLink to="/dashboard" class="mx-2">Home</RouterLink>
          <RouterLink to="/admin/users" class="mx-2">Users</RouterLink>
          <RouterLink to="/admin/search" class="mx-2">Search</RouterLink>
          <RouterLink to="/admin/summary" class="mx-2">Summary</RouterLink>
        <a href="#">Logout</a>
      </nav>
      <div class="right">
        <a href="#" class="edit-profile">Edit Profile</a>
      </div>
    </header>

    <!-- Main content -->
    <main class="content">
      <h2>Registered Users</h2>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>E-Mail</th>
              <th>Full Name</th>
              <th>Address</th>
              <th>Pin Code</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.fullName }}</td>
              <td>{{ user.address }}</td>
              <td>{{ user.pinCode }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="footer-text">etc., users...</p>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Example: You can replace this with real API call
const users = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/admin/users', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    })
    users.value = res.data.users
  } catch (err) {
    console.error('Failed to fetch users:', err)
    users.value = [
      { id: 1, email: 'abc@gmail.com', fullName: 'zzzzzz', address: 'xxxxxx', pinCode: '444444' },
      { id: 2, email: 'xyz@gmail.com', fullName: 'oooooo', address: 'xxxxxx', pinCode: '222222' },
    ]
  }
})
</script>

<style scoped>
.admin-container {
  border: 2px solid #ccc;
  border-radius: 8px;
  padding: 0;
  font-family: 'Segoe UI', sans-serif;
  background-color: #fff;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #d8f5d1;
  padding: 10px 20px;
  border-bottom: 2px solid #b2d8b2;
  font-size: 15px;
}

.admin-header .welcome {
  color: red;
  font-weight: bold;
}

.nav-links a {
  color: #000;
  text-decoration: none;
  margin: 0 5px;
}

.nav-links a:hover {
  text-decoration: underline;
}

.edit-profile {
  color: blue;
  font-weight: 500;
  text-decoration: none;
}

.edit-profile:hover {
  text-decoration: underline;
}

.content {
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.table-container {
  border: 2px solid #9cc4e4;
  border-radius: 8px;
  padding: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th, td {
  border-bottom: 1px solid #ddd;
  padding: 8px 12px;
}

th {
  background-color: #f1faff;
}

.footer-text {
  color: red;
  font-style: italic;
  margin-top: 10px;
  text-align: left;
}
</style>

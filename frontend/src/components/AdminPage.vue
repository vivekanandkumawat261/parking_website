<script>
import axios from "axios";

export default {
  data() {
    return {
      adminName: "Admin",
      parkingLots: [],
      message: "",
      error: ""
    };
  },
  async created() {
    try {
      // Example: Fetch parking lots
      const res = await axios.get("http://127.0.0.1:5000/admin/parkingLots", {
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
        }
      });
      this.parkingLots = res.data;
       
    } catch (err) {
      this.error = err.response?.data?.message || "Failed to load parking lots.";
    }
  },
  methods: {
    editLot(id) {
      this.$router.push(`/admin/edit-lot/${id}`);
    },
    async deleteLot(id) {
      if (!confirm("Are you sure you want to delete this lot?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/admin/parkingLots/${id}`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          }
        });
        this.parkingLots = this.parkingLots.filter(lot => lot.id !== id);
        this.message = "Parking lot deleted successfully!";
      } catch (err) {
        this.error = "Error deleting parking lot.";
      }
    },
    addLot() {
      this.$router.push("/admin/parkingLots");
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToProfile() {
      this.$router.push("/admin/profile");
    }
  }
};
</script>

<template>
  <div id="admin-dashboard" class="container mt-4">
    <div class="header d-flex justify-content-between align-items-center p-3 bg-light rounded">
      <h3 class="text-success">Welcome to {{ adminName }}</h3>
      <div>
        <router-link to="/admin" class="mx-2">Home</router-link>
        <router-link to="/admin/users" class="mx-2">Users</router-link>
        <router-link to="/admin/search" class="mx-2">Search</router-link>
        <router-link to="/admin/summary" class="mx-2">Summary</router-link>
        <button class="btn btn-outline-primary btn-sm mx-2" @click="goToProfile">Edit Profile</button>
        <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
      </div>
    </div>

    <hr />

    <h4 class="text-center my-4 text-primary">Parking Lots</h4>

    <p class="text-danger text-center" v-if="error">{{ error }}</p>
    <p class="text-success text-center" v-if="message">{{ message }}</p>

    <div class="row">
      <div
        class="col-md-4 mb-4"
        v-for="lot in parkingLots"
        :key="lot.id"
      >
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">🏙 Parkin #{{ lot.id }}</h5>
            <p class="text-muted">Addr: {{ lot.address }}</p>
            <p class="text-success">Occupied: {{ lot.number_of_spots }}</p>

            <div class="btn-group">
              <button class="btn btn-sm btn-warning" @click="editLot(lot.id)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteLot(lot.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <button class="btn btn-primary btn-lg" @click="addLot">+ Add Lot</button>
    </div>
  </div>
</template>

<style scoped>
.header {
  border-radius: 8px;
  background-color: #f8f9fa;
}
.card {
  border-radius: 10px;
  transition: 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
</style>

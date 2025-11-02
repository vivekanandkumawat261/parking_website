<template>
  <div v-if="token">
    <!-- USER DASHBOARD -->
    <div v-if="role === 'user'">
      <div
        class="bg-success bg-opacity-25 border border-dark border-2 rounded-3 p-3 mb-4 d-flex justify-content-between align-items-center"
      >
        <div>
          <span class="fw-bold">Welcome, {{ userData.username }}</span>
          <span class="ms-3">Home | Summary | Logout</span>
        </div>
        <button class="btn btn-primary btn-sm rounded-pill px-4" @click="goToProfile">
          Edit Profile
        </button>
      </div>

      <!-- Parking History -->
      <div class="border border-primary border-2 rounded-3 p-4 mb-4 bg-white">
        <h4 class="text-primary text-center mb-4">Recent Parking History</h4>
        <div class="table-responsive">
          <table class="table table-bordered border-dark">
            <thead class="table-light">
              <tr>
                <th class="text-center">ID</th>
                <th class="text-center">Location</th>
                <th class="text-center">Vehicle No</th>
                <th class="text-center">Timestamp</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="h in userData.history" :key="h.id">
                <td class="text-center">{{ h.id }}</td>
                <td class="text-center">{{ h.location }}</td>
                <td class="text-center">{{ h.vehicle_no || 'N/A' }}</td>
                <td class="text-center">{{ h.timestamp }}</td>
                <td class="text-center">
                  <button class="btn btn-success btn-sm px-3">{{ h.action }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Search -->
      <div class="text-center mb-3">
        <span class="text-danger fw-bold me-3">Search parking @ location/pin code:</span>
        <input
          type="text"
          class="form-control d-inline-block w-auto border border-dark rounded-pill px-4"
          v-model="searchQuery"
          placeholder="Enter location or pin code"
          @input="searchParkingLots"
        />
      </div>

      <!-- Parking Lots -->
      <div class="border border-primary border-2 rounded-3 p-4 mb-4 bg-white">
        <h4 class="text-primary text-center mb-4">Available Parking Lots</h4>
        <div class="table-responsive">
          <table class="table table-bordered border-dark">
            <thead class="table-light">
              <tr>
                <th class="text-center">ID</th>
                <th class="text-center">Address</th>
                <th class="text-center">Availability</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in parkingLots" :key="lot.id">
                <td class="text-center">{{ lot.id }}</td>
                <td class="text-center">{{ lot.location }}</td>
                <td class="text-center">{{ lot.available_spots }}</td>
                <td class="text-center">
                  <RouterLink to="/user/reserve">
                    <button class="btn btn-primary btn-sm px-4 rounded-pill">Book</button>
                  </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ADMIN DASHBOARD -->
    <div v-else-if="role === 'admin'" id="admin-dashboard" class="container mt-4">
      <div class="header d-flex justify-content-between align-items-center p-3 bg-light rounded">
        <h3 class="text-success">Welcome, {{ adminName }}</h3>
        <div>
          <RouterLink to="/dashboard" class="mx-2">Home</RouterLink>
          <RouterLink to="/admin/users" class="mx-2">Users</RouterLink>
          <RouterLink to="/admin/search" class="mx-2">Search</RouterLink>
          <RouterLink to="/admin/summary" class="mx-2">Summary</RouterLink>
          <button class="btn btn-outline-primary btn-sm mx-2" @click="goToProfile">
            Edit Profile
          </button>
          <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
        </div>
      </div>

      <hr />
      <h4 class="text-center my-4 text-primary">Parking Lots</h4>
      <p class="text-danger text-center" v-if="error">{{ error }}</p>
      <p class="text-success text-center" v-if="message">{{ message }}</p>

      <!-- <div class="row">
        <div class="col-md-4 mb-4" v-for="lot in parkingLots" :key="lot.id">
          <div class="card shadow-sm">
            <div class="card-body">
               <h5 class="card-title">🏙 Parking #{{ lot.id }}</h5>
               <p class="text-muted">Address: {{ lot.address }}</p>
               <p class="text-success">Occupied: {{ lot.occupied }}/{{ lot.number_of_spots }}</p>
               <p class="text-success">Spot Status: {{ lot.spot_status }}</p>
                <div class="container mt-4">
                  <h4 class="mb-3 text-center">Parking Spot Status</h4>
                  <div class="row">
                    {% for spot in lot.spot_status %}
                      <div class="col-md-3 col-sm-6 mb-3">
                        <div class="card text-center 
                                    {% if lot.spot_status == 'Available' %} border-success
                                    {% elif lot.spot_status == 'Occupied' %} border-danger
                                    {% elif lot.spot_status == 'Reserved' %} border-warning
                                    {% else %} border-secondary {% endif %}">
                          <div class="card-body">
                            <h5 class="card-title">Spot {{ spot }}</h5>
                            <p class="card-text">
                              <span class="badge 
                                {% if lot.spot_status == 'A' %} bg-success
                                {% elif lot.spot_status == 'O' %} bg-danger
                                {% else %} bg-secondary {% endif %}">
                                {{ spot }}
                              </span>
                            </p>
                          </div>
                        </div>
                      </div>
                    {% endfor %}
                  </div>
                </div>

              <div class="btn-group">
                <button class="btn btn-sm btn-warning" @click="editLot(lot.id)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteLot(lot.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div> -->
      <div class="row">
  <div class="col-md-4 mb-4" v-for="lot in parkingLots" :key="lot.id">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="card-title">🏙 Parking #{{ lot.id }}</h5>
        <p class="text-muted">Address: {{ lot.address }}</p>
        <p class="text-success">Occupied: {{ lot.occupied }}/{{ lot.number_of_spots }}</p>

        <h6 class="mt-3 text-center">Parking Spot Status</h6>
        <div class="d-flex flex-wrap justify-content-center gap-2 mt-2">
          <div
            v-for="(spot, index) in lot.spot_status"
            :key="index"
            class="spot-box"
            :class="{
              'available': spot === 'Available' || spot === 'A',
              'occupied': spot === 'Occupied' || spot === 'O',
              'reserved': spot === 'Reserved' || spot === 'R',
              'unknown': !['Available', 'Occupied', 'Reserved', 'A', 'O', 'R'].includes(spot)
            }"
          >
             <RouterLink :to="`/admin/view-spot/${lot.id}`" style="color: white; text-decoration: none;">
                     {{ spot }}
              </RouterLink>
          </div>
        </div>

        <div class="btn-group mt-3 w-100">
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
  </div>

  <!-- IF NOT LOGGED IN -->
  <div v-else>
    <h1>Please <RouterLink to="/login">Login</RouterLink> to access the dashboard.</h1>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      token: "",
      role: "",
      userData: {},
      parkingLots: [],
      adminName: "Admin",
      message: "",
      error: "",
      searchQuery: "",
    };
  },
  async created() {
    this.loadToken();
    if (this.token) {
      await this.loadUser();
      if (this.role === "admin") await this.loadAdminParkingLots();
      else if (this.role === "user") await this.loadUserParkingLots();
    }
  },
  methods: {
    loadToken() {
      this.token = localStorage.getItem("token") || "";
    },

    async loadUser() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/dashboard", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.role = res.data.role;
        this.userData = res.data;
        if (this.role === "admin") this.adminName = res.data.username;
      } catch (err) {
        this.error = err.response?.data?.message || "Error loading user data.";
      }
    },

    async loadUserParkingLots() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/user/parkinglots", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.parkingLots = res.data;
      } catch (err) {
        this.error = "Failed to load parking lots for user.";
      }
    },

    async loadAdminParkingLots() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/admin/parkinglots", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.parkingLots = res.data;
      } catch (err) {
        this.error = "Failed to load admin parking lots.";
      }
    },

    async deleteLot(id) {
      if (!confirm("Are you sure you want to delete this lot?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/admin/parkinglots/${id}`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.parkingLots = this.parkingLots.filter((lot) => lot.id !== id);
        this.message = "Parking lot deleted successfully!";
      } catch (err) {
        this.error = "Error deleting parking lot.";
      }
    },

    searchParkingLots() {
      if (this.searchQuery.length > 2) {
        this.parkingLots = this.parkingLots.filter((lot) =>
          lot.location.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      } else {
        this.loadUserParkingLots();
      }
    },

    editLot(id) {
      this.$router.push(`/admin/edit-lot/${id}`);
    },
    addLot() {
      this.$router.push("/admin/parkinglots");
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    goToProfile() {
      if (this.role === "admin") this.$router.push("/admin/profile");
      else this.$router.push("/user/profile");
    },
  },
};
</script>

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

.spot-box {
  min-width: 70px;
  padding: 8px 12px;
  border-radius: 8px;
  text-align: center;
  color: #fff;
  font-weight: 600;
  font-size: 0.9rem;
}
.available {
  background-color: rgba(8, 202, 73, 0.89)
}
.occupied {
  background-color: #dc3545; /* Red */
}
.reserved {
  background-color: #ffc107;
  color: #000;
}
.unknown {
  background-color: #6c757d;
}

</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      lotData: {
        locationName: "",
        address: "",
        pnCode: "",
        pricePerHour: "",
        maxSpots: ""
      },
      message: "",
      error: ""
    };
  },
  methods: {
        async addLot() {
    try {
        const payload = {
        prime_location_name: this.lotData.locationName,
        price: parseFloat(this.lotData.pricePerHour),
        address: this.lotData.address,
        pin_code: this.lotData.pinCode,
        number_of_spots: parseInt(this.lotData.maxSpots)
        };

        const res = await axios.post(
        "http://127.0.0.1:5000/admin/parkinglots",
        payload,
        {
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        }
        );

        if (res.status === 201 || res.status === 200) {
         this.message = "Parking lot added successfully!";
         this.error = "";
         this.$router.push("/dashboard");
        }
    } catch (err) {
        this.error = err.response?.data?.message || "Failed to add parking lot.";
    }
    },

    cancel() {
      this.$router.push("/dashboard");
    }
  }
};
</script>

<template>
  <div class="container mt-5">
    <div class="card shadow-lg p-4 rounded-4" style="max-width: 600px; margin: auto;">
      <div class="card-header text-center bg-warning fw-bold fs-5">
        New Parking Lot
      </div>

      <div class="card-body">
        <p class="text-danger text-center" v-if="error">{{ error }}</p>
        <p class="text-success text-center" v-if="message">{{ message }}</p>

        <form @submit.prevent="addLot">
          <div class="mb-3">
            <label class="form-label">Prime Location Name:</label>
            <input
              type="text"
              class="form-control"
              v-model="lotData.locationName"
              required
              placeholder="e.g., Dadar Road"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Address:</label>
            <textarea
              class="form-control"
              rows="3"
              v-model="lotData.address"
              required
              placeholder="Enter full address"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Pin code:</label>
            <input
              type="text"
              class="form-control"
              v-model="lotData.pinCode"
              pattern="[0-9]{6}"
              title="6-digit PIN code"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Price (per hour):</label>
            <input
              type="number"
              class="form-control"
              v-model="lotData.pricePerHour"
              required
              min="1"
              placeholder="e.g., 50"
            />
          </div>

          <div class="mb-4">
            <label class="form-label">Maximum spots:</label>
            <input
              type="number"
              class="form-control"
              v-model="lotData.maxSpots"
              required
              min="1"
              placeholder="e.g., 15"
            />
          </div>

          <div class="text-center">
            <button type="submit" class="btn btn-primary mx-2">Add</button>
            <button type="button" class="btn btn-secondary mx-2" @click="cancel">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 10px;
}
.form-control {
  border-radius: 8px;
}
button {
  min-width: 100px;
}
</style>

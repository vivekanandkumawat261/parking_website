<script>
import axios from "axios";

export default {
  data() {
    return {
      lotData: {
        id: "",
        locationName: "",
        address: "",
        pinCode: "",
        pricePerHour: "",
        maxSpots: ""
      },
      message: "",
      error: ""
    };
  },
  async created() {
    const lotId = this.$route.params.id; // fetch ID from route
    if (lotId) {
      await this.fetchLotData(lotId);
    }
  },
  methods: {
    // 🔹 Fetch existing lot details
    async fetchLotData(id) {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/admin/parkingLots/${id}`, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const data = res.data;
        this.lotData = {
          id: data.id,
          locationName: data.prime_location_name || data.locationName,
          address: data.address,
          pinCode: data.pin_code,
          pricePerHour: data.price,
          maxSpots: data.number_of_spots
        };
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to load parking lot details.";
      }
    },

    // 🔹 Update the existing lot
    async updateLot() {
      try {
        const payload = {
          prime_location_name: this.lotData.locationName,
          address: this.lotData.address,
          pin_code: this.lotData.pinCode,
          price: parseFloat(this.lotData.pricePerHour),
          number_of_spots: parseInt(this.lotData.maxSpots)
        };

        const res = await axios.put(
          `http://127.0.0.1:5000/admin/parkingLots/${this.lotData.id}`,
          payload,
          {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
          }
        );

        if (res.status === 200) {
          this.message = "Parking lot updated successfully!";
          this.error = "";
          setTimeout(() => this.$router.push("/dashboard"), 1200);
        }
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to update parking lot.";
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
      <div class="card-header text-center bg-info fw-bold fs-5">
        Edit Parking Lot
      </div>

      <div class="card-body">
        <p class="text-danger text-center" v-if="error">{{ error }}</p>
        <p class="text-success text-center" v-if="message">{{ message }}</p>

        <form @submit.prevent="updateLot">
          <div class="mb-3">
            <label class="form-label">Prime Location Name:</label>
            <input
              type="text"
              class="form-control"
              v-model="lotData.locationName"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Address:</label>
            <textarea
              class="form-control"
              rows="3"
              v-model="lotData.address"
              required
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Pin Code:</label>
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
            />
          </div>

          <div class="mb-4">
            <label class="form-label">Maximum Spots:</label>
            <input
              type="number"
              class="form-control"
              v-model="lotData.maxSpots"
              required
              min="1"
            />
          </div>

          <div class="text-center">
            <button type="submit" class="btn btn-success mx-2">Update</button>
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

<template>
  <div id="main" class="container mt-4">
    <div class="card shadow">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">Book the Parking Spot</h3>
      </div>
      <div class="card-body">
        <div v-if="message" :class="['alert', alertClass]">{{ message }}</div>

        <form @submit.prevent="reserveSpot">
          <table class="table table-borderless">
            <tbody>
              <tr>
                <td><label class="form-label">Spot ID</label></td>
                <td><input type="text" class="form-control" v-model="form.spot_id" readonly></td>
              </tr>
              <tr>
                <td><label class="form-label">Lot ID</label></td>
                <td>
                  <select class="form-select" v-model="form.lot_id" @change="selectLot">
                    <option value="">-- Select Lot --</option>
                    <option v-for="lot in lots" :key="lot.id" :value="lot.id">
                      Lot {{ lot.id }} - {{ lot.name }}
                    </option>
                  </select>
                </td>
              </tr>
              <tr>
                <td><label class="form-label">User ID</label></td>
                <td><input type="text" class="form-control" v-model="form.user_id" readonly></td>
              </tr>
              <tr>
                <td><label class="form-label">Vehicle Number</label></td>
                <td><input type="text" class="form-control" v-model="form.vehicle_number" required></td>
              </tr>
            </tbody>
          </table>

          <div class="text-center">
            <button type="submit" class="btn btn-success me-2">Reserve</button>
            <button type="button" class="btn btn-secondary" @click="cancelBooking">Cancel</button>
          </div>
        </form>

        <!-- Example: Card Request form (optional if needed on same page) -->
        <hr />
        <h4>Request Card</h4>
        <form @submit.prevent="requestCard">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-control" v-model="formData.fullname" />
          </div>
          <div class="mb-3">
            <label class="form-label">DOB</label>
            <input type="date" class="form-control" v-model="formData.dob" />
          </div>
          <div class="mb-3">
            <label class="form-label">Phone</label>
            <input type="text" class="form-control" v-model="formData.ph" />
          </div>
          <button type="submit" class="btn btn-primary">Request Card</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RequestSpot",
  data() {
    return {
      lots: [],
      form: {
        lot_id: "",
        spot_id: "",
        user_id: localStorage.getItem("user_id") || "",
        vehicle_number: ""
      },
      formData: {
        fullname: "",
        dob: "",
        ph: ""
      },
      message: "",
      alertClass: "alert-info",
      error: ""
    };
  },
  mounted() {
    this.fetchLots();
  },
  methods: {
    // fetch all lots
    async fetchLots() {
      try {
        const response = await axios.get("/user/parkinglots", {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") }
        });
        this.lots = response.data;
      } catch (error) {
        this.message = "❌ Failed to load parking lots";
        this.alertClass = "alert-danger";
      }
    },

    // fetch available spot for selected lot
    async selectLot() {
      if (!this.form.lot_id) return;
      try {
        const response = await axios.get(`/user/available_spot/${this.form.lot_id}`, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") }
        });
        this.form.spot_id = response.data.spot_id;
      } catch {
        this.form.spot_id = "";
        this.message = "❌ No spots available in this lot";
        this.alertClass = "alert-danger";
      }
    },

    // reserve a spot
    async reserveSpot() {
      try {
        const response = await axios.post(
          "/user/reserve",
          {
            lot_id: this.form.lot_id,
            spot_id: this.form.spot_id,
            user_id: this.form.user_id,
            vehicle_number: this.form.vehicle_number
          },
          {
            headers: { Authorization: "Bearer " + localStorage.getItem("token") }
          }
        );
        this.message = `✅ ${response.data.message} (Reservation ID: ${response.data.reservation_id})`;
        this.alertClass = "alert-success";
      } catch (error) {
        this.message = error.response?.data?.message || "❌ Error reserving spot";
        this.alertClass = "alert-danger";
      }
    },

    cancelBooking() {
      this.form.lot_id = "";
      this.form.spot_id = "";
      this.form.vehicle_number = "";
      this.message = "";
    },

    // card request
    async requestCard() {
      try {
        const cardname = this.$route.params.cardname;
        const response = await axios.post(
          `http://127.0.0.1:5000/api/request/${cardname}`,
          this.formData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        );
        console.log(response.data);
        this.message = "✅ Card requested successfully!";
        this.alertClass = "alert-success";
      } catch (err) {
        this.error = err.response?.data?.message || "❌ Failed to request card";
      }
    }
  }
};
</script>

<style scoped>
.card-header {
  font-size: 1.25rem;
}
</style>

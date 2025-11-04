<template>
  <div class="container mt-4">
    <h4 class="text-center text-primary mb-4">Parking Lot #{{ lot.id }}</h4>

    <div class="d-flex flex-wrap justify-content-center gap-2">
      <div
        v-for="(spot, index) in lot.spot_status"
        :key="index"
        class="spot-box"
        :class="{
          available: spot === 'A',
          occupied: spot === 'O',
          reserved: spot === 'R'
        }"
        @click="openModal(index, spot)"
      >
        {{ spot }}
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h5 class="text-center mb-3">View / Delete Parking Spot</h5>
        <p><strong>Spot ID:</strong> {{ selectedSpot.id }}</p>
        <p><strong>Status:</strong> {{ selectedSpot.status }}</p>

        <div class="text-center mt-4">
          <button
            class="btn btn-danger me-2"
            :disabled="selectedSpot.status === 'O'"
            @click="deleteSpot"
          >
            Delete
          </button>
          <button class="btn btn-secondary" @click="closeModal">Close</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger text-center mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lotId: null,
      lot: { id: null, spot_status: [] },
      showModal: false,
      selectedSpot: { id: null, status: '' },
      error: null,
    };
  },

  async mounted() {
    this.lotId = this.$route.params.id;
    await this.getLotDetails();
  },

  methods: {
    async getLotDetails() {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`http://127.0.0.1:5000/api/parkinglot/${this.lotId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error(`Failed to fetch lot: ${res.status}`);
        this.lot = await res.json();
      } catch (err) {
        this.error = err.message;
      }
    },

    openModal(index, status) {
      this.selectedSpot = { id: index + 1, status };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedSpot = { id: null, status: '' };
    },

    async deleteSpot() {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(
          `http://127.0.0.1:5000/api/delete-spot/${this.lot.id}/${this.selectedSpot.id}`,
          { method: "DELETE", headers: { Authorization: `Bearer ${token}` } }
        );

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to delete spot");

        // Update UI immediately
        this.lot.spot_status.splice(this.selectedSpot.id - 1, 1, "A");
        this.closeModal();
        alert("Spot deleted successfully!");
      } catch (err) {
        alert(err.message);
      }
    },
  },
};
</script>

<style scoped>
.spot-box {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.available { background-color: green; }
.occupied { background-color: red; }
.reserved { background-color: orange; }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 350px;
}

.alert { width: 80%; margin: auto; }
</style>

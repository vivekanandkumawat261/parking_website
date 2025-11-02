<template>
  <div>
    <!-- Parking Spots -->
    <div class="d-flex flex-wrap justify-content-center gap-2 mt-2">
      <div
        v-for="(spot, index) in lot.spot_status"
        :key="index"
        class="spot-box"
        :class="{
          'available': spot === 'A',
          'occupied': spot === 'O',
          'reserved': spot === 'R'
        }"
        @click="openModal(index, spot)"
      >
        {{ spot }}
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h5 class="text-center">View/Delete Parking Spot</h5>
        <div class="mt-3">
          <p><strong>ID:</strong> {{ selectedSpot.id }}</p>
          <p><strong>Status:</strong> {{ selectedSpot.status }}</p>
        </div>

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
  </div>
</template>

<script>
export default {
  data() {
    return {
      lot: { id: null, spot_status: [] },
      showModal: false,
      selectedSpot: { id: null, status: '' },
    };
  },
   async mounted() {
    await this.getLotDetails();
  },
  methods: {
   
  
  }
};
</script>

 
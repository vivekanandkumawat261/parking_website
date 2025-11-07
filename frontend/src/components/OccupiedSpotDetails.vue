<template>
  <div>
    <!-- Parking Spots Grid -->
    <div class="d-flex flex-wrap justify-content-center gap-2 mt-3">
      <div
        v-for="(spot, index) in spots"
        :key="index"
        class="spot-box"
        :class="{
          available: spot.status === 'A',
          occupied: spot.status === 'O',
          reserved: spot.status === 'R'
        }"
        @click="showDetails(spot)"
      >
        {{ spot.status }}
      </div>
    </div>

    <!-- Modal for Occupied Spot Details -->
    <div v-if="selectedSpot" class="modal-overlay">
      <div class="modal-box">
        <h3 class="modal-title">Occupied Parking Spot Details</h3>

        <div class="details">
          <p><strong>ID :</strong> {{ selectedSpot.id }}</p>
          <p><strong>Customer ID :</strong> {{ selectedSpot.customerId }}</p>
          <p><strong>Vehicle number :</strong> {{ selectedSpot.vehicleNo }}</p>
          <p><strong>Date/time of parking :</strong> {{ selectedSpot.dateTime }}</p>
          <p><strong>Est. parking cost :</strong> ₹{{ selectedSpot.cost }}</p>
        </div>

        <button class="close-btn" @click="selectedSpot = null">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Example data (replace this with your API data)
const spots = ref([
  { id: 1, status: 'O', customerId: 'C101', vehicleNo: 'TN09AB1234', dateTime: '07/11/2025, 10:45 AM', cost: 120 },
  { id: 2, status: 'A' },
  { id: 3, status: 'R' },
  { id: 4, status: 'O', customerId: 'C205', vehicleNo: 'RJ14BK4455', dateTime: '07/11/2025, 09:15 AM', cost: 200 }
])

const selectedSpot = ref(null)

// show details when clicking on Occupied spots
function showDetails(spot) {
  if (spot.status === 'O') {
    selectedSpot.value = spot
  }
}


// Load parking lot and spots
onMounted(async () => {
  const res = await fetch(`http://127.0.0.1:5000/api/parkinglot/${lotId}`, {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  })
  lot.value = await res.json()
})

// When a spot is clicked
async function showDetails(index) {
  const status = lot.value.spot_status[index]
  if (status !== 'O') return

  const res = await fetch(`http://127.0.0.1:5000/api/parking_spot/${index + 1}`, {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  })
  selectedSpot.value = await res.json()
}
</script>

<style scoped>
/* Spot Boxes */
.spot-box {
  width: 60px;
  height: 60px;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
}

.available {
  background-color: #4caf50;
}
.occupied {
  background-color: #f44336;
}
.reserved {
  background-color: #ff9800;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-box {
  background: #fffefc;
  padding: 20px 30px;
  border-radius: 12px;
  width: 350px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  text-align: left;
}

.modal-title {
  background-color: #ffe59e;
  padding: 8px 10px;
  border-radius: 6px;
  text-align: center;
  font-weight: bold;
  margin-bottom: 15px;
}

.details p {
  margin: 6px 0;
  font-size: 0.95rem;
}

.close-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 6px;
  display: block;
  margin: 15px auto 0;
  cursor: pointer;
  font-weight: 500;
}
.close-btn:hover {
  background-color: #2563eb;
}
</style>


 
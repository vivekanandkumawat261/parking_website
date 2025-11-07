<script setup>
import { ref, onMounted } from 'vue'

const lot = ref({})
const selectedSpot = ref(null)
const lotId = 1  // or get from route param

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

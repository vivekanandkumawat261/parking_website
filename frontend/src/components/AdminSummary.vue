<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4">Admin Summary Dashboard</h2>

    <div class="row">
      <!-- Revenue Chart -->
      <div class="col-md-6">
        <h5 class="text-center mb-3">💰 Revenue from each parking lot</h5>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              dataKey="revenue"
              :data="revenueData"
              nameKey="lot_name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#82ca9d"
              label
            />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <!-- Occupancy Chart -->
      <div class="col-md-6">
        <h5 class="text-center mb-3">🚗 Parking Lot Occupancy Summary</h5>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart :data="occupancyChartData">
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// import api from '../api'
// import {
//   PieChart, Pie, Tooltip,
//   BarChart, Bar, XAxis, YAxis, ResponsiveContainer
// } from 'recharts'

const revenueData = ref([])
const occupancyChartData = ref([])

async function loadSummary() {
  try {
    const res = await api.get('/admin/summary/stats')
    revenueData.value = res.data.revenue
    const occ = res.data.occupancy
    occupancyChartData.value = [
      { name: 'Available', count: occ.available },
      { name: 'Occupied', count: occ.occupied }
    ]
  } catch (err) {
    console.error(err)
  }
}

onMounted(loadSummary)
</script>

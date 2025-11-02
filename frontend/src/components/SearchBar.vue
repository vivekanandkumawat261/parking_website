<template>
 
  <div class="search-bar">
    <label class="fw-bold me-2">Search by:</label>
    <select v-model="searchBy" class="form-select d-inline-block w-auto me-2">
      <option value="location">Location</option>
      <option value="id">Parking Lot ID</option>
    </select>
    <input
      v-model="searchString"
      type="text"
      placeholder="Enter search query..."
      class="form-control d-inline-block w-auto me-2"
    />
    <button class="btn btn-primary" @click="onSearch">Search</button>
  </div>
</template>

<script setup>
import { ref } from 'vue' 
const emit = defineEmits(['search']);
const searchBy = ref('location');
const searchString = ref('');

function onSearch() {
  emit('search', { searchBy: searchBy.value, searchString: searchString.value });
}
</script>

<style>
.search-bar {
  margin: 20px;
  display: flex;
  align-items: center;
}
</style>

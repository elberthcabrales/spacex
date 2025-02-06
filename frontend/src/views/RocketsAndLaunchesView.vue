<template>
  <div class="dashboard-container p-4">
    <h1 class="text-3xl font-bold mb-6">Launches and rockets</h1>
    <!-- Use the RocketList component here -->
    <LaunchList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LaunchList from '@/components/LaunchList.vue';
// Update the import path according to your folder structure

export default defineComponent({
  name: 'RocetsAndLaunchesView',
  components: {
    LaunchList
  }
});
</script>

<style scoped>
/* Add any custom styling for your dashboard here */
</style>

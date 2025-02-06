<template>
  <div class="dashboard-container p-4">
    <h1 class="text-3xl font-bold mb-10">Dashboard</h1>
    <!-- Use the RocketList component here -->
    <DashboardChart />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import DashboardChart from '@/components/DashboardChart.vue';
// Update the import path according to your folder structure

export default defineComponent({
  name: 'DashboardView',
  components: {
    DashboardChart
  }
});
</script>

<style scoped>
/* Add any custom styling for your dashboard here */
</style>

<template>
  <div class="dashboard-container p-4">
    <h1 class="text-3xl font-bold mb-20">Dashboard</h1>
    <!-- Use the RocketList component here -->
    <div
      class="chart-container bg-gradient-to-br from-gray-800 via-gray-900 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
      <DashboardChart />
    </div>

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

<template>
  <div class="dashboard-container p-4">
    <h1 class="text-3xl font-bold mb-10">Launches and rockets</h1>
    <LaunchList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import LaunchList from '@/components/LaunchList.vue';

export default defineComponent({
  name: 'RocketsAndLaunchesView',
  components: {
    LaunchList
  }
});
</script>

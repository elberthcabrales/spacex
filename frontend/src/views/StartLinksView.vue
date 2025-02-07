<template>
  <div class="dashboard-container p-4">
    <h1 class="text-3xl font-bold mb-10">Starlinks</h1>
    <StarlinkList />

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import StarlinkList from '@/components/StarlinkList.vue';

export default defineComponent({
  name: 'StarlinksView',
  components: {
    StarlinkList
  }
});
</script>

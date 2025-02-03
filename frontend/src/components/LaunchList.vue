<template>
    <div class="p-4">
        <h2 class="text-2xl font-bold mb-4">Launches</h2>
        <div v-if="loading" class="text-center">Loading...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="launch in launches" :key="launch.id" class="border p-4 rounded-lg shadow-md">
                <h3 class="text-xl font-semibold">{{ launch.name }}</h3>
                <p class="text-gray-600">{{ launch.details }}</p>
                <p class="text-sm text-gray-500">{{ new Date(launch.date_utc).toLocaleDateString() }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

interface Launch {
    id: string;
    name: string;
    details: string;
    date_utc: string;
}

export default defineComponent({
    setup() {
        const launches = ref<Launch[]>([]);
        const loading = ref(true);

        onMounted(async () => {
            try {
                const response = await fetch('https://api.spacexdata.com/v4/launches');
                launches.value = await response.json();
            } catch (error) {
                console.error('Error fetching launches:', error);
            } finally {
                loading.value = false;
            }
        });

        return { launches, loading };
    },
});
</script>
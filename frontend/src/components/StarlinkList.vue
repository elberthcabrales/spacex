<template>
    <div class="p-4">
        <h2 class="text-2xl font-bold mb-4">Starlink Satellites</h2>
        <div v-if="loading" class="text-center">Loading...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="satellite in satellites" :key="satellite.id" class="border p-4 rounded-lg shadow-md">
                <h3 class="text-xl font-semibold">{{ satellite.spaceTrack.OBJECT_NAME }}</h3>
                <p class="text-gray-600">Launch Date: {{ new Date(satellite.launch_date_utc).toLocaleDateString() }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

interface Starlink {
    id: string;
    spaceTrack: {
        OBJECT_NAME: string;
    };
    launch_date_utc: string;
}

export default defineComponent({
    setup() {
        const satellites = ref<Starlink[]>([]);
        const loading = ref(true);

        onMounted(async () => {
            try {
                const response = await fetch('https://api.spacexdata.com/v4/starlink');
                satellites.value = await response.json();
            } catch (error) {
                console.error('Error fetching Starlink satellites:', error);
            } finally {
                loading.value = false;
            }
        });

        return { satellites, loading };
    },
});
</script>
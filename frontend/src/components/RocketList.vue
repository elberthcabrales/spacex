<template>
    <div class="bg-space-gradient min-h-screen p-8 text-white">
        <!-- Search + Pagination Controls -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <!-- Search Filter -->
            <div class="mb-4 md:mb-0">
                <label for="search" class="mr-2 uppercase text-sm tracking-wide">Search:</label>
                <input type="text" id="search" v-model="searchQuery" placeholder="Rocket name..."
                    class="bg-white/20 border border-white/30 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-white/50 transition" />
            </div>

            <!-- Pagination -->
            <div class="flex items-center">
                <button class="bg-white/10 px-4 py-1 rounded mr-2 disabled:opacity-50 hover:bg-white/20 transition"
                    :disabled="currentPage === 1" @click="prevPage">
                    Previous
                </button>
                <span class="mr-2">
                    Page {{ currentPage }} / {{ totalPages }}
                </span>
                <button class="bg-white/10 px-4 py-1 rounded disabled:opacity-50 hover:bg-white/20 transition"
                    :disabled="currentPage === totalPages" @click="nextPage">
                    Next
                </button>
            </div>
        </div>

        <!-- Loading Indicator -->
        <div v-if="loading" class="text-center text-lg font-semibold">
            Loading...
        </div>

        <!-- Data Table -->
        <div v-else class="overflow-x-auto rounded-lg shadow-lg bg-white/10 border border-white/20">
            <table class="table-auto w-full text-sm text-gray-200">
                <thead>
                    <tr class="bg-white/10 text-gray-300 uppercase text-xs tracking-wider">
                        <th class="px-6 py-3 text-left border-b border-white/20">ID</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Name</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Description</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="rocket in paginatedRockets" :key="rocket.id" class="hover:bg-white/5 transition-colors">
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ rocket.id }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ rocket.name }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ rocket.description }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            <a :href="rocket.wikipedia" target="_blank" class="text-blue-400 hover:underline">
                                Learn More
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Bottom Pagination (Optional) -->
        <div class="flex justify-end items-center mt-4">
            <button class="bg-white/10 px-4 py-1 rounded mr-2 disabled:opacity-50 hover:bg-white/20 transition"
                :disabled="currentPage === 1" @click="prevPage">
                Previous
            </button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button class="bg-white/10 px-4 py-1 rounded ml-2 disabled:opacity-50 hover:bg-white/20 transition"
                :disabled="currentPage === totalPages" @click="nextPage">
                Next
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';

// 1. Interface describing a single rocket
interface Rocket {
    id: number;
    name: string;
    description: string;
    wikipedia: string;
}

export default defineComponent({
    name: 'RocketList',
    setup() {
        // 2. Reactive references
        const rockets = ref<Rocket[]>([]);
        const loading = ref<boolean>(true);

        // Pagination & search states
        const searchQuery = ref<string>('');
        const currentPage = ref<number>(1);
        const pageSize = ref<number>(2); // Items per page

        // 3. Mock data
        const mockRockets: Rocket[] = [
            {
                id: 1,
                name: 'Falcon 1',
                description: 'The first orbital rocket developed by SpaceX. It is now retired.',
                wikipedia: 'https://en.wikipedia.org/wiki/Falcon_1',
            },
            {
                id: 2,
                name: 'Falcon 9',
                description: 'A partially reusable two-stage-to-orbit medium-lift launch vehicle.',
                wikipedia: 'https://en.wikipedia.org/wiki/Falcon_9',
            },
            {
                id: 3,
                name: 'Falcon Heavy',
                description: 'Currently the most powerful operational rocket in the world.',
                wikipedia: 'https://en.wikipedia.org/wiki/Falcon_Heavy',
            },
            {
                id: 4,
                name: 'Starship',
                description: 'A fully-reusable launch vehicle under development by SpaceX.',
                wikipedia: 'https://en.wikipedia.org/wiki/SpaceX_Starship',
            },
            {
                id: 5,
                name: 'Big Falcon Rocket',
                description: 'An earlier concept name for Starship.',
                wikipedia: 'https://en.wikipedia.org/wiki/SpaceX_Starship',
            },
            // Add more if needed
        ];

        // 4. Simulate fetching data
        onMounted(() => {
            setTimeout(() => {
                rockets.value = mockRockets;
                loading.value = false;
            }, 500);
        });

        // 5. Computed property: filter rockets by search
        const filteredRockets = computed<Rocket[]>(() => {
            if (!searchQuery.value) {
                return rockets.value;
            }
            return rockets.value.filter((rocket) =>

                rocket.name.toLowerCase().includes(searchQuery.value.toLowerCase())
            );
        });

        // 6. Compute total pages
        const totalPages = computed<number>(() => {
            return Math.ceil(filteredRockets.value.length / pageSize.value);
        });

        // 7. Paginate the results
        const paginatedRockets = computed<Rocket[]>(() => {
            const startIndex = (currentPage.value - 1) * pageSize.value;
            const endIndex = startIndex + pageSize.value;
            return filteredRockets.value.slice(startIndex, endIndex);
        });

        // 8. Pagination methods
        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
            }
        };
        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
            }
        };

        return {
            rockets,
            loading,
            searchQuery,
            currentPage,
            pageSize,
            totalPages,
            paginatedRockets,
            prevPage,
            nextPage,
        };
    },
});
</script>

<style scoped>
/* Use your existing Tailwind setup, but add a custom gradient class */
.bg-space-gradient {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
</style>
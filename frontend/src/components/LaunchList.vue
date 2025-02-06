<template>
    <div class="bg-space-gradient min-h-screen p-8 text-white">
        <!-- Search + Pagination Controls -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <!-- Search Filter -->
            <div class="mb-4 md:mb-0">
                <label for="search" class="mr-2 uppercase text-sm tracking-wide">Search:</label>
                <input type="text" id="search" v-model="searchQuery" placeholder="Mission name..."
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
                        <th class="px-6 py-3 text-left border-b border-white/20">Image</th>
                        <th @click="handleSort('mission_name')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">
                            Mission Name
                            <span v-if="sortColumn === 'mission_name'">{{ sortOrder === "asc" ? "▲" : "▼" }}</span>
                        </th>
                        <th @click="handleSort('details')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">
                            Details
                            <span v-if="sortColumn === 'details'">{{ sortOrder === "asc" ? "▲" : "▼" }}</span>
                        </th>
                        <th @click="handleSort('upcoming')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">
                            Upcoming
                            <span v-if="sortColumn === 'upcoming'">{{ sortOrder === "asc" ? "▲" : "▼" }}</span>
                        </th>
                        <th @click="handleSort('success')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">
                            Success
                            <span v-if="sortColumn === 'success'">{{ sortOrder === "asc" ? "▲" : "▼" }}</span>
                        </th>
                        <th @click="handleSort('rocket.name')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">
                            Rocket
                            <span v-if="sortColumn === 'rocket.name'">{{ sortOrder === "asc" ? "▲" : "▼" }}</span>
                        </th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="launch in paginatedLaunches" :key="launch.mission_name"
                        class="hover:bg-white/5 transition-colors">
                        <td class="px-6 py-4 border-b border-white/10">
                            <img v-if="launch.image" :src="launch.image" alt="Launch Image"
                                class="w-12 h-12 object-cover rounded-md" />
                            <span v-else class="text-gray-400">No Image</span>
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ launch.mission_name || "N/A" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ launch.details || "N/A" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            <span :class="[launch.upcoming ? 'text-blue-400' : 'text-gray-400']">
                                {{ launch.upcoming ? "Yes" : "No" }}
                            </span>
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            <span :class="[launch.success ? 'text-green-400' : 'text-red-400']">
                                {{ launch.success ? "Yes" : "No" }}
                            </span>
                        </td>
                        <td class="px-6 py-4 border-b border-white/10 cursor-pointer text-blue-400 hover:underline"
                            @click="fetchRocketDetails(launch.rocket.rocket_uuid)">
                            {{ launch.rocket?.name || "N/A" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            <a v-if="launch.article" :href="launch.article" target="_blank"
                                class="text-blue-400 hover:underline">
                                Learn More
                            </a>
                            <span v-else>N/A</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!-- Rocket Modal -->
        <RocketModal :isOpen="isModalOpen" :rocket="selectedRocket" @close="closeModal" />
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
import { defineComponent, ref, onMounted, computed, watch } from 'vue';
import RocketModal from '@/components/RocketModal.vue';
import axios from 'axios';

// Interface describing a single launch
// Interface describing detailed rocket data
interface Rocket {
    name: string;
    active: boolean;
    wikipedia: string;
    weight: string;
    height: number;
    diameter: number;
    cost_per_launch: number;
    first_flight: string;
    country: string;
    stages: number;
}

interface Launch {
    mission_name: string | null;
    details: string | null;
    upcoming: boolean | null;
    success: boolean | null;
    image: string | null;
    webcast: string | null;
    article: string | null;
    rocket: Rocket,
    failures: {
        time: number;
        reason: string;
    }[];
}

export default defineComponent({
    name: 'LaunchedList',
    components: {
        RocketModal,
    },
    setup() {
        // Reactive references
        const launches = ref<Launch[]>([]);
        const totalRecords = ref<number>(0);
        const loading = ref<boolean>(true);
        const searchQuery = ref<string>('');
        const currentPage = ref<number>(1);
        const pageSize = ref<number>(7);
        const sortColumn = ref<string>('mission_name'); // Default sort column
        const sortOrder = ref<'asc' | 'desc'>('asc'); // Default sort order
        const isModalOpen = ref<boolean>(false);
        const selectedRocket = ref<Rocket | null>(null);

        // Fetch data from API
        const fetchLaunches = async () => {
            try {
                const params = {
                    skip: (currentPage.value - 1) * pageSize.value,
                    limit: pageSize.value,
                    mission_name: searchQuery.value || undefined,
                    details: undefined, // Add if needed
                    sort_by: sortColumn.value,
                    order: sortOrder.value,
                };

                const response = await axios.get('http://127.0.0.1:8000/api/launches', { params });
                const responseData = response.data;

                launches.value = responseData.data;
                totalRecords.value = responseData.total; // Update total records
                loading.value = false;
            } catch (error) {
                console.error('Error fetching launches:', error);
                loading.value = false;
            }
        };

        // Fetch rocket details
        const fetchRocketDetails = async (rocket_uuid: string) => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/rockets?rocket_uuid=${rocket_uuid}`);
                selectedRocket.value = response.data.data[0]; // Assuming the API returns an array
                isModalOpen.value = true;
            } catch (error) {
                console.error('Error fetching rocket details:', error);
            }
        };

        // Close modal
        const closeModal = () => {
            isModalOpen.value = false;
            selectedRocket.value = null;
        };

        watch(searchQuery, () => {
            currentPage.value = 1; // Reset to first page when search query changes
            fetchLaunches(); // Refetch data with new search query
        });
        // Computed property: total pages
        const totalPages = computed<number>(() => {
            return Math.ceil(totalRecords.value / pageSize.value);
        });

        // Paginate the results
        const paginatedLaunches = computed<Launch[]>(() => {
            return launches.value;
        });

        // Sorting handler
        const handleSort = (column: string) => {
            if (sortColumn.value === column) {
                sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
            } else {
                sortColumn.value = column;
                sortOrder.value = "asc";
            }
            currentPage.value = 1; // Reset to first page when sorting changes
            fetchLaunches(); // Refetch data with new sorting
        };

        // Pagination methods
        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
                fetchLaunches(); // Refetch data for the previous page
            }
        };

        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
                fetchLaunches(); // Refetch data for the next page
            }
        };

        // Fetch data on component mount
        onMounted(() => {
            fetchLaunches();
        });

        return {
            launches,
            totalRecords,
            loading,
            searchQuery,
            currentPage,
            pageSize,
            totalPages,
            paginatedLaunches,
            sortColumn,
            sortOrder,
            handleSort,
            prevPage,
            nextPage,
            fetchRocketDetails,
            closeModal,
            isModalOpen,
            selectedRocket,
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
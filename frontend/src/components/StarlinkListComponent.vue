<template>
    <div class="bg-space-gradient min-h-screen p-8 text-white">
        <!-- Search + Pagination Controls -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <!-- Search Filter -->
            <div class="mb-4 md:mb-0">
                <label for="search" class="mr-2 uppercase text-sm tracking-wide">Search by Name:</label>
                <input type="text" id="search" v-model="searchQuery" placeholder="Starlink name..."
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
                        <th @click="handleSort('name')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">Name</th>
                        <th @click="handleSort('creation_date')"
                            class="px-6 py-3 text-left border-b border-white/20 cursor-pointer">Creation Date</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Launch date</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Cost per launch</th>
                        <th class="px-6 py-3 text-left border-b border-white/20">Rocket</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="starlink in paginatedStarlinks" :key="starlink.starlink_uuid"
                        class="hover:bg-white/5 transition-colors">
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ starlink.name || "No name" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ starlink.creation_date || "No date" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ starlink.rocket.first_flight || "No launched" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ starlink.rocket.cost_per_launch || "N/A" }}
                        </td>
                        <td class="px-6 py-4 border-b border-white/10">
                            {{ starlink.rocket?.name || "N/A" }}
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
import { defineComponent, ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';

// Interface describing a single Starlink
interface Starlink {
    starlink_uuid: string;
    name: string | null;
    creation_date: string | null;
    country_code: string | null;
    rocket: {
        rocket__uuid: string;
        name: string;
        cost_per_launch: number;
        first_flight: string;
        active: boolean;
    };
}

export default defineComponent({
    name: 'StarlinkList',
    setup() {
        // Reactive references
        const starlinks = ref<Starlink[]>([]);
        const totalRecords = ref<number>(0);
        const loading = ref<boolean>(true);
        const searchQuery = ref<string>('');
        const sortColumn = ref<string>('name');
        const sortOrder = ref<'asc' | 'desc'>('asc');
        const currentPage = ref<number>(1);
        const pageSize = ref<number>(10); // Items per page

        // Fetch data from API
        const fetchStarlinks = async () => {
            try {
                const params = {
                    skip: (currentPage.value - 1) * pageSize.value,
                    limit: pageSize.value,
                    name: searchQuery.value || undefined,
                    sort_by: sortColumn.value,
                    order: sortOrder.value,
                };

                const response = await axios.get('http://127.0.0.1:8000/api/starlinks/', { params });
                const responseData = response.data;

                starlinks.value = responseData.data;
                totalRecords.value = responseData.total; // Update total records
                loading.value = false;
            } catch (error) {
                console.error('Error fetching starlinks:', error);
                loading.value = false;
            }
        };

        watch(searchQuery, () => {
            currentPage.value = 1; // Reset to first page when search query changes
            fetchStarlinks(); // Refetch data with new search query
        });

        const handleSort = (column: string) => {
            if (column === sortColumn.value) {
                sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn.value = column;
                sortOrder.value = 'asc';
            }
            currentPage.value = 1; // Reset to first page when sorting changes
            fetchStarlinks();
        };

        // Computed property: total pages
        const totalPages = computed<number>(() => {
            return Math.ceil(totalRecords.value / pageSize.value);
        });

        // Paginate the results
        const paginatedStarlinks = computed<Starlink[]>(() => {
            return starlinks.value;
        });

        // Pagination methods
        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
                fetchStarlinks(); // Refetch data for the previous page
            }
        };

        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
                fetchStarlinks(); // Refetch data for the next page
            }
        };

        // Watch for changes in searchQuery
        watch(searchQuery, () => {
            currentPage.value = 1; // Reset to first page when search query changes
            fetchStarlinks(); // Refetch data with new search query
        });

        // Fetch data on component mount
        onMounted(() => {
            fetchStarlinks();
        });

        return {
            starlinks,
            totalRecords,
            loading,
            searchQuery,
            currentPage,
            pageSize,
            totalPages,
            paginatedStarlinks,
            prevPage,
            nextPage,
            handleSort,
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
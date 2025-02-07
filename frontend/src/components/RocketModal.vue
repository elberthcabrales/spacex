<template>
    <div v-if="isOpen" class="fixed inset-0 bg-black/70 flex justify-center items-center z-50">
        <div class="bg-black/90 p-8 rounded-lg shadow-2xl max-w-md w-full text-white space-y-6">
            <h2 class="text-2xl font-bold text-center text-blue-400">{{ rocket?.name }}</h2>

            <div class="space-y-4">
                <p class="flex justify-between">
                    <span class="font-medium">Active:</span>
                    <span :class="[rocket?.active ? 'text-green-400' : 'text-red-400']">
                        {{ rocket?.active ? 'Yes' : 'No' }}
                    </span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Wikipedia:</span>
                    <a :href="rocket?.wikipedia" target="_blank" class="text-blue-400 hover:underline">
                        Link
                    </a>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Weight:</span>
                    <span>{{ rocket?.weight }} kg</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Height:</span>
                    <span>{{ rocket?.height }} m</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Diameter:</span>
                    <span>{{ rocket?.diameter }} m</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Cost Per Launch:</span>
                    <span>${{ rocket?.cost_per_launch.toLocaleString() }}</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">First Flight:</span>
                    <span>{{ rocket?.first_flight }}</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Country:</span>
                    <span>{{ rocket?.country }}</span>
                </p>
                <p class="flex justify-between">
                    <span class="font-medium">Stages:</span>
                    <span>{{ rocket?.stages }}</span>
                </p>
            </div>

            <!-- Close Button -->
            <button @click="closeModal"
                class="w-full py-3 px-6 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition duration-300">
                Close
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

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

export default defineComponent({
    name: 'RocketModal',
    props: {
        isOpen: {
            type: Boolean,
            required: true,
        },
        rocket: {
            type: Object as PropType<Rocket | null>,
            required: false,
            default: null,
        },
    },
    emits: ['close'],
    setup(props, { emit }) {
        const closeModal = () => {
            emit('close');
        };

        return {
            closeModal,
        };
    },
});
</script>

<style scoped>
.bg-space-gradient {
    background: linear-gradient(135deg, #f4f4f8, #302b63, #24243e);
}
</style>
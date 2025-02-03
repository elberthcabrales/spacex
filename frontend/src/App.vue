<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="min-h-screen bg-space-gradient text-white font-space-mono">
    <!-- Navigation Bar -->
    <header class="bg-black/90 backdrop-blur-md shadow-lg fixed w-full z-50">
      <div class="container mx-auto flex justify-between items-center p-4">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold text-blue-400 font-orbitron">SpaceX Viewer</span>
        </RouterLink>

        <!-- Navigation Links -->
        <nav class="flex space-x-6">
          <RouterLink to="/" class="text-gray-300 hover:text-blue-400 transition-colors duration-300 font-orbitron"
            active-class="text-blue-400 font-bold">
            Launches
          </RouterLink>
          <RouterLink to="/lunches-and-rockets"
            class="text-gray-300 hover:text-blue-400 transition-colors duration-300 font-orbitron"
            active-class="text-blue-400 font-bold">
            Rockets & Launches
          </RouterLink>
          <RouterLink to="/start-links"
            class="text-gray-300 hover:text-blue-400 transition-colors duration-300 font-orbitron"
            active-class="text-blue-400 font-bold">
            Starlinks
          </RouterLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="pt-20">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Custom gradient for space theme */
.bg-space-gradient {
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

/* Apply custom fonts */
.font-orbitron {
  font-family: 'Orbitron', sans-serif;
}

.font-space-mono {
  font-family: 'Space Mono', monospace;
}
</style>
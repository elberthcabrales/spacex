import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import RocketsAndLaunchesView from '@/views/RocketsAndLaunchesView.vue'
import StartLinksView from '@/views/StartLinksView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DashboardView,
    },
    {
      path: '/lunches-and-rockets',
      name: '',
      component: RocketsAndLaunchesView,
    },
    {
      path: '/start-links',
      name: 'start-links',
      component: StartLinksView,
    },
  ],
})

export default router

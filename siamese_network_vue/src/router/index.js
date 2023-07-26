import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import GalleryView from '../views/GalleryView.vue'
import IdentifyView from '../views/IdentifyView.vue'
import ImageDetailsView from '../views/ImageDetailsView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/gallery',
    name: 'gallery',
    component: GalleryView
  },
  {
    path: '/identify',
    name: 'identify',
    component: IdentifyView
  },
  {
    path: '/imageDetails',
    name: 'imageDetails',
    component: ImageDetailsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

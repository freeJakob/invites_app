import Vue from 'vue'
import VueRouter from 'vue-router'
import Map from '../views/Map.vue'
import Boarding from '../views/Boarding.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/map',
    name: 'Map',
    component: Map
  },
  {
    path: '/boarding',
    name: 'Boarding',
    component: Boarding
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

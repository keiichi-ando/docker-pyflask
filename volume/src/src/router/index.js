import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Store from '../store/index.js'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // require login example
  // {
  //   path: '/jobs',
  //   name: 'Jobs',
  //   component: () => import('../views/Jobs.vue'),
  //   meta: { requiresAuth: true, authRole: 'manager' }
  // },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Logout.vue')
  },
  // otherwise redirect to home
  { path: '*', redirect: '/' }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const { authRole } = to.meta
  const currentTeam = Store.state.userTeam
  const authRequired = (to.name !== 'Login' && to.matched.some(record => record.meta.requiresAuth))
  if (authRequired && !Store.getters.isAuthenticated) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }
  if (authRole) {
    if (authRole.length && !authRole.includes(currentTeam)) {
      return next({ path: '/' })
    }
  }
  next()
})

export default router

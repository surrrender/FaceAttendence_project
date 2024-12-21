import { createRouter, createWebHistory } from 'vue-router';
// import Home from './views/Home.vue';
// import About from './views/About.vue';
import RegisterFaces from '@/components/RegisterFaces.vue';
import Register from '@/components/Register.vue';
import Login from '@/components/Login.vue';

const routes = [
  // { path: '/', component: Home },
  // { path: '/about', component: About },
  { path:'/RegisterFaces',component: RegisterFaces},
  { path:'/Register',component: Register},
  { path:'/Login',component: Login}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

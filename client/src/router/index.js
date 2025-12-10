import { createRouter, createWebHistory } from 'vue-router';
import GameCRUD from '../components/GameCRUD.vue';
import DeveloperCRUD from '../components/DeveloperCRUD.vue';
import UserProfileCRUD from '../components/UserProfileCRUD.vue';
import PurchaseCRUD from '../components/PurchaseCRUD.vue';
import ReviewCRUD from '../components/ReviewCRUD.vue';

const routes = [
  { path: '/games', component: GameCRUD },
  { path: '/developers', component: DeveloperCRUD },
  { path: '/profiles', component: UserProfileCRUD },
  { path: '/purchases', component: PurchaseCRUD },
  { path: '/reviews', component: ReviewCRUD },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import ItemList from '../views/ItemList.vue';
import ItemDetail from '../views/ItemDetail.vue';
import CustomerList from '../views/CustomerList.vue';
import CustomerDetail from '../views/CustomerDetail.vue';
import HomePage from '../views/HomePage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/items',
    name: 'ItemList',
    component: ItemList,
  },
  {
    path: '/items/new',
    name: 'ItemNew',
    component: ItemDetail,
  },
  {
    path: '/items/:id',
    name: 'ItemDetail',
    component: ItemDetail,
  },
  {
    path: '/customers',
    name: 'CustomerList',
    component: CustomerList,
  },
  {
    path: '/customers/new',
    name: 'CustomerNew',
    component: CustomerDetail,
  },
  {
    path: '/customers/:id',
    name: 'CustomerDetail',
    component: CustomerDetail,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

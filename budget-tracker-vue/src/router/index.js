import {createRouter, createWebHistory} from 'vue-router';
import HomeView from '../views/MainView.vue';
import AboutView from '../views/AboutView.vue';
import AuthView from '../views/AuthView.vue';
import Transact from "@/views/TransactionsView.vue";
import AddTransactionView from "@/views/AddTransactionView.vue";
import AddTargetView from "@/views/AddTargetView.vue";
import AddLimitView from "@/views/AddLimitView.vue";
import TargetListView from "@/views/TargetListView.vue"
import EditLimit from "@/components/EditLimit.vue";
import EditTarget from "@/components/EditTarget.vue";
import EditTransaction from "@/components/EditTransaction.vue";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/login',
            name: 'login',
            component: AuthView
        },
        {
            path: '/transactions',
            name: 'Transact',
            component: Transact,
            meta: {
                requiresAuth: true,
            },
        },

        {
            path: '/register',
            name: 'register',
            component: AuthView
        },
        {
            path: '/add_transaction',
            name: 'add_transaction',
            component: AddTransactionView
        },
        {
            path: '/create_target',
            name: 'create_target',
            component: AddTargetView
        },
        {
            path: '/create_limit',
            name: 'create_limit',
            component: AddLimitView
        },
        {
            path: '/target-list',
            name: 'target-list',
            component: TargetListView
        },
        {
            path: '/edit_limit',
            name: 'Edit_limit',
            component: EditLimit
        },
        {
            path: '/edit_target/:targetId',
            name: 'Edit_target',
            component: EditTarget
        },
         {
            path: '/edit_transaction/:transactionId',
            name: 'Edit_transaction',
            component: EditTransaction
        },
    ]
});

export default router;

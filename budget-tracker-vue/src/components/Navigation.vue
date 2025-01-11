<template>
  <nav>
    <ul v-if="isLoggedIn">
      <li><router-link to="/">Главная</router-link></li>
      <li><router-link to="/transactions">Транзакции</router-link></li>
      <li><router-link @click="logout" to="/">Выйти</router-link></li>
      <li><router-link to="/target-list">Цели</router-link></li>
    </ul>
  </nav>
</template>

<script>
import { useUserStore } from "@/stores/user.js";
import { computed } from "vue";
import router from "@/router/index.js";

export default {
  name: 'Navigation',
  setup() {
    const userStore = useUserStore();

    const isLoggedIn = computed(() => userStore.isAuthenticated);
    const logout = async () => {
      try {
        await userStore.logout();
        router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    return {
      isLoggedIn,
      logout
    };
  }
}
</script>

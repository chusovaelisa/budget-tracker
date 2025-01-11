<template>
  <div v-if="isLoggedIn" class="app-container">
    <Aside />
    <div class="content-container">
      <router-view />
    </div>
  </div>
  <div v-else>
    <AuthView />
  </div>
</template>

<script>
import Aside from "@/components/Aside.vue";
import AuthView from "@/views/AuthView.vue";
import { useUserStore } from "@/stores/user.js";
import { computed, onMounted, onUnmounted } from "vue";

export default {
  components: { Aside, AuthView },
  setup() {
    const userStore = useUserStore();
    const isLoggedIn = computed(() => userStore.isAuthenticated);

    onMounted(() => {
      if (isLoggedIn.value) {
        userStore.startTokenRefreshInterval();
      }
    });

    onUnmounted(() => {
      userStore.stopTokenRefreshInterval();
    });

    return {
      isLoggedIn
    };
  },
}
</script>

<style scoped>
.app-container {
  display: grid;
  grid-template-columns: 210px 1fr;
  height: 100vh;
}

.content-container {
  padding: 20px;
  overflow-y: auto;
}
</style>
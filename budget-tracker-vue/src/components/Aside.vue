<template>
  <aside>
    <div class="toggle">
      <div class="site-name">
        <svg class="site-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 88">
          <path
              d="M40 32a12 12 0 1 0 12 12 12.013 12.013 0 0 0-12-12zm0 22a10 10 0 1 1 10-10 10.011 10.011 0 0 1-10 10z"
              style="fill:#22c3e6"/>
          <path
              d="M42 41a1 1 0 0 0 2 0 3.003 3.003 0 0 0-3-3v-1a1 1 0 0 0-2 0v1a3.003 3.003 0 0 0-3 3v.559a2.997 2.997 0 0 0 2.05 2.846l.95.316V48a1 1 0 0 1-1-1 1 1 0 0 0-2 0 3.003 3.003 0 0 0 3 3v1a1 1 0 0 0 2 0v-1a3.003 3.003 0 0 0 3-3v-.559a2.997 2.997 0 0 0-2.05-2.846L41 43.28V40a1 1 0 0 1 1 1zm-.684 4.493a.998.998 0 0 1 .684.948V47a1 1 0 0 1-1 1v-2.613zM39 42.613l-.316-.106A.998.998 0 0 1 38 41.56V41a1 1 0 0 1 1-1zM21 41a3 3 0 1 0 3 3 3.003 3.003 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1zM59 41a3 3 0 1 0 3 3 3.003 3.003 0 0 0-3-3zm0 4a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"
              style="fill:#22c3e6"/>
          <path
              d="M84 31.4V15a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v5H3a1 1 0 0 0-1 1v46a1 1 0 0 0 1 1h65v2c0 2.626 4.527 4 9 4s9-1.374 9-4V34a3.12 3.12 0 0 0-2-2.6zm0 29.207V64c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.16 16.16 0 0 0 77 62a16.15 16.15 0 0 0 7-1.393zM77 32c3.049 0 7 1 7 2 0 .58-2.453 2-7 2s-7-1.42-7-2c.44-1.482 5.145-2 7-2zm-9 21.934A8.955 8.955 0 0 0 63.055 61h-46.11A9.017 9.017 0 0 0 9 53.055v-18.11A9.017 9.017 0 0 0 16.944 27h46.113A9.041 9.041 0 0 0 68 34.057zm16 .673V58c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.147 16.147 0 0 0 77 56a16.158 16.158 0 0 0 7-1.393zm0-6V52c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.147 16.147 0 0 0 77 50a16.15 16.15 0 0 0 7-1.393zm0-6V46c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.147 16.147 0 0 0 77 44a16.149 16.149 0 0 0 7-1.393zm0-6V40c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.147 16.147 0 0 0 77 38a16.162 16.162 0 0 0 7-1.393zM10 16h72v14.617a19.317 19.317 0 0 0-4-.595V21a1 1 0 0 0-1-1H10zM4 66V22h72v8.023c-2.218.103-5.594.642-7.172 2.192A7.007 7.007 0 0 1 65 26a1 1 0 0 0-1-1H16a1 1 0 0 0-1 1 7.008 7.008 0 0 1-7 7 1 1 0 0 0-1 1v20a1 1 0 0 0 1 1 7.008 7.008 0 0 1 7 7 1 1 0 0 0 1 1h48a1 1 0 0 0 1-1 6.957 6.957 0 0 1 3-5.728V66zm80 4c0 .58-2.453 2-7 2s-7-1.42-7-2v-3.393A16.147 16.147 0 0 0 77 68a16.162 16.162 0 0 0 7-1.393z"
              style="fill:#22c3e6"/>
        </svg>
        <h2><a href="/" class="icon-tg">ProMoney</a></h2>
      </div>
    </div>
    <div class="sidebar">
      <router-link v-for="(item, index) in navigationItems" :to="item.to" class="main" :key="index"
                   @click="switcherFunctions(item)">
        <span class="material-symbols-outlined">{{ item.icon }}</span>
        <h3>{{ item.title }}</h3>
      </router-link>
    </div>
  </aside>
</template>
<script>
import {useUserStore} from "@/stores/user.js";
import {computed} from "vue";
import router from "@/router/index.js";
import {generateTelegramAuthLink, getExcel} from "@/services/api.js";

export default {
  name: 'Aside',
  data() {
    return {
      navigationItems: [
        {to: '/', icon: 'dashboard', title: 'Главная'},
        {to: '/transactions', icon: 'paid', title: 'Транзакции'},
        {to: '/target-list', icon: 'inventory', title: 'Цели'},
        {to: '/', icon: 'receipt_long', title: 'Загрузить эксель'},
        {to: '/', icon: 'send', title: 'Telegram'},
        {to: '/login', icon: 'logout', title: 'Выйти'},
      ]
    };
  },
  setup() {
    const userStore = useUserStore();

    const isLoggedIn = computed(() => userStore.isAuthenticated);
    const logout = async () => {
      try {
        await userStore.logout();
        await router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    const switcherFunctions = async (item) => {
      if (item.title === 'Загрузить эксель') {
        await getExcel()
      } else if (item.title === 'Выйти') {
        await logout()
      } else if (item.title === 'Telegram') {
        await registerTelegram()
      }
    }
    const registerTelegram = async () => {
      try {
        const telegramAuthLink = await generateTelegramAuthLink();
        window.location.href = telegramAuthLink;
      } catch (error) {
        console.error('Error registering in Telegram:', error);
      }
    };


    return {
      isLoggedIn,
      logout,
      switcherFunctions,
      registerTelegram
    };
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap");

:root {
  --color-primary: #6c9bcf;
  --color-white: #fff;
  --color-info-dark: #7d8da1;
  --color-dark: #363949;
  --color-light: rgba(132, 139, 200, 0.18);
  --color-dark-variant: #677483;
  --color-background: #f6f6f9;
  --color-input: #eee;

  --card-border-radius: 2rem;
  --border-radius-1: 0.4rem;
  --border-radius-2: 1.2rem;

  --card-padding: 1.8rem;
  --padding-1: 1.2rem;

  --box-shadow: 0 2rem 3rem var(--color-light);
}

* {
  margin: 0;
  padding: 0;
  outline: 0;
  border: 0;
  text-decoration: none;
  box-sizing: border-box;
}

html {
  font-size: 14px;
}

body {
  font-family: "Montserrat", sans-serif;
  font-size: 0.88rem;
  user-select: none;
  overflow-x: hidden;
  color: var(--color-dark);
  background-color: var(--color-background);
}

a {
  color: var(--color-dark);
}

img {
  display: block;
  width: 100%;
  object-fit: cover;
}

h1 {
  font-weight: 800;
  font-size: 1.8rem;
}

h2 {
  font-weight: 600;
  font-size: 1.3rem;
}

h3 {
  font-weight: 500;
  font-size: 0.87rem;
}

small {
  font-size: 0.76rem;
}

p {
  color: var(--color-dark-variant);
}

b {
  color: var(--color-dark);
}

aside {
  height: 100vh;
  width: 12rem;
}

aside .toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.4rem;
}

aside .toggle .site-name {
  display: flex;
  gap: 0.5rem;
}

aside .toggle .site-name svg {
  width: 2rem;
  height: 2rem;
  margin-left: 22px;
}

aside .toggle .close {
  padding-right: 1rem;
  display: none;
}

aside .sidebar {
  display: flex;
  flex-direction: column;
  background-color: var(--color-white);
  box-shadow: var(--box-shadow);
  border-radius: 15px;
  height: 88vh;
  position: relative;
  top: 1.5rem;
  transition: all 0.3s ease;
  margin-left: 10px;
}

aside .sidebar:hover {
  box-shadow: none;
}

aside .sidebar a {
  display: flex;
  align-items: center;
  color: var(--color-info-dark);
  height: 3.7rem;
  gap: 1rem;
  position: relative;
  margin-left: 2rem;
  transition: all 0.3s ease;
}

aside .sidebar a span {
  font-size: 1.6rem;
  transition: all 0.3s ease;
}

aside .sidebar a:nth-last-child(-n+2) {
  position: absolute;
  bottom: 5.5rem;
  width: 100%;
}

aside .sidebar a:nth-last-child(-n+1) {
  position: absolute;
  bottom: 2rem;
  width: 100%;
}

aside .sidebar a:hover {
  color: var(--color-primary);
}

aside .sidebar a:hover span {
  margin-left: 0.6rem;
}

main {
  margin-top: 1.4rem;
}
</style>

<template>
  <div class="page">
    <div class="container" :class="{ active: activeTab === 'register' }">
      <div v-if="activeTab === 'login'" class="form-container sign-in">
        <form @submit.prevent="login">
          <h1 class="h_title">Войти в аккаунт</h1>
          <input type="email" v-model="loginData.email" placeholder="Email" required/>
          <input type="password" v-model="loginData.password" placeholder="Пароль" required/>
          <a href="#">Запомнить пароль?</a>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <button type="submit">Войти</button>
          <a class="column">
            <div class="social-icons">
              <a @click="handleGoogleLogin" class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="24" height="24"
                     viewBox="0 0 30 30">
                  <path fill="#ffeea3"
                        d="M2.647,20.416c-0.578-1.309-0.941-2.682-1.081-4.09C1.522,15.886,1.5,15.439,1.5,15 c0-0.406,0.019-0.809,0.054-1.206c0.142-1.583,0.557-3.11,1.237-4.546l3.271,2.544C5.688,12.827,5.5,13.904,5.5,15 c0,1.014,0.166,2.021,0.494,2.999L2.647,20.416z"></path>
                  <path fill="#ba9b48"
                        d="M2.988,10.035l2.485,1.933C5.159,12.95,5,13.967,5,15c0,0.947,0.137,1.887,0.408,2.805L2.867,19.64 c-0.419-1.086-0.689-2.213-0.804-3.364C2.021,15.854,2,15.425,2,15c0-0.387,0.017-0.777,0.052-1.161 C2.169,12.524,2.483,11.249,2.988,10.035 M2.616,8.479c-0.844,1.6-1.392,3.381-1.561,5.271C1.019,14.162,1,14.579,1,15 c0,0.464,0.023,0.923,0.068,1.375c0.171,1.709,0.654,3.325,1.381,4.8l4.141-2.991C6.215,17.193,6,16.123,6,15 c0-1.195,0.238-2.332,0.66-3.375L2.616,8.479L2.616,8.479z"></path>
                  <path fill="#ffeea3"
                        d="M5.749,18.792C5.269,17.622,5,16.343,5,15c0-1.427,0.308-2.78,0.847-4.008l-2.431-1.89 C2.512,10.871,2,12.875,2,15c0,2.001,0.465,3.888,1.272,5.581L5.749,18.792z"></path>
                  <path fill="#f78f8f"
                        d="M3.259,8.346C5.66,4.112,10.121,1.5,15,1.5c3.168,0,6.217,1.115,8.642,3.151l-2.848,2.848 C19.133,6.207,17.094,5.5,15,5.5c-3.667,0-6.95,2.075-8.537,5.338L3.259,8.346z"></path>
                  <path fill="#c74343"
                        d="M15,2c2.867,0,5.633,0.949,7.895,2.691L20.746,6.84C19.065,5.648,17.057,5,15,5 c-3.653,0-6.943,1.955-8.702,5.076L3.913,8.221C6.271,4.363,10.446,2,15,2 M15,1C9.624,1,4.962,4.034,2.616,8.479l4.044,3.145 C7.996,8.328,11.224,6,15,6c2.231,0,4.26,0.825,5.828,2.172l3.546-3.546C21.895,2.377,18.613,1,15,1L15,1z"></path>
                  <path fill="#f78f8f"
                        d="M5.847,10.992C7.266,7.758,10.338,5.414,14,5.05v-3C9.373,2.404,5.424,5.174,3.416,9.102 L5.847,10.992z"></path>
                  <path fill="#bae0bd"
                        d="M15,28.5c-5.029,0-9.555-2.736-11.91-7.17l3.283-2.371C7.909,22.298,11.298,24.5,15,24.5 c2.017,0,3.994-0.651,5.613-1.84l3.066,2.658C21.247,27.374,18.187,28.5,15,28.5z"></path>
                  <path fill="#5e9c76"
                        d="M6.188,19.709C7.91,22.918,11.307,25,15,25c1.989,0,3.941-0.601,5.581-1.706l2.319,2.01 C20.638,27.05,17.872,28,15,28c-4.697,0-8.938-2.479-11.258-6.525L6.188,19.709 M6.591,18.185L2.45,21.175 C4.733,25.806,9.488,29,15,29c3.645,0,6.953-1.402,9.439-3.686l-3.807-3.299C19.092,23.256,17.134,24,15,24 C11.152,24,7.878,21.581,6.591,18.185L6.591,18.185z"></path>
                  <path fill="#bae0bd"
                        d="M21.401,22.68C19.666,24.128,17.435,25,15,25c-4.18,0-7.756-2.566-9.251-6.208l-2.477,1.789 C5.362,24.964,9.821,28,15,28c3.341,0,6.378-1.271,8.681-3.343L21.401,22.68z"></path>
                  <g>
                    <path fill="#8bb7f0"
                          d="M21.396,22.015C23.377,20.213,24.5,17.695,24.5,15c0-0.839-0.115-1.677-0.342-2.5h4.103 C28.42,13.339,28.5,14.178,28.5,15c0,3.688-1.483,7.134-4.068,9.646L21.396,22.015z"></path>
                    <path fill="#4e7ab5"
                          d="M27.841,13C27.947,13.671,28,14.341,28,15c0,3.394-1.305,6.575-3.593,8.962l-2.27-1.967 C23.97,20.134,25,17.649,25,15c0-0.67-0.069-1.339-0.207-2H27.841 M28.67,12h-5.193C23.81,12.94,24,13.946,24,15 c0,2.884-1.361,5.444-3.471,7.091c0.034-0.026,0.07-0.05,0.103-0.076l3.807,3.299c-0.615,0.565-1.281,1.075-1.99,1.524 C26.381,24.36,29,19.991,29,15C29,13.969,28.881,12.967,28.67,12L28.67,12z"></path>
                  </g>
                  <g>
                    <path fill="#8bb7f0" d="M15.5 12.5H26.5V16.5H15.5z"></path>
                    <path fill="#4e7ab5" d="M26,13v3H16v-3H26 M27,12H15v5h12V12L27,12z"></path>
                  </g>
                  <path fill="#8bb7f0"
                        d="M27.5,13H22v3h2.944c-0.267,2.679-1.585,5.047-3.543,6.68l2.281,1.977C26.327,22.277,28,18.838,28,15 L27.5,13z"></path>
                </svg>
              </a>
            </div>
            <span>используйте свою почту для авторизации</span>
          </a>
        </form>
      </div>
      <div v-else class="form-container sign-up">
        <form @submit.prevent="register">
          <h1>Создать аккаунт</h1>
          <input type="email" v-model="registerData.email" placeholder="Email" required>
          <input type="text" v-model="registerData.first_name" placeholder="Имя" required>
          <input type="text" v-model="registerData.last_name" placeholder="Фамилия" required>
          <input type="password" v-model="registerData.password" placeholder="Пароль" required>
          <input type="password" v-model="registerData.password2" placeholder="Повторите пароль" required>
          <button type="submit">Зарегистрироваться</button>
          <div class="column">
            <div class="social-icons">
              <a @click="handleGoogleLogin" class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="24" height="24"
                     viewBox="0 0 30 30">
                  <path fill="#ffeea3"
                        d="M2.647,20.416c-0.578-1.309-0.941-2.682-1.081-4.09C1.522,15.886,1.5,15.439,1.5,15 c0-0.406,0.019-0.809,0.054-1.206c0.142-1.583,0.557-3.11,1.237-4.546l3.271,2.544C5.688,12.827,5.5,13.904,5.5,15 c0,1.014,0.166,2.021,0.494,2.999L2.647,20.416z"></path>
                  <path fill="#ba9b48"
                        d="M2.988,10.035l2.485,1.933C5.159,12.95,5,13.967,5,15c0,0.947,0.137,1.887,0.408,2.805L2.867,19.64 c-0.419-1.086-0.689-2.213-0.804-3.364C2.021,15.854,2,15.425,2,15c0-0.387,0.017-0.777,0.052-1.161 C2.169,12.524,2.483,11.249,2.988,10.035 M2.616,8.479c-0.844,1.6-1.392,3.381-1.561,5.271C1.019,14.162,1,14.579,1,15 c0,0.464,0.023,0.923,0.068,1.375c0.171,1.709,0.654,3.325,1.381,4.8l4.141-2.991C6.215,17.193,6,16.123,6,15 c0-1.195,0.238-2.332,0.66-3.375L2.616,8.479L2.616,8.479z"></path>
                  <path fill="#ffeea3"
                        d="M5.749,18.792C5.269,17.622,5,16.343,5,15c0-1.427,0.308-2.78,0.847-4.008l-2.431-1.89 C2.512,10.871,2,12.875,2,15c0,2.001,0.465,3.888,1.272,5.581L5.749,18.792z"></path>
                  <path fill="#f78f8f"
                        d="M3.259,8.346C5.66,4.112,10.121,1.5,15,1.5c3.168,0,6.217,1.115,8.642,3.151l-2.848,2.848 C19.133,6.207,17.094,5.5,15,5.5c-3.667,0-6.95,2.075-8.537,5.338L3.259,8.346z"></path>
                  <path fill="#c74343"
                        d="M15,2c2.867,0,5.633,0.949,7.895,2.691L20.746,6.84C19.065,5.648,17.057,5,15,5 c-3.653,0-6.943,1.955-8.702,5.076L3.913,8.221C6.271,4.363,10.446,2,15,2 M15,1C9.624,1,4.962,4.034,2.616,8.479l4.044,3.145 C7.996,8.328,11.224,6,15,6c2.231,0,4.26,0.825,5.828,2.172l3.546-3.546C21.895,2.377,18.613,1,15,1L15,1z"></path>
                  <path fill="#f78f8f"
                        d="M5.847,10.992C7.266,7.758,10.338,5.414,14,5.05v-3C9.373,2.404,5.424,5.174,3.416,9.102 L5.847,10.992z"></path>
                  <path fill="#bae0bd"
                        d="M15,28.5c-5.029,0-9.555-2.736-11.91-7.17l3.283-2.371C7.909,22.298,11.298,24.5,15,24.5 c2.017,0,3.994-0.651,5.613-1.84l3.066,2.658C21.247,27.374,18.187,28.5,15,28.5z"></path>
                  <path fill="#5e9c76"
                        d="M6.188,19.709C7.91,22.918,11.307,25,15,25c1.989,0,3.941-0.601,5.581-1.706l2.319,2.01 C20.638,27.05,17.872,28,15,28c-4.697,0-8.938-2.479-11.258-6.525L6.188,19.709 M6.591,18.185L2.45,21.175 C4.733,25.806,9.488,29,15,29c3.645,0,6.953-1.402,9.439-3.686l-3.807-3.299C19.092,23.256,17.134,24,15,24 C11.152,24,7.878,21.581,6.591,18.185L6.591,18.185z"></path>
                  <path fill="#bae0bd"
                        d="M21.401,22.68C19.666,24.128,17.435,25,15,25c-4.18,0-7.756-2.566-9.251-6.208l-2.477,1.789 C5.362,24.964,9.821,28,15,28c3.341,0,6.378-1.271,8.681-3.343L21.401,22.68z"></path>
                  <g>
                    <path fill="#8bb7f0"
                          d="M21.396,22.015C23.377,20.213,24.5,17.695,24.5,15c0-0.839-0.115-1.677-0.342-2.5h4.103 C28.42,13.339,28.5,14.178,28.5,15c0,3.688-1.483,7.134-4.068,9.646L21.396,22.015z"></path>
                    <path fill="#4e7ab5"
                          d="M27.841,13C27.947,13.671,28,14.341,28,15c0,3.394-1.305,6.575-3.593,8.962l-2.27-1.967 C23.97,20.134,25,17.649,25,15c0-0.67-0.069-1.339-0.207-2H27.841 M28.67,12h-5.193C23.81,12.94,24,13.946,24,15 c0,2.884-1.361,5.444-3.471,7.091c0.034-0.026,0.07-0.05,0.103-0.076l3.807,3.299c-0.615,0.565-1.281,1.075-1.99,1.524 C26.381,24.36,29,19.991,29,15C29,13.969,28.881,12.967,28.67,12L28.67,12z"></path>
                  </g>
                  <g>
                    <path fill="#8bb7f0" d="M15.5 12.5H26.5V16.5H15.5z"></path>
                    <path fill="#4e7ab5" d="M26,13v3H16v-3H26 M27,12H15v5h12V12L27,12z"></path>
                  </g>
                  <path fill="#8bb7f0"
                        d="M27.5,13H22v3h2.944c-0.267,2.679-1.585,5.047-3.543,6.68l2.281,1.977C26.327,22.277,28,18.838,28,15 L27.5,13z"></path>
                </svg>
              </a>
            </div>
            <span>используйте свою почту для регистрации</span>
          </div>
        </form>
      </div>
      <div class="toggle-container">
        <div class="toggle">
          <div class="toggle-panel toggle-left">
            <h1>С возвращением!</h1>
            <p>Введите свои данные, чтобы использовать все возможности сайта</p>
            <button @click="switchToLogin" class="hidden" id="login">Войти</button>
          </div>
          <div class="toggle-panel toggle-right">
            <h1>Добро пожаловать!</h1>
            <p>Введите свои данные, чтобы использовать все возможности сайта</p>
            <button @click="switchToRegister" class="hidden" id="register">Зарегистрироваться</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {googleSdkLoaded} from "vue3-google-login";
import router from "@/router/index.js";
import {useUserStore} from "@/stores/user.js";

export default {
  name: "LoginView",
  data() {
    return {
      activeTab: 'login',
      registerData: {
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        password2: '',
      },
      loginData: {
        email: '',
        password: '',
      },
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const userStore = useUserStore();
        await userStore.login(this.loginData);
        if (userStore.isLoggedIn) {
          router.push("/");
        } else {
          this.errorMessage = 'Неправильный логин или пароль';
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error === 'Invalid credentials') {
          this.errorMessage = 'Неправильный логин или пароль';
          return;
        }
        console.error("Login failed:", error.response ? error.response.data : error);
      }
    },
    async register() {
      try {
        const userStore = useUserStore();
        const data = await userStore.register(this.registerData);
        if (data.refresh && data.access) {
          router.push("/");
        }
        if (data.registration_link) {
          setTimeout(() => {
            window.location.href = data.registration_link;
          }, 1000);
        } else {
          this.activeTab = 'login';
          const container = document.getElementById('container');
          container.classList.remove('active');
        }
      } catch (error) {
      }
    },
    switchToRegister() {
      this.activeTab = 'register';
    },
    switchToLogin() {
      this.activeTab = 'login';
    }
  },
  setup() {
    const userStore = useUserStore();

    const handleGoogleLogin = () => {
      googleSdkLoaded(google => {
        google.accounts.oauth2
            .initCodeClient({
              client_id: import.meta.env.VITE_APP_GOOGLE_OAUTH2_CLIENT_ID,
              scope: "email profile openid",
              redirect_uri: import.meta.env.VITE_APP_REDIRECT_URI,
              callback: response => {
                if (response.code) {
                  loginWithGoogle(response.code);
                }
              }
            })
            .requestCode();
      });
    };

    const loginWithGoogle = async code => {
      await userStore.loginWithGoogle(code);
      if (userStore.isLoggedIn) {
        router.push("/");
      }
    };
    return {
      handleGoogleLogin
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Montserrat', sans-serif;
}

body {
  background: linear-gradient(to right, #eee, #98bae770);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  height: 100vh;
}

p {
  color: #fff;
}

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.container {
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.35);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 100%;
  min-height: 480px;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.container p {
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.3px;
  margin: 20px 0;
}

.container h1 {
  font-size: 28px;
  margin-bottom: 28px;
}

.container span {
  font-size: 12px;
}

.container a {
  color: #333;
  font-size: 13px;
  text-decoration: none;
  margin: 28px 0 4px;
}

.container button {
  background-color: rgb(154, 153, 222);
  color: #fff;
  font-size: 12px;
  padding: 10px 45px;
  border: 1px solid transparent;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 10px;
  cursor: pointer;
}

.container a.hidden {
  color: #fff;
  font-size: 12px;
  padding: 10px 45px;
  border: 1px solid #ffffff;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 10px;
  cursor: pointer;
  text-decoration: none;
}

.container form {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  height: 100%;
}

.container input {
  background-color: #eee;
  border: none;
  margin: 8px 0;
  padding: 10px 15px;
  font-size: 13px;
  border-radius: 8px;
  width: 100%;
  outline: none;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
}

.sign-up {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
}

.column {
  max-width: 300px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.social-icons {
  margin: 20px 16px;
}

.social-icons a {
  border: 1px solid #ccc;
  border-radius: 20%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 3px;
  width: 40px;
  height: 40px;
}

.toggle-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: all 0.6s ease-in-out;
  border-radius: 150px 0 0 100px;
  z-index: 10;
}

.container.active .toggle-container {
  transform: translateX(-100%);
  border-radius: 0 150px 100px 0;
}

.toggle {
  background-color: #000000c3;
  height: 100%;
  background: linear-gradient(to right, #98bae7, #b793d3);
  color: #fff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: all 0.6s ease-in-out;
}

.container.active .toggle {
  transform: translateX(50%);
}

.toggle-panel {
  position: absolute;
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 30px;
  text-align: center;
  top: 0;
  transform: translateX(0);
  transition: all 0.6s ease-in-out;
}

.container button.hidden {
  background-color: transparent;
  border-color: white;
}

.toggle-left {
  transform: translateX(-200%);
}

.container.active .toggle-left {
  transform: translateX(0);
}

.toggle-right {
  right: 0;
  transform: translateX(0);
}

.container.active .toggle-right {
  transform: translateX(200%);
}
</style>

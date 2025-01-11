import axios from 'axios';
import { BASE_URL } from "@/const.js";
import {
    getAccessToken,
    setAccessToken,
    setRefreshToken,
    clearRefreshToken,
    clearAccessToken,
    getRefreshToken
} from '../services/localStore.js';
import { defineStore } from 'pinia';
import {googleLogin, login, logout, refreshToken} from "@/services/api.js";

export const useUserStore = defineStore('loggedIn', {
    state: () => {
        return {
            isLoggedIn: !!getAccessToken(),
            refreshInterval: null,
        };
    },
    actions: {
        async login(loginData) {
            try {
                const result = await login(loginData.email, loginData.password);
                console.log(result);
                setRefreshToken(result.refresh);
                setAccessToken(result.access);
                this.isLoggedIn = true;
                this.startTokenRefreshInterval();
            } catch (error) {
                console.error("Login failed:", error.response.data);
            }
        },
        async logout() {
            try {
                const result =  await logout(getRefreshToken());
                clearAccessToken();
                clearRefreshToken();
                this.isLoggedIn = false;
                console.log("Logout successful");
                this.stopTokenRefreshInterval();
            } catch (error) {
                console.error("Logout failed:", error.response ? error.response.data : error);
            }
        },
        async refreshToken() {
            try {
                const result = await refreshToken(getRefreshToken());
                setAccessToken(result.access);
            } catch (error) {
                console.error("Failed to refresh token:", error);
                this.logout();
            }
        },
        async loginWithGoogle(code) {
            try {
                const response = await axios.post(
                    "https://oauth2.googleapis.com/token",
                    {
                        code,
                        clientId: import.meta.env.VITE_APP_GOOGLE_OAUTH2_CLIENT_ID,
                        client_secret: import.meta.env.VITE_APP_GOOGLE_OAUTH2_CLIENT_SECRET,
                        redirect_uri: "postmessage",
                        grant_type: "authorization_code"
                    }
                );
                const accessToken = response.data.access_token;
                this.isLoggedIn = true;
                await this.sendAccessTokenToBackend(accessToken);
                this.startTokenRefreshInterval();
            } catch (error) {
                console.error("Token exchange failed:", error.response.data);
            }
        },
        async sendAccessTokenToBackend(accessToken) {
            try {
                const result = await googleLogin(accessToken);
                setRefreshToken(result.refresh);
                setAccessToken(result.access);
                console.log("Access token sent to backend successfully");
            } catch (error) {
                console.error("Failed to send access token to backend:", error);
            }
        },
        async register(registerData) {
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get('next');

            let registrationUrl = `${BASE_URL}/registration/`;

            if (nextUrl) {
                registrationUrl += `?next=${nextUrl}`;
            }

            try {
                const response = await fetch(registrationUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        ...registerData,
                        next: nextUrl
                    }),
                });
                const data = await response.json();
                console.log(data);
                if (data.refresh && data.access) {
                    setAccessToken(data.access);
                    setRefreshToken(data.access);
                    this.isLoggedIn = true;
                    this.startTokenRefreshInterval();
                }
                return data;
            } catch (error) {
                console.error('Error:', error);
                throw error;
            }
        },
        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        startTokenRefreshInterval() {
            this.stopTokenRefreshInterval();
            this.refreshInterval = setInterval(() => {
                this.refreshToken();
            }, 172800000);
        },
        stopTokenRefreshInterval() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
                this.refreshInterval = null;
            }
        }
    },
    getters: {
        isAuthenticated(state) {
            return state.isLoggedIn;
        }
    }
});
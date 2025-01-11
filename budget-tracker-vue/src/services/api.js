import axios from "axios";
import {BASE_URL} from "@/const.js";
import {useUserStore} from "@/stores/user.js";
import {getAccessToken} from "@/services/localStore.js";

const instance = axios.create({
    baseURL: BASE_URL,
});


instance.interceptors.request.use(async function (config) {
    const userState = useUserStore();
    userState.accessToken = getAccessToken();
    if (userState.accessToken) {
        config.headers.Authorization = `Bearer ${userState.accessToken}`;
    }
    return config;
});

export async function getUserInfo() {
    const response = await instance.get('/user');
    return response.data;
}

export async function login(email, password) {
    const response = await instance.post('/auth/', {email: email, password: password});
    return response.data;
}

export async function googleLogin(accessToken) {
    const response = await instance.post('/google/', {
        token: accessToken
    });
    return response.data;
}

export async function addLimit(formData) {
    const response = await instance.post('/create_limit/', formData);
    return response.data;
}

export async function fetchLimit() {
    const response = await instance.get('/limit/');
    return response.data;
}

export async function deleteLimit(limitId) {
    const response = await instance.delete(`/delete_limit/${limitId}/`);
    return response.data;
}

export async function editLimit(limitId, formData) {
    const response = await instance.put(`/edit_limit/${limitId}/`, formData);
    return response.data;
}

export async function addTransaction(formData) {
    const response = await instance.post('/add_transaction/', formData);
    return response.data;
}

export async function fetchTransactionData(type = '') {
    const response = await instance.get('/add_transaction/', {
        params: {type}
    });
    return response.data;
}

export async function deleteTransaction(transactionId) {
    const response = await instance.delete(`/delete_transaction/${transactionId}/`);
    return response.data;
}
export async function editTransaction(transactionId, transaction) {
    const response = await instance.put(`/edit_transaction/${transactionId}/`, transaction);
    return response.data;
}

export async function getTransactionId(transactionId) {
    const response = await instance.get(`/transaction_id/${transactionId}`);
    return response.data;
}

export async function getCategoriesTargets(type = '') {
    const response = await instance.get('/get_categories_targets/', {
        params: {type}
    });
    return response.data;
}
export async function fetchTransactions() {
    const response = await instance.get('/transactions/');
    return response.data;
}

export async function getTransactions(selectedDate) {
    const params = selectedDate ? {selected_date: selectedDate} : null;
    const response = await instance.get('/', {
        params: params,
    });
    return response.data;
}

export async function fetchTargets() {
    const response = await instance.get('/target/');
    return response.data;
}

export async function addTarget(formData) {
    const response = await instance.post('/create_target/', formData);
    return response.data;
}

export async function getTargetId(targetId) {
    const response = await instance.get(`/target_id/${targetId}`);
    return response.data;
}

export async function editTarget(targetId, formData) {
    const response = await instance.put(`/edit_target/${targetId}/`, formData);
    return response.data;
}

export async function deleteTarget(targetId) {
    const response = await instance.delete(`/delete_target/${targetId}/`);
    return response.data;
}

export async function getExcel() {
    const response = await instance.get('/download_excel/', {
        responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'transactions.xlsx');
    document.body.appendChild(link);
    link.click();
}

export async function fetchChartData(transactionType) {
    const response = await instance.get(`/chart/${transactionType}/`);
    return response.data;
}

export async function generateTelegramAuthLink() {
    const response = await instance.get('/telegram/auth/start/');
    return response.data.telegram_auth_link;
}

export async function refreshToken(refreshToken) {
    try {
        const response = await instance.post("api/token/refresh/", { refresh: refreshToken });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export async function logout(refreshToken){
    const response = await instance.post('/logout/', {
        refresh: refreshToken
    });
    return response.data;
}

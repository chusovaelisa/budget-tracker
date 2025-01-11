<template>
  <h1>Редактировать лимит</h1>
  <div class="base">
    <div v-if="limit !== null && Object.keys(limit).length > 0">
    <form @submit.prevent="submitForm">
      <div class="group">
        <div class="status">
          <div class="info">
            <p>Лимит на: </p>
            <input type="text" v-model="formData.amount" >
            <p>Дата окончания: {{formatDate(limit.end_date)}} </p>
            <input type="date" v-model="formData.endDate">
            <button @click="editLimit(limit.id)">Изменить</button>
          </div>
          <div class="text">
          Без указания даты, лимит по умолчанию будет выставлен на 30 дней
        </div>
        </div>
      </div>
    </form>
    </div>
  </div>
</template>

<script>
import {useUserStore} from "@/stores/user.js";
import {editLimit, fetchLimit} from "@/services/api.js";

export default {
  name: "Limit",
  data() {
    return {
      limit: null,
      formData: {
        amount: '',
        endDate: ''
      }
    };
  },
  methods: {
    async fetchLimit() {
      try {
        const response = await fetchLimit();
        this.limit = response;
        this.formData.endDate = response.endDate;
        this.formData.amount = response.amount;
        console.log("Лимит успешно изменен");
      } catch (error) {
        console.error("Error fetching limit:", error.response.data);
        throw error;
      }
    },
    async editLimit(limitId) {
       try {
          await editLimit(limitId, this.formData);
          await this.fetchLimit();
          this.$router.push('/');
        } catch (error) {
          console.error('Ошибка при обновлении лимита:', error.response.data);
        }
    },

    formatDate(date) {
      const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
  },

  mounted() {
    this.fetchLimit();
  },

  computed: {
     isLoggedIn() {
      const userStore = useUserStore();
      return userStore.isLoggedIn;
    },
  },
};
</script>

<style scoped>
.base {
    display: grid;
    grid-template-columns: repeat(2, 2fr);
    gap: 20rem;
}

.base > div {
    background-color: var(--color-white);
    padding: var(--card-padding);
    border-radius: var(--card-border-radius);
    margin-top: 1rem;
    box-shadow: var(--box-shadow);
    transition: all 0.3s ease;
}

.base > div:hover {
    box-shadow: none;
}

.base > div .status {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.base h3 {
    font-size: 1rem;
}

button {
    background-color: rgb(154, 153, 222);
    color: #fff;
    height: 36px;
    width: 220px;
    font-size: 12px;
    padding: 10px 45px;
    border: 1px solid transparent;
    border-radius: 8px;
    font-weight: 300;
    text-transform: uppercase;
    margin-top: 10px;
    cursor: pointer;
}

button:hover{
    background-color: rgb(153, 169, 222);
    color: #fff;
}

input {
    background-color: var(--color-input);
    color: var(--color-dark);
    border: none;
    margin: 8px 0;
    padding: 10px 15px;
    font-size: 13px;
    border-radius: 8px;
    width: 100%;
    outline: none;
}

.text {
    display: flex;
    margin-left:20px;
    letter-spacing: 0.1rem;
    line-height: 1rem;
}
</style>
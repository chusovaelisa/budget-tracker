<template>
  <h1>Установить лимит</h1>
  <form @submit.prevent="submitForm" class="base">
    <div class="group">
      <div class="status">
        <div class="info">
          <p>Лимит на:</p>
          <input type="text" v-model="formData.amount" placeholder="Введите лимит">
          <p>Дата окончания:</p>
          <input type="date" v-model="formData.endDate">
          <button type="submit">Сохранить</button>
        </div>
        <div class="text">
          Без указания даты, лимит по умолчанию будет выставлен на 30 дней
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { addLimit } from "@/services/api.js";

export default {
  data() {
    return {
      formData: {
        amount: '',
        endDate: ''
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await addLimit(this.formData);
        this.$router.push('/');
      } catch (error) {
        console.error('Ошибка при добавлении лимита:', error.response.data);
      }
    }
  }
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

.base .edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 270px;
  height: 92px;
  border-radius: 50%;
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

button:hover {
  background-color: rgb(153, 169, 222);
  color: #fff;
}

.base .empty {
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  margin-left: 20px;
  letter-spacing: 0.1rem;
  line-height: 1rem;
}
</style>
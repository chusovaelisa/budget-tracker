<template>
  <div>
    <h2>Редактировать транзакцию</h2>
    <form @submit.prevent="submitForm">
   <div>
        <label for="type">Тип:</label>
        <select id="type" v-model="transaction.type" @change="fetchCategories">
          <option value="" disabled>Выберите тип транзакции</option>
          <option value="income">Доход</option>
          <option value="expense">Расход</option>
        </select>
      </div>

      <div>
        <label for="amount">Сумма:</label>
        <input type="number" id="amount" v-model.number="transaction.amount" :placeholder="transaction.amount">
      </div>

      <div>
        <label for="description">Описание:</label>
        <input type="text" id="description" v-model.text="transaction.description" :placeholder="transaction.description">
      </div>

      <div v-if="transaction.type">
        <label for="category">Категория:</label>
        <select id="category" v-model="transaction.category">
          <option value="" disabled>Выберите категорию</option>
          <option v-for="category in categories" :key="category" :value="category.id">{{ category.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="target">Цель:</label>
        <select id="target" v-model="transaction.target">
          <option value="" disabled>Выберите цель</option>
          <option v-for="target in targets" :key="target" :value="target.id">{{ target.name }}</option>
        </select>
      </div>

      <button type="submit">Изменить</button>
    </form>
  </div>
</template>
<script>

import {
  editTransaction,
  getCategoriesTargets,
  getTransactionId,
} from "@/services/api.js";
import {useUserStore} from "@/stores/user.js";

export default {
  data() {
    return {
      transaction: {
        type: '',
        amount: '',
        description: '',
        category: '',
        target: ''
      },
      categories: [],
      targets: []
    };
  },
  methods: {
    async fetchTransactions() {
      const transactionId = this.$route.params.transactionId;
      try {
        const response = await getTransactionId(transactionId);
        this.transaction = response;
        this.transaction.type = response.type;
        this.transaction.amount = response.amount;
        this.transaction.description = response.description;
        this.transaction.category = response.category;
        this.transaction.target = response.target;
      } catch (error) {
        console.error("Ошибка при получении транзакции:", error.response.data);
        throw error;
      }
    },
    async submitForm() {
      try {
          const transactionId = this.$route.params.transactionId;
            await editTransaction(transactionId, { type: this.transaction.type,  amount: this.transaction.amount, description: this.transaction.description, category: this.transaction.category, target: this.transaction.target });
            console.log('Транзакция обновлена');
            this.$router.push('/transactions');
      } catch (error) {
            console.error('Ошибка при обновлении транзакции:', error.response.data);
      }
    },
    async fetchCategories() {
      try {
        const { categories, targets } = await getCategoriesTargets(this.transaction.type);
        this.categories = categories;
        this.targets = targets;
      } catch (error) {
        console.error('Ошибка при получении данных категорий:', error);
      }
    },
  },
  async created() {
    try {
      const { targets, categories } = await getCategoriesTargets();
      this.targets = targets;
      this.categories = categories;
    } catch (error) {
      console.error('Ошибка при получении данных о транзакциях:', error);
    }
  },
  mounted() {
    this.fetchTransactions();
  },
  computed: {
    isLoggedIn() {
      const userStore = useUserStore();
      return userStore.isLoggedIn;
    }
  }
};
</script>

<style scoped>
.base {
  max-width: 150px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.6rem;
}

.base > div {
  background-color: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
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
  width: 250px;
  height: 82px;
  border-radius: 50%;
}

button {
  background-color: rgb(154, 153, 222);
  color: #fff;
  height: 36px;
  width: calc(100% - 20px);
  font-size: 12px;
  padding: 10px 35px;
  border: 1px solid transparent;
  border-radius: 8px;
  font-weight: 300;
  text-transform: uppercase;
  margin-top: 10px;
  cursor: pointer;
}

button:hover {
  background-color: rgb(153, 169, 222);
}

.base .empty {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

input, select {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 8px 0;
  font-size: 13px;
  border-radius: 8px;
  border: none;
  background-color: #eee;
  outline: none;
}

textarea {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 8px 0;
  font-size: 12px;
  border-radius: 8px;
  border: none;
  background-color: #eee;
  outline: none;
}

.input-with-hint {
  position: relative;
  width: calc(100% - 20px);
}

.input-with-hint input {
  width: 100%;
}

.input-with-hint span {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  font-size: 12px;
  color: #999;
}

form {
  width: 60%;
}
</style>
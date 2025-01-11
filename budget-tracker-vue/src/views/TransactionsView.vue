<template>
  <div class="block">
      <h1>Транзакции</h1>
      <router-link to="/add_transaction" class="button-link add-transaction-button" title="Добавить транзакцию">
        <span class="material-symbols-outlined" title="Добавить транзакцию">add_box</span>
      </router-link>
  </div>
  <div class="page-container">
    <div class="transactions">
      <div>
        <div v-for="transaction in transactions" :key="transaction.id" class="transaction-item">
          <div class="transaction-main">
            <span class="category-circle" :style="{ backgroundColor: transaction.color }">
              <img :src="transaction.logo" :alt="transaction.category" class="category-icon">
            </span>
            <div class="transaction-details">
              <span class="transaction-name">{{ transaction.category }}</span>
              <span>{{ transaction.formatted_date }}</span>
              <span v-if="transaction.type === 'income'" class="transaction-amount transaction-income">
                +{{ transaction.formatted_amount }} ₽
              </span>
              <span v-else-if="transaction.type === 'expense'" class="transaction-amount transaction-expense">
                -{{ transaction.formatted_amount }} ₽
              </span>
            </div>
            <div class="transaction-actions">
              <div class="transaction-description"
                   v-bind:title="transaction.showDescription ? '' : 'Показать описание'"
                   v-bind:data-description="transaction.description"
                   @click="toggleDescription(transaction)">
                <span class="material-symbols-outlined">more_horiz</span>
              </div>
              <router-link :to="'/edit_transaction/' + transaction.id" class="edit-button">
                <span class="material-symbols-outlined" title="Редактировать">edit</span>
              </router-link>
              <button @click="deleteTransaction(transaction.id)" class="transparent-button">
                <span class="material-symbols-outlined" title="Удалить">delete_sweep</span>
              </button>
            </div>
          </div>
          <div v-if="transaction.showDescription" class="transaction-full-description">
            {{ transaction.description }}
          </div>
        </div>
        <div v-if="transactions.length === 0">
          <p class="empty">Транзакций нет.</p>
          <p class="empty">Нажмите на кнопку 'Добавить транзакцию', чтобы внести новую запись о вашем финансовом движении.</p>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useUserStore} from '@/stores/user.js';
import {deleteTransaction, fetchTransactions} from "@/services/api.js";

export default {
  data() {
    return {
      transactions: [],
    };
  },
  methods: {
    async fetchTransactions() {
      try {
        const transactions = await fetchTransactions();
        this.transactions = transactions.sort((a, b) => new Date(b.date) - new Date(a.date)).map(transaction => ({
          ...transaction,
          showDescription: false,
        }));
      } catch (error) {
        console.error("Error fetching transactions:", error.response.data);
        throw error;
      }
    },
    async deleteTransaction(transactionId) {
      try {
        await deleteTransaction(transactionId);
        this.transactions = this.transactions.filter(transaction => transaction.id !== transactionId);
        console.log('Транзакция успешно удалена');
      } catch (error) {
        console.error('Произошла ошибка при удалении транзакции:', error.response.data);
        throw error;
      }
    },
    toggleDescription(transaction) {
      transaction.showDescription = !transaction.showDescription;
    },
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
@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0");

.transactions {
  list-style-type: none;
  padding: 0;
}

h1 {
  margin-bottom: 8px;
}

.transaction-item {
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.transaction-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.category-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;
}

.category-icon {
  width: 20px;
  height: auto;
}

.transaction-details {
  color: #333;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: 200px;
}

.transaction-amount {
  color: var(--color-white);
  font-weight: bold;
  font-size: 18px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  position: relative;
  top: -16px;
}

.transaction-name {
  color: var(--color-dark);
  font-weight: bold;
}

.transaction-income {
  color: #41da41;
}

.transaction-expense {
  color: #cb4c4c;
}

.transaction-actions {
  display: flex;
  align-items: center;
}

.transaction-actions button {
  margin-left: 5px;
  margin-right: 5px;
}

.material-symbols-outlined {
  color: #7D8DA1FF;
}

.material-symbols-outlined:hover {
  color: #6C9BCFFF;
}

.transparent-button {
  background-color: transparent;
  border: none;
}

.page-container {
  display: flex;
  flex-direction: column;
}

.transactions {
  flex-grow: 1;
}

span {
  color: var(--color-dark-variant);
}

.transaction-full-description {
  margin-top: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.empty {
  display: flex;
  justify-content: center;
  flex-direction: column;
  max-width: 30rem;
  background-color: var(--color-white);
  padding: var(--card-padding);
  border-radius: 20px;
  margin-top: 1rem;
  box-shadow: var(--box-shadow);
  transition: all 0.3s ease;
}

.empty:hover {
  box-shadow: none;
}

.block {
  margin-bottom: 10px;
  width: 16%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
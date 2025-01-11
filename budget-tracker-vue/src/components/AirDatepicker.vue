<template>
  <div class="main-container">
    <div class="transactions-section">
      <div class="transactions-container">
        <div v-for="transaction in paginatedTransactions" :key="transaction.id" class="transaction-item">
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
        </div>
        <div v-if="transactions.length === 0">
          <div class="empty">
            <p>Нет транзакций за это число.</p>
          </div>
          <div class="empty">
            <p>Выберите дату в календаре, чтобы просмотреть транзакции за этот день.</p><br>
            <p>Будут показаны последние 5 транзакций за выбранную дату.</p></div>
        </div>
      </div>
      <div class="pagination-more">
        <button @click="viewMoreTransactions" title="More">Подробнее</button>
        <div v-if="totalPages > 1" class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">←</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">→</button>
        </div>
      </div>
    </div>
    <div class="date-picker-section">
      <div class="date-picker-container"></div>
    </div>
  </div>
</template>
<script>
import AirDatepicker from 'air-datepicker';
import 'air-datepicker/air-datepicker.css';
import {BASE_URL} from "@/const.js";
import {getTransactions} from "@/services/api.js";

export default {
  data() {
    return {
      transactions: [],
      currentPage: 1,
      transactionsPerPage: 5
    };
  },
  mounted() {
    const self = this;
    new AirDatepicker('.date-picker-container', {
      inline: true,
      dateFormat: 'dd.MM.yyyy',
      onSelect: function (formattedDate) {
        self.fetchTransactions(formattedDate);
      }
    });
    const selectedDate = null;
    this.fetchTransactions(selectedDate);
  },

  methods: {
    BASE_URL() {
      return BASE_URL;
    },
    async fetchTransactions(selectedDate) {
      try {
        this.transactions = await getTransactions(selectedDate);
        this.currentPage = 1;
        console.log(this.transactions)
      } catch (error) {
        console.error('Ошибка при получении транзакций:', error);
      }
    },
    viewMoreTransactions() {
      this.$router.push('/transactions');
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  },
  computed: {
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.transactionsPerPage;
      const end = start + this.transactionsPerPage;
      return this.transactions.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.transactions.length / this.transactionsPerPage);
    }
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0");

.main-container {
  justify-content: space-between;
}

.transactions-section {
  flex: 1;
  margin-right: 20px;
}

.date-picker-section {
  width: 300px;
  position: fixed;
  top: 400px;
}

.transactions-container {
  max-width: 600px;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
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

button {
  background-color: rgb(154, 153, 222);
  color: #fff;
  font-size: 10px;
  padding: 8px 30px;
  border: 1px solid transparent;
  border-radius: 6px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 5px;
  cursor: pointer;
}

.date-picker-container {
  margin-top: 10px;
}

span {
  color: var(--color-dark-variant);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.pagination button {
  background-color: rgb(154, 153, 222);
  color: #fff;
  border: none;
  padding: 5px 10px;
  margin: 0 5px;
  cursor: pointer;
}

.pagination span {
  margin: 0 10px;
}

.pagination-more {
  display: flex;
  position: fixed;
  top: 370px;
}

.empty {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 20em;
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
</style>

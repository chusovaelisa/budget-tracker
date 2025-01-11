<template>
  <div class="base">
    <div v-if="limit !== null && Object.keys(limit).length > 0">
      <div class="group">
        <div class="status">
          <div class="info">
            <h3>Лимит на: </h3>
            <p>{{ limit.amount }}</p>
          </div>
          <div class="progress-container">
            <p>{{ limit.current_amount }}</p>
            <progress class="progress-bar" :value="limit.current_amount" :max="limit.amount"></progress>
            <p>{{ limit.amount }}</p>
          </div>
          <div class="dates-row">
            <div class="date">
              <p>{{ formatDate(limit.start_date) }}</p>
            </div>
            <div class="date">
              <p>{{ formatDate(limit.end_date) }}</p>
            </div>
          </div>
        </div>
         <div class="edit">
          <router-link to="/edit_limit" class="edit-button"><span class="material-symbols-outlined" title="Редактировать">edit</span></router-link>
          <button @click="deleteLimit(limit.id)" class="edit-button"><span class="material-symbols-outlined" title="Удалить">delete_sweep</span></button>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="empty group">
        <div class="block">
           <h2>Лимита нет 😔</h2>
            <div class="text-bloc">
              <p>Установите предельную сумму трат на месяц.</p>
            </div>
        </div>
        <div>
          <router-link to="/create_limit" class="add-button" disabled>Добавить лимит</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user.js";
import { deleteLimit, fetchLimit } from "@/services/api.js";

export default {
  name: "Limit",
  data() {
    return {
      limit: null,
    };
  },
  methods: {
    async fetchLimit() {
      try {
        this.limit = await fetchLimit();
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.warn("Лимит не найден для текущего пользователя.");
          this.limit = null;
        } else if (error.response && error.response.status === 401) {
          console.warn("Ошибка авторизации: требуется повторный вход.");
        } else {
          console.error("Ошибка при получении лимита:", error);
        }
      }
    },
    async deleteLimit(limitId) {
      try {
        await deleteLimit(limitId);
        console.log("Лимит успешно удален");
        this.limit = null;
        await this.fetchLimit();
      } catch (error) {
        console.error("Произошла ошибка при удалении лимита:", error);
        throw error;
      }
    },
    formatDate(date) {
      const options = {day: "2-digit", month: "2-digit", year: "numeric"};
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
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
  width: 100%;
}

.group {
  display: flex;
  max-width: 460px;
  min-width: 400px;
  align-items: center;
  background-color: var(--color-white);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  margin-top: 1rem;
  box-shadow: var(--box-shadow);
  transition: all 0.3s ease;
}

.group:hover {
  box-shadow: none;
}

.status {
  display: flex;
  flex-direction: column;
}

.info {
  margin-bottom: 1rem;
  display: flex;
}

.info h3 {
  margin: 0.3rem;
}

.info p {
  font-size: 1.2rem;
  margin-left: 12px;

}

.progress-container {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 10px;
  width: 250px;
}

.progress-bar {
  flex-grow: 1;
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar::-webkit-progress-bar {
  background-color: #e0e0e0;
}

.progress-bar::-webkit-progress-value {
  background-color: #9a99de;
  border-radius: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #9a99de;
  transition: width 0.3s ease;
}

.dates-row {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.date {
  display: flex;
  flex-direction: column;
}

.edit {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  margin-left: 110px;
}

.add-button {
  background-color: rgb(154, 153, 222);
  color: #fff;
  min-height: 100%;
  min-width: 70%;
  font-size: 12px;
  padding: 10px 20px;
  border: 1px solid transparent;
  border-radius: 8px;
  font-weight: 300;
  text-transform: uppercase;
  margin-bottom: 10px;
  cursor: pointer;
}

.material-symbols-outlined {
  color: #7D8DA1FF;
}

.material-symbols-outlined:hover {
  color: rgb(154, 153, 222);
}

.edit-button {
  background-color: transparent;
  border: none;
}

.empty {
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

.edit .add-button {
  font-weight: normal;
}

.block{
  display: flex;
  flex-direction: column;
}

.text-bloc{
  display: flex;
  padding-top: 20px;
  width: 180px;
}

</style>

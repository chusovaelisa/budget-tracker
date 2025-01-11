<template>
    <div class="block">

  <h1>Список целей</h1>
  <router-link to="/create_target" class="button-link add-transaction-button" disabled>
          <span class="material-symbols-outlined" title="Добавить цель">add_box</span>
</router-link>
    </div>
  <div class="page-container">
    <div>
      <div class="scrollable-content">
        <div v-if="targets.length > 0" class="base">
          <div v-for="target in targets" :key="target.id" class="group">
            <div class="card">
              <div class="content">
                <template v-if="target.reached == 100">
                  <h2 class="target-status">Цель достигнута!</h2>
                  <p class="target-status">🎉😎👍</p>
                </template>
                <template v-else class="content">
                  <h3 class="target-name">{{ target.name }}</h3>
                  <div class="progress-container">
                    <span class="sum">{{ target.current_sum }}</span>
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: `${(target.current_sum / target.target_sum) * 100}%` }"></div>
                    </div>
                    <span class="sum">{{ target.target_sum }}</span>
                  </div>
                </template>
                 <div class="edit actions">
                  <router-link :to="'/edit_target/' + target.id" class="edit-button"><span class="material-symbols-outlined" title="Редактировать">edit</span></router-link>
                  <button @click="deleteTarget(target.id)" class="edit-button"><span class="material-symbols-outlined" title="Удалить">delete_sweep</span></button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty">
          <h2>Целей нет 😔</h2>
          <p>Создайте свой список финансовых целей.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { deleteTarget, fetchTargets } from "@/services/api.js";

export default {
  data() {
    return {
      targets: []
    };
  },
  methods: {
    async fetchTargets() {
      try {
        this.targets = await fetchTargets();
      } catch (error) {
        console.error("Error fetching targets:", error.response.data);
        throw error;
      }
    },
    async deleteTarget(targetId) {
      try {
        await deleteTarget(targetId);
        this.targets = this.targets.filter(target => target.id !== targetId);
        console.log('Цель успешно удалена');
      } catch (error) {
        console.error('Произошла ошибка при удалении цели:', error.response.data);
        throw error;
      }
    },
  },
  mounted() {
    this.fetchTargets();
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap");

.base {
  margin-top: 1rem;
  font-family: 'Montserrat', sans-serif;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.6rem;
}

.page-container {
  font-family: 'Montserrat', sans-serif;
}

.card {
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
  position: relative;
}

.card:hover {
  box-shadow: none;
}

.empty {
  max-width: 30%;
  display: flex;
  flex-direction: column;
  align-items: start;
  font-family: 'Montserrat', sans-serif;
  background-color: #fff;
  padding: 40px;
  border-radius: 25px;
  margin-top: 22px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.3s ease;
}

h1 {
  margin-bottom: 8px;
}
.empty p {
  margin-top: 10px;
}

.target-name {
  font-size: 200px;
  margin-bottom: 5px;
}

.edit {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translate(0, -50%);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  margin-left: 110px;
}

.add-button {
  font-family: 'Montserrat', sans-serif;
  background-color: #9a99de;
  color: #fff;
  height: auto;
  width: 14rem;
  font-size: 14px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 300;
  text-transform: uppercase;
  margin-top: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: block;
  text-align: center;
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

.add-button:hover {
  background-color: #8590de;
}

.content {
  width: 75%;
}

.target-name {
  font-weight: 400;
  font-size: 10px;
  margin-top: 1px;
  margin-bottom: 1px;
  text-transform: capitalize;
}

.target-info {
  display: flex;
}

.target-info-sum {
  font-size: 18px;
  margin-left: 20px;
}

.sum {
  font-size: 1rem;
}

.base h3 {
  font-size: 14px;
  margin-bottom: 1rem;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 10px;
}

.progress-bar {
  flex-grow: 1;
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #9a99de;
  transition: width 0.3s ease;
}

.block {
  margin-bottom: 10px;
  width: 18%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>

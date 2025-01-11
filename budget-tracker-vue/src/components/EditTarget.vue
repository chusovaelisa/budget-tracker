<template>
  <h1>Редактировать цель</h1>
  <form @submit.prevent="submitForm" class="base">
    <div class="group">
      <div class="status">
        <div class="info-c">
          <p>Название:</p>
          <input type="text" v-model="formData.name" :placeholder="target.name">
          <p>Целевая сумма:</p>
          <input type="number" v-model="formData.target_sum" :placeholder="target.target_sum">
          <button type="submit">Изменить</button>
        </div>
        <div class="text">
          Совет классический:<br><br> Для целей лучше использовать короткие названия
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import {editTarget, getTargetId} from "@/services/api.js";

export default {
  data() {
    return {
      target: {
        name: '',
        target_sum: ''
      },
      formData: {
        name: '',
        target_sum: ''
      }
    };
  },
  methods: {
    async fetchTarget() {
      const targetId = this.$route.params.targetId;
      try {
        const response = await getTargetId(targetId);
        this.target = response;
        this.formData.name = response.name;
        this.formData.target_sum = response.target_sum;
      } catch (error) {
        console.error("Ошибка при получении цели:", error.response.data);
        throw error;
      }
    },
    async submitForm() {
      try {
        const targetId = this.$route.params.targetId;
        await editTarget(targetId, {name: this.formData.name, target_sum: this.formData.target_sum});
        this.$router.push('/target-list');
      } catch (error) {
        console.error('Ошибка при обновлении цели:', error.response.data);
      }
    },
  },
  mounted() {
    this.fetchTarget();
  }
};
</script>

<style scoped>
.base {
  display: grid;
  grid-template-columns: repeat(2, 2fr);
  gap: 1.6rem;
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

.base .info {
  display: flex;
  flex-direction: column;
  align-items: start;
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

.target-name {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
}
</style>
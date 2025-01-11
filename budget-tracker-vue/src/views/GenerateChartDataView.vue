<template>
  <div class="chart-container">
    <div v-if="incomeChartData" class="chart income-chart">
      <canvas v-if="incomeChartData.data.length" ref="incomePieChartCanvas" width="300px" height="300px"></canvas>
    </div>
    <div v-if="expenseChartData" class="chart expense-chart">
      <canvas v-if="expenseChartData.data.length" ref="expensePieChartCanvas" width="300px" height="300px"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import { fetchChartData } from "@/services/api.js";

export default {
  data() {
    return {
      incomeChartData: null,
      expenseChartData: null
    };
  },
  async mounted() {
    await Promise.all([this.loadIncomeChartData(), this.loadExpenseChartData()]);
  },
  methods: {
    async loadIncomeChartData() {
      try {
        const incomeData = await fetchChartData('income');
        if (incomeData.data.length) {
          this.incomeChartData = incomeData;
          this.$nextTick(() => {
            const incomeCanvas = this.$refs.incomePieChartCanvas;
            if (incomeCanvas) {
              this.drawIncomePieChart(incomeCanvas, this.incomeChartData);
            }
          });
        }
      } catch (error) {
        console.error('Error loading income chart data:', error);
      }
    },
    async loadExpenseChartData() {
      try {
        const expenseData = await fetchChartData('expense');
        if (expenseData.data.length) {
          this.expenseChartData = expenseData;
          this.$nextTick(() => {
            const expenseCanvas = this.$refs.expensePieChartCanvas;
            if (expenseCanvas) {
              this.drawExpensePieChart(expenseCanvas, this.expenseChartData);
            }
          });
        }
      } catch (error) {
        console.error('Error loading expense chart data:', error);
      }
    },
    drawIncomePieChart(canvas, chartData) {
      const ctx = canvas.getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'Income Data',
            data: chartData.data,
            backgroundColor: chartData.colors
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {
            title: {
              display: true,
              text: 'Доходы'
            },
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const label = chartData.labels[context.dataIndex];
                  const value = chartData.data[context.dataIndex];
                  return `${label}: ${((value).toLocaleString('ru-RU', {style: 'currency', currency: 'RUB'}))}`;
                }
              }
            }
          }
        },
        plugins: [{
          id: 'centerText',
          beforeDraw: function(chart) {
            const width = chart.width,
                  height = chart.height,
                  ctx = chart.ctx;

            ctx.restore();
            const fontSize = (height / 150).toFixed(2);
            ctx.font = `${fontSize}em sans-serif`;
            ctx.textBaseline = 'middle';

            const total = chartData.data.reduce((sum, value) => sum + value, 0);
            const text = total.toLocaleString('ru-RU', {style: 'currency', currency: 'RUB'});
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2 + 10;

            ctx.fillText(text, textX, textY);
            ctx.save();
          }
        }]
      });
    },
    drawExpensePieChart(canvas, chartData) {
      const ctx = canvas.getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'Expense Data',
            data: chartData.data,
            backgroundColor: chartData.colors
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {
            title: {
              display: true,
              text: 'Расходы'
            },
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const label = chartData.labels[context.dataIndex];
                  const value = chartData.data[context.dataIndex];
                  return `${label}: ${((value).toLocaleString('ru-RU', {style: 'currency', currency: 'RUB'}))}`;
                }
              }
            }
          }
        },
        plugins: [{
          id: 'centerText',
          beforeDraw: function(chart) {
            const width = chart.width,
                  height = chart.height,
                  ctx = chart.ctx;

            ctx.restore();
            const fontSize = (height / 150).toFixed(2);
            ctx.font = `${fontSize}em sans-serif`;
            ctx.textBaseline = 'middle';

            const total = chartData.data.reduce((sum, value) => sum + value, 0);
            const text = total.toLocaleString('ru-RU', {style: 'currency', currency: 'RUB'});
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2 + 10;

            ctx.fillText(text, textX, textY);
            ctx.save();
          }
        }]
      });
    }
  }
};
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: flex-start;
  margin-top: 40px;
  margin-left: -20px;
}

.income-chart {
  margin-right: 20px;
}

.chart {
  text-align: center;
}
</style>

<template>
  <div class="container">
    <div class="content">
      <Limit />
      <GenerateChartDataView />
    </div>
    <div class="sidebar">
      <AirDatepicker />
    </div>
  </div>
</template>

<script>
import Limit from "@/views/Limit.vue";
import GenerateChartDataView from "@/views/GenerateChartDataView.vue";
import AirDatepicker from "@/components/AirDatepicker.vue";

export default {
  components: { Limit, GenerateChartDataView, AirDatepicker }
}
</script>

<style scoped>
.container {
  display: flex;
  margin-top: 35px;
}

.content {
  flex: 4;
  margin-right: 60px;
}

.sidebar {
  flex: 2;
  max-width: 400px;
}
</style>

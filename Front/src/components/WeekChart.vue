<template>
  <div class="chart">
    <h2></h2>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      chart: null,
      chartData: null,
    };
  },
  computed: {
    ...mapGetters(["getForecastData"]),
  },
  mounted() {
    this.buildChart();
  },
  methods: {
    buildChart() {
      const forecastData = this.getForecastData.slice(0, 6);
      this.chartData = {
        labels: forecastData.map((day) => new Date(day.date).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' })),
        datasets: [
          {
            label: "5 days weather Forecast !",
            data: forecastData.map((day) => day.temp),
            backgroundColor: "rgba(248, 121, 121, 0.2)",
            borderColor: "#f87979",
            borderWidth: 2,
            pointBackgroundColor: "#f87979",
            pointRadius: 4,
            pointBorderWidth: 1,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: "#f87979",
            pointHoverBorderColor: "#f87979",
            pointHoverBorderWidth: 2,
            fill: true,
          },
        ],
      };
      this.chart = new Chart(this.$refs.chart, {
        type: "line",
        data: this.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          backgroundColor: "rgba(255, 255, 255, 0.8)",
          scales: {
            x: {
              ticks: {
                autoSkip: true,
                maxTicksLimit: 10,
                font: {
                  family: "Roboto",
                  size: 12,
                  weight: 500,
                },
              },
              grid: {
                display: false,
              },
            },
            y: {
              ticks: {
                font: {
                  family: "Roboto",
                  size: 12,
                  weight: 500,
                },
                callback: function (value) {
                  return value + "°C";
                },
                stepSize: 2,
              },
              grid: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          },
        },

      });
    },

  },
  watch: {
    getForecastData() {
      if (this.chart) {
        this.chart.destroy();
      }
      this.buildChart();
    },
  },
};
</script>

<style lang="less" scoped>
.chart {
  max-width: 600px;
  margin: 8px auto;
  height: 200px;
}
</style>


<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

import type { WeatherRecord, WeatherParameter } from '../types'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps<{
  records: WeatherRecord[]
  parameter: WeatherParameter
}>()

const titles: Record<WeatherParameter, string> = {
  temperature: 'Температура, °C',
  feels_like: 'Ощущаемая температура, °C',
  humidity: 'Влажность, %',
  pressure: 'Давление, гПа',
  wind_speed: 'Скорость ветра, м/с'
}

const chartData = computed(() => ({
  labels: props.records.map(record => record.date),
  datasets: [{
    label: titles[props.parameter],
    data: props.records.map(record => record[props.parameter]),
    borderColor: '#8B7CFF',
    backgroundColor: 'rgba(139, 124, 255, 0.12)',
    fill: true,
    tension: 0.35,
    pointRadius: 4,
    pointHoverRadius: 7
  }]
}))

const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: '#9CA3AF' }
    },
    y: {
      grid: { color: '#303846' },
      ticks: { color: '#9CA3AF' }
    }
  }
}
</script>

<template>
  <div class="chart">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.chart {
  position: relative;
  width: 100%;
  height: 320px;
}
</style>

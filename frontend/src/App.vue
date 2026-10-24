<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import type { WeatherRecord, WeatherParameter } from './types'
import WeatherChart from './components/Weatherchart.vue'

const API_URL = 'http://127.0.0.1:8000/api'

const city = ref('')
const cities = ref<string[]>([])
const records = ref<WeatherRecord[]>([])
const parameter = ref<WeatherParameter>('temperature')

const loading = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetch(`${API_URL}/cities`)

    if (!response.ok) {
      throw new Error('Не удалось загрузить список городов')
    }

    cities.value = await response.json()

    if (cities.value.length > 0) {
      city.value = cities.value[0]
    } else {
      error.value = 'В базе пока нет записей о погоде'
    }
  } catch {
    error.value = 'Не удалось подключиться к API. Проверь, запущен ли сервер.'
  }
})

watch(city, async (selectedCity) => {
  records.value = []
  error.value = ''

  if (!selectedCity) return

  loading.value = true

  try {
    const response = await fetch(
      `${API_URL}/weather?city=${encodeURIComponent(selectedCity)}`
    )

    if (!response.ok) {
      throw new Error('Не удалось загрузить историю погоды')
    }

    records.value = await response.json()
  } catch {
    error.value = 'Не удалось загрузить записи для этого города'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="dashboard">
    <header>
      <h1>Weatherly</h1>
      <p>История погодных наблюдений</p>
    </header>

    <section class="toolbar">
      <label for="city">Город</label>

      <select id="city" v-model="city" :disabled="cities.length === 0">
        <option v-for="item in cities" :key="item" :value="item">
          {{ item }}
        </option>
      </select>

      <label for="parameter">Показатель</label>

      <select id="parameter" v-model="parameter">
        <option value="temperature">Температура</option>
        <option value="feels_like">Ощущаемая температура</option>
        <option value="humidity">Влажность</option>
        <option value="pressure">Давление</option>
        <option value="wind_speed">Скорость ветра</option>
      </select>
    </section>

    <p v-if="loading">Загружаем историю погоды...</p>
    <p v-else-if="error" class="message">{{ error }}</p>

    <template v-else-if="records.length > 0">
      <section class="stats">
        <article class="stat-card">
          <span>Температура</span>
          <strong>{{ records[records.length - 1].temperature }} °C</strong>
        </article>

        <article class="stat-card">
          <span>Влажность</span>
          <strong>{{ records[records.length - 1].humidity }} %</strong>
        </article>
      </section>

      <section class="chart-card">
        <h2>{{ city }} — история погоды</h2>
        <WeatherChart :records="records" :parameter="parameter" />
      </section>
    </template>
  </main>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #0d1117;
  color: #f0f3f6;
  font-family: Arial, sans-serif;
}

.dashboard {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 24px;
}

header p,
.stat-card span {
  color: #9ca3af;
}

.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin: 30px 0;
}

select {
  padding: 12px;
  border: 1px solid #303846;
  border-radius: 8px;
  background: #171d27;
  color: white;
}

.stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card,
.chart-card {
  padding: 24px;
  border: 1px solid #303846;
  border-radius: 16px;
  background: #171d27;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-card strong {
  font-size: 28px;
}

.chart-card h2 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 20px;
}

.message {
  color: #fca5a5;
}

@media (max-width: 600px) {
  .dashboard {
    padding: 24px 16px;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .toolbar {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
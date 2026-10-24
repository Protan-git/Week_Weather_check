export interface WeatherRecord {
  date: string
  temperature: number
  feels_like: number
  humidity: number
  pressure: number
  wind_speed: number
  description: string
}

export type WeatherParameter =
  | 'temperature'
  | 'humidity'
  | 'pressure'
  | 'wind_speed'
  | 'feels_like'

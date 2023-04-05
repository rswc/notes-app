import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

declare global {
    interface Window { userId: number | null }
}

app.provide('userId', window.userId)

app.mount('#app')

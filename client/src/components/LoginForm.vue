<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

const username = ref('')
const password = ref('')
const otpKey = ref('')
const isAuthenticated = ref(false)
const otpGood = ref(false)
const message = ref('')

function updateCsrf() {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
}

async function fetchStatus() {
  const r = await axios.get("/api/user/info/")
  isAuthenticated.value = r.data.is_authenticated
  otpGood.value = r.data.otp_good
}

async function onLogin() {
  updateCsrf()
  const r = await axios.post("/api/user/login/", {
    username: username.value,
    password: password.value,
  })
  if (r.data.is_authenticated) {
    message.value = 'Вход выполнен успешно'
    await fetchStatus()
  } else {
    message.value = 'Неверный логин или пароль'
  }
}

async function onOtpLogin() {
  updateCsrf()
  const r = await axios.post("/api/user/otp-login/", {
    key: otpKey.value,
  })
  if (r.data.success) {
    message.value = 'OTP подтверждён'
    otpGood.value = true
  } else {
    message.value = 'Неверный OTP код'
  }
}

async function onLogout() {
  updateCsrf()
  await axios.post("/api/user/logout/")
  isAuthenticated.value = false
  otpGood.value = false
  message.value = 'Выход выполнен'
}

onBeforeMount(async () => {
  await fetchStatus()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Авторизация</h1>

    <div v-if="message" class="alert alert-info mb-3">{{ message }}</div>

    <div v-if="!isAuthenticated" class="mb-3 p-2 border rounded">
      <h5>Вход</h5>
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="username" />
            <label>Логин</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="password" class="form-control" v-model="password" />
            <label>Пароль</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" @click="onLogin">Войти</button>
        </div>
      </div>
    </div>

    <div v-if="isAuthenticated" class="mb-3 p-2 border rounded">
      <p>Вы вошли. OTP статус: <strong>{{ otpGood ? 'подтверждён' : 'не подтверждён' }}</strong></p>

      <div v-if="!otpGood">
        <h5>Введите OTP код</h5>
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="otpKey" />
              <label>OTP код</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-success" @click="onOtpLogin">Подтвердить</button>
          </div>
        </div>
      </div>

      <button class="btn btn-danger mt-2" @click="onLogout">Выйти</button>
    </div>
  </div>
</template>

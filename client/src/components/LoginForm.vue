<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user_store'
import { storeToRefs } from 'pinia'
import Cookies from 'js-cookie'
import axios from 'axios'

const username = ref('')
const password = ref('')
const otpKey = ref('')
const message = ref('')

const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore)

function updateCsrf() {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
}

async function onLogin() {
  updateCsrf()
  await userStore.login(username.value, password.value)
  if (userInfo.value.is_authenticated) {
    message.value = 'Вход выполнен успешно'
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
    await userStore.checkLogin()
  } else {
    message.value = 'Неверный OTP код'
  }
}

async function onLogout() {
  updateCsrf()
  await userStore.logout()
  message.value = 'Выход выполнен'
}
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Авторизация</h1>

    <div v-if="message" class="alert alert-info mb-3">{{ message }}</div>

    <div v-if="!userInfo.is_authenticated" class="mb-3 p-2 border rounded">
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

    <div v-if="userInfo.is_authenticated" class="mb-3 p-2 border rounded">
      <p>Вы вошли как <strong>{{ userInfo.username }}</strong>. OTP статус: <strong>{{ userInfo.otp_good ? 'подтверждён' : 'не подтверждён' }}</strong></p>

      <div v-if="!userInfo.otp_good">
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

<template>
  <div class="container">
    <h1>Профили пользователей</h1>

    <form @submit.prevent.stop="onProfileAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="profileToAdd.user_id" required />
            <label>ID пользователя</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="profileToAdd.balance" required />
            <label>Баланс</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="profileToAdd.avatar" />
            <label>Аватар (URL)</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in profiles" class="d-flex gap-2 align-items-center mt-2">
      <div>{{ item.user?.username }}</div>
      <div>{{ item.balance }}</div>
      <div>{{ item.avatar }}</div>
      <button
        class="btn btn-success"
        @click="onProfileEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editProfileModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editProfileModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="profileToEdit.balance" />
                  <label>Баланс</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="profileToEdit.avatar" />
                  <label>Аватар (URL)</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateProfile">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  fetchProfiles()
})

const profiles = ref([])
const profileToAdd = ref({})
const profileToEdit = ref({})

async function fetchProfiles() {
  const response = await axios.get("/api/profiles/")
  profiles.value = response.data
}

async function onProfileAdd() {
  await axios.post("/api/profiles/", {
    ...profileToAdd.value,
  })
  await fetchProfiles()
}

async function onRemoveClick(profile) {
  await axios.delete(`/api/profiles/${profile.id}/`)
  await fetchProfiles()
}

async function onProfileEditClick(profile) {
  profileToEdit.value = { ...profile }
}

async function onUpdateProfile() {
  await axios.put(`/api/profiles/${profileToEdit.value.id}/`, {
    ...profileToEdit.value,
  })
  await fetchProfiles()
}
</script>

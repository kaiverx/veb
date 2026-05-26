<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const profiles = ref([])
const profileToAdd = ref({})
const profileToEdit = ref({})

async function fetchProfiles() {
  const r = await axios.get("/api/profiles/")
  profiles.value = r.data
}

async function onProfileAdd() {
  await axios.post("/api/profiles/", { ...profileToAdd.value })
  await fetchProfiles()
  profileToAdd.value = {}
}

async function onUpdateProfile() {
  await axios.put(`/api/profiles/${profileToEdit.value.id}/`, { ...profileToEdit.value })
  await fetchProfiles()
}

async function onProfileEditClick(profile) {
  profileToEdit.value = { ...profile }
}

async function onRemoveClick(profile) {
  await axios.delete(`/api/profiles/${profile.id}/`)
  await fetchProfiles()
}

onBeforeMount(async () => {
  await fetchProfiles()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Профили пользователей</h1>

    <div class="p-2 px-0">
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
            <button class="btn btn-primary"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
      </form>
    </div>

    <div class="px-0">
      <div v-for="item in profiles" class="item mb-2 p-2 border rounded">
        <div>
          <strong>{{ item.user?.username }}</strong> - Баланс: {{ item.balance }}
        </div>
        <div class="mt-2">
          <button class="btn btn-success me-2" @click="onProfileEditClick(item)" data-bs-toggle="modal" data-bs-target="#editProfileModal">
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editProfileModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать профиль</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="profileToEdit.balance" />
              <label>Баланс</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="profileToEdit.avatar" />
              <label>Аватар (URL)</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateProfile"><i class="bi bi-check-lg"></i></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item {
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item > div:first-child {
  flex: 1;
}
button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}
button i {
  font-size: 16px;
}
</style>

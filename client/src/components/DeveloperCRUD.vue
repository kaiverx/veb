<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const developers = ref([])
const developerToAdd = ref({})
const developerToEdit = ref({})
const developerPictureRef = ref()
const developerAddImageUrl = ref()
const developerEditPictureRef = ref()
const developerEditImageUrl = ref()
const currentImageUrl = ref('')

function developerAddPictureChange(event) {
  const file = event.target.files[0]
  if (file) {
    developerAddImageUrl.value = URL.createObjectURL(file)
  } else {
    developerAddImageUrl.value = null
  }
}

function developerEditPictureChange(event) {
  const file = event.target.files[0]
  if (file) {
    developerEditImageUrl.value = URL.createObjectURL(file)
  } else {
    developerEditImageUrl.value = null
  }
}

async function fetchDevelopers() {
  const r = await axios.get("/api/developers/")
  developers.value = r.data
}

async function onDeveloperAdd() {
  const formData = new FormData()
  if (developerPictureRef.value && developerPictureRef.value.files[0]) {
    formData.append('picture', developerPictureRef.value.files[0])
  }
  formData.append('developer_name', developerToAdd.value.developer_name)
  formData.append('country', developerToAdd.value.country)
  formData.append('foundation_date', developerToAdd.value.foundation_date)
  await axios.post("/api/developers/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchDevelopers()
  developerToAdd.value = {}
  developerAddImageUrl.value = null
  if (developerPictureRef.value) developerPictureRef.value.value = ''
}

async function onUpdateDeveloper() {
  const formData = new FormData()
  if (developerEditPictureRef.value && developerEditPictureRef.value.files[0]) {
    formData.append('picture', developerEditPictureRef.value.files[0])
  }
  formData.append('developer_name', developerToEdit.value.developer_name)
  formData.append('country', developerToEdit.value.country)
  formData.append('foundation_date', developerToEdit.value.foundation_date)
  await axios.put(`/api/developers/${developerToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchDevelopers()
  developerEditImageUrl.value = null
  if (developerEditPictureRef.value) developerEditPictureRef.value.value = ''
}

async function onDeveloperEditClick(developer) {
  developerToEdit.value = { ...developer }
  if (developer.picture) {
    developerEditImageUrl.value = developer.picture
  } else {
    developerEditImageUrl.value = null
  }
}

async function onRemoveClick(developer) {
  await axios.delete(`/api/developers/${developer.id}/`)
  await fetchDevelopers()
}

function openImageModal(url) {
  currentImageUrl.value = url
}

onBeforeMount(async () => {
  await fetchDevelopers()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Разработчики</h1>

    <div class="p-2 px-0">
      <form @submit.prevent.stop="onDeveloperAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="developerToAdd.developer_name" required />
              <label>Название</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="developerToAdd.country" required />
              <label>Страна</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="date" class="form-control" v-model="developerToAdd.foundation_date" required />
              <label>Дата основания</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="file" class="form-control" ref="developerPictureRef" @change="developerAddPictureChange" />
              <label>Фото</label>
            </div>
          </div>
          <div class="col-auto">
            <img :src="developerAddImageUrl" style="max-height: 60px;" alt="" />
          </div>
          <div class="col-auto">
            <button class="btn btn-primary"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
      </form>
    </div>

    <div class="px-0">
      <div v-for="item in developers" class="item mb-2 p-2 border rounded">
        <div>
          <strong>{{ item.developer_name }}</strong> - {{ item.country }} ({{ item.foundation_date }})
        </div>
        <div v-if="item.picture" class="item-photo">
          <img
            :src="item.picture"
            style="max-height: 60px; cursor: pointer;"
            alt="Фото"
            @click="openImageModal(item.picture)"
            data-bs-toggle="modal"
            data-bs-target="#developerImageModal"
          />
        </div>
        <div v-else>Нет фото</div>
        <div class="mt-2">
          <button class="btn btn-success me-2" @click="onDeveloperEditClick(item)" data-bs-toggle="modal" data-bs-target="#editDeveloperModal">
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editDeveloperModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать разработчика</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="developerToEdit.developer_name" />
              <label>Название</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="developerToEdit.country" />
              <label>Страна</label>
            </div>
            <div class="form-floating mb-2">
              <input type="date" class="form-control" v-model="developerToEdit.foundation_date" />
              <label>Дата основания</label>
            </div>
            <div class="form-floating mb-2">
              <input type="file" class="form-control" ref="developerEditPictureRef" @change="developerEditPictureChange" />
              <label>Фото</label>
            </div>
            <div class="mb-2">
              <img :src="developerEditImageUrl" style="max-height: 100px;" alt="" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateDeveloper"><i class="bi bi-check-lg"></i></button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="developerImageModal" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр фото</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="currentImageUrl" style="max-width: 100%; max-height: 70vh;" alt="Фото" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
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
.item-photo {
  margin-right: 20px;
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

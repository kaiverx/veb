<template>
  <div class="container">
    <h1>Разработчики</h1>

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
        <div class="col-auto">
          <input class="form-control" type="file" ref="developerPictureRef" @change="developerAddPictureChange" />
        </div>
        <div class="col-auto">
          <img :src="developerAddImageUrl" style="max-height: 60px;" alt="" />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in developers" class="d-flex gap-2 align-items-center mt-2">
      <div>{{ item.developer_name }}</div>
      <div>{{ item.country }}</div>
      <div>{{ item.foundation_date }}</div>
      <div v-show="item.picture"><img :src="item.picture" style="max-height: 60px;" /></div>
      <button
        class="btn btn-success"
        @click="onDeveloperEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editDeveloperModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editDeveloperModal" tabindex="-1">
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
                  <input type="text" class="form-control" v-model="developerToEdit.developer_name" />
                  <label>Название</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="developerToEdit.country" />
                  <label>Страна</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="date" class="form-control" v-model="developerToEdit.foundation_date" />
                  <label>Дата основания</label>
                </div>
              </div>
              <div class="col-auto">
                <input class="form-control" type="file" ref="developerEditPictureRef" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateDeveloper">Сохранить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с картинкой -->
    <div class="modal fade" id="pictureModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <img :src="selectedPicture" style="width: 100%;" alt="" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

onBeforeMount(() => {
  fetchDevelopers()
})

const developers = ref([])
const developerToAdd = ref({})
const developerToEdit = ref({})
const developerPictureRef = ref()
const developerEditPictureRef = ref()
const developerAddImageUrl = ref()
const selectedPicture = ref()

async function fetchDevelopers() {
  const response = await axios.get("/api/developers/")
  developers.value = response.data
}

function developerAddPictureChange() {
  developerAddImageUrl.value = URL.createObjectURL(developerPictureRef.value.files[0])
}

async function onDeveloperAdd() {
  const formData = new FormData()
  if (developerPictureRef.value.files[0]) {
    formData.append('picture', developerPictureRef.value.files[0])
  }
  formData.set('developer_name', developerToAdd.value.developer_name)
  formData.set('country', developerToAdd.value.country)
  formData.set('foundation_date', developerToAdd.value.foundation_date)
  await axios.post("/api/developers/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchDevelopers()
}

async function onRemoveClick(developer) {
  await axios.delete(`/api/developers/${developer.id}/`)
  await fetchDevelopers()
}

async function onDeveloperEditClick(developer) {
  developerToEdit.value = { ...developer }
}

async function onUpdateDeveloper() {
  const formData = new FormData()
  if (developerEditPictureRef.value.files[0]) {
    formData.append('picture', developerEditPictureRef.value.files[0])
  }
  formData.set('developer_name', developerToEdit.value.developer_name)
  formData.set('country', developerToEdit.value.country)
  formData.set('foundation_date', developerToEdit.value.foundation_date)
  await axios.put(`/api/developers/${developerToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchDevelopers()
}

function onPictureClick(picture) {
  selectedPicture.value = picture
}
</script>

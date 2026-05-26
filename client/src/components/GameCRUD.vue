<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const games = ref([])
const developers = ref([])
const gameToAdd = ref({})
const gameToEdit = ref({})
const gamePictureRef = ref()
const gameAddImageUrl = ref()
const gameEditPictureRef = ref()
const gameEditImageUrl = ref()
const currentImageUrl = ref('')

function gameAddPictureChange(event) {
  const file = event.target.files[0]
  if (file) {
    gameAddImageUrl.value = URL.createObjectURL(file)
  } else {
    gameAddImageUrl.value = null
  }
}

function gameEditPictureChange(event) {
  const file = event.target.files[0]
  if (file) {
    gameEditImageUrl.value = URL.createObjectURL(file)
  } else {
    gameEditImageUrl.value = null
  }
}

async function fetchGames() {
  const r = await axios.get("/api/games/")
  games.value = r.data
}

async function fetchDevelopers() {
  const r = await axios.get("/api/developers/")
  developers.value = r.data
}

async function onGameAdd() {
  const formData = new FormData()
  if (gamePictureRef.value && gamePictureRef.value.files[0]) {
    formData.append('picture', gamePictureRef.value.files[0])
  }
  formData.append('game_name', gameToAdd.value.game_name)
  formData.append('price', gameToAdd.value.price)
  formData.append('score', gameToAdd.value.score || 0)
  formData.append('info', gameToAdd.value.info)
  formData.append('status', gameToAdd.value.status)
  formData.append('system_requirements', gameToAdd.value.system_requirements)
  formData.append('developer_id', gameToAdd.value.developer_id)
  await axios.post("/api/games/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchGames()
  gameToAdd.value = {}
  gameAddImageUrl.value = null
  if (gamePictureRef.value) gamePictureRef.value.value = ''
}

async function onUpdateGame() {
  const formData = new FormData()
  if (gameEditPictureRef.value && gameEditPictureRef.value.files[0]) {
    formData.append('picture', gameEditPictureRef.value.files[0])
  }
  formData.append('game_name', gameToEdit.value.game_name)
  formData.append('price', gameToEdit.value.price)
  formData.append('score', gameToEdit.value.score || 0)
  formData.append('info', gameToEdit.value.info)
  formData.append('status', gameToEdit.value.status)
  formData.append('system_requirements', gameToEdit.value.system_requirements)
  formData.append('developer_id', gameToEdit.value.developer_id)
  await axios.put(`/api/games/${gameToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchGames()
  gameEditImageUrl.value = null
  if (gameEditPictureRef.value) gameEditPictureRef.value.value = ''
}

async function onGameEditClick(game) {
  gameToEdit.value = { ...game, developer_id: game.developer?.id }
  if (game.picture) {
    gameEditImageUrl.value = game.picture
  } else {
    gameEditImageUrl.value = null
  }
}

async function onRemoveClick(game) {
  await axios.delete(`/api/games/${game.id}/`)
  await fetchGames()
}

function openImageModal(url) {
  currentImageUrl.value = url
}

onBeforeMount(async () => {
  await fetchGames()
  await fetchDevelopers()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Игры</h1>

    <div class="p-2 px-0">
      <form @submit.prevent.stop="onGameAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="gameToAdd.game_name" required />
              <label>Название</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="gameToAdd.price" required />
              <label>Цена</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="gameToAdd.score" step="0.1" />
              <label>Оценка</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="gameToAdd.info" required />
              <label>Описание</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="gameToAdd.status" required>
                <option value="beta">Beta</option>
                <option value="released">Released</option>
                <option value="early access">Early Access</option>
                <option value="coming soon">Coming Soon</option>
              </select>
              <label>Статус</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="gameToAdd.system_requirements" required />
              <label>Системные требования</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="gameToAdd.developer_id" required>
                <option :value="d.id" v-for="d in developers">{{ d.developer_name }}</option>
              </select>
              <label>Разработчик</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="file" class="form-control" ref="gamePictureRef" @change="gameAddPictureChange" />
              <label>Фото</label>
            </div>
          </div>
          <div class="col-auto">
            <img :src="gameAddImageUrl" style="max-height: 60px;" alt="" />
          </div>
          <div class="col-auto">
            <button class="btn btn-primary"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
      </form>
    </div>

    <div class="px-0">
      <div v-for="item in games" class="item mb-2 p-2 border rounded">
        <div>
          <strong>{{ item.game_name }}</strong> - {{ item.developer?.developer_name }} ({{ item.price }}₽, {{ item.status }})
          <br/><small>{{ item.info }} | {{ item.system_requirements }} | Оценка: {{ item.score }}</small>
        </div>
        <div v-if="item.picture" class="item-photo">
          <img
            :src="item.picture"
            style="max-height: 60px; cursor: pointer;"
            alt="Фото"
            @click="openImageModal(item.picture)"
            data-bs-toggle="modal"
            data-bs-target="#gameImageModal"
          />
        </div>
        <div v-else>Нет фото</div>
        <div class="mt-2">
          <button class="btn btn-success me-2" @click="onGameEditClick(item)" data-bs-toggle="modal" data-bs-target="#editGameModal">
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editGameModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать игру</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="gameToEdit.game_name" />
              <label>Название</label>
            </div>
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="gameToEdit.price" />
              <label>Цена</label>
            </div>
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="gameToEdit.score" step="0.1" />
              <label>Оценка</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="gameToEdit.info" />
              <label>Описание</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" v-model="gameToEdit.status">
                <option value="beta">Beta</option>
                <option value="released">Released</option>
                <option value="early access">Early Access</option>
                <option value="coming soon">Coming Soon</option>
              </select>
              <label>Статус</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="gameToEdit.system_requirements" />
              <label>Системные требования</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" v-model="gameToEdit.developer_id">
                <option :value="d.id" v-for="d in developers">{{ d.developer_name }}</option>
              </select>
              <label>Разработчик</label>
            </div>
            <div class="form-floating mb-2">
              <input type="file" class="form-control" ref="gameEditPictureRef" @change="gameEditPictureChange" />
              <label>Фото</label>
            </div>
            <div class="mb-2">
              <img :src="gameEditImageUrl" style="max-height: 100px;" alt="" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateGame"><i class="bi bi-check-lg"></i></button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="gameImageModal" tabindex="-1" data-bs-backdrop="static">
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

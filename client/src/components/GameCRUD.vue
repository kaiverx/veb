<template>
  <div class="container">
    <h1>Игры</h1>

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
        <div class="col-auto">
          <input class="form-control" type="file" ref="gamePictureRef" @change="gameAddPictureChange" />
        </div>
        <div class="col-auto">
          <img :src="gameAddImageUrl" style="max-height: 60px;" alt="" />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in games" class="d-flex gap-2 align-items-center mt-2">
      <div>{{ item.game_name }}</div>
      <div>{{ item.price }}</div>
      <div>{{ item.score }}</div>
      <div>{{ item.info }}</div>
      <div>{{ item.status }}</div>
      <div>{{ item.system_requirements }}</div>
      <div>{{ item.developer?.developer_name }}</div>
      <div v-show="item.picture">
        <img :src="item.picture" style="max-height: 60px;"
          @click="onPictureClick(item.picture)"
          data-bs-toggle="modal"
          data-bs-target="#pictureModal"
        />
      </div>
      <button
        class="btn btn-success"
        @click="onGameEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editGameModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editGameModal" tabindex="-1">
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
                  <input type="text" class="form-control" v-model="gameToEdit.game_name" />
                  <label>Название</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="gameToEdit.price" />
                  <label>Цена</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="gameToEdit.score" step="0.1" />
                  <label>Оценка</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="gameToEdit.info" />
                  <label>Описание</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="gameToEdit.status">
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
                  <input type="text" class="form-control" v-model="gameToEdit.system_requirements" />
                  <label>Системные требования</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="gameToEdit.developer_id">
                    <option :value="d.id" v-for="d in developers">{{ d.developer_name }}</option>
                  </select>
                  <label>Разработчик</label>
                </div>
              </div>
              <div class="col-auto">
                <input class="form-control" type="file" ref="gameEditPictureRef" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateGame">Сохранить</button>
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
  fetchGames()
  fetchDevelopers()
})

const games = ref([])
const developers = ref([])
const gameToAdd = ref({})
const gameToEdit = ref({})
const gamePictureRef = ref()
const gameEditPictureRef = ref()
const gameAddImageUrl = ref()
const selectedPicture = ref()

async function fetchGames() {
  const response = await axios.get("/api/games/")
  games.value = response.data
}

async function fetchDevelopers() {
  const response = await axios.get("/api/developers/")
  developers.value = response.data
}

function gameAddPictureChange() {
  gameAddImageUrl.value = URL.createObjectURL(gamePictureRef.value.files[0])
}

async function onGameAdd() {
  const formData = new FormData()
  if (gamePictureRef.value.files[0]) {
    formData.append('picture', gamePictureRef.value.files[0])
  }
  formData.set('game_name', gameToAdd.value.game_name)
  formData.set('price', gameToAdd.value.price)
  formData.set('score', gameToAdd.value.score || 0)
  formData.set('info', gameToAdd.value.info)
  formData.set('status', gameToAdd.value.status)
  formData.set('system_requirements', gameToAdd.value.system_requirements)
  formData.set('developer_id', gameToAdd.value.developer_id)
  await axios.post("/api/games/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchGames()
}

async function onRemoveClick(game) {
  await axios.delete(`/api/games/${game.id}/`)
  await fetchGames()
}

async function onGameEditClick(game) {
  gameToEdit.value = { ...game, developer_id: game.developer?.id }
}

async function onUpdateGame() {
  const formData = new FormData()
  if (gameEditPictureRef.value.files[0]) {
    formData.append('picture', gameEditPictureRef.value.files[0])
  }
  formData.set('game_name', gameToEdit.value.game_name)
  formData.set('price', gameToEdit.value.price)
  formData.set('score', gameToEdit.value.score || 0)
  formData.set('info', gameToEdit.value.info)
  formData.set('status', gameToEdit.value.status)
  formData.set('system_requirements', gameToEdit.value.system_requirements)
  formData.set('developer_id', gameToEdit.value.developer_id)
  await axios.put(`/api/games/${gameToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchGames()
}

function onPictureClick(picture) {
  selectedPicture.value = picture
}
</script>

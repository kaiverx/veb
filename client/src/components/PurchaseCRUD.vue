<template>
  <div class="container">
    <h1>Покупки</h1>

    <form @submit.prevent.stop="onPurchaseAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="purchaseToAdd.user" required />
            <label>ID пользователя</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="purchaseToAdd.game" required>
              <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
            </select>
            <label>Игра</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="purchaseToAdd.price_at_purchase" required />
            <label>Цена покупки</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in purchases" class="d-flex gap-2 align-items-center mt-2">
      <div>{{ item.user }}</div>
      <div>{{ item.game }}</div>
      <div>{{ item.price_at_purchase }}</div>
      <div>{{ item.purchase_date }}</div>
      <button
        class="btn btn-success"
        @click="onPurchaseEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editPurchaseModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editPurchaseModal" tabindex="-1">
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
                  <input type="number" class="form-control" v-model="purchaseToEdit.user" />
                  <label>ID пользователя</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="purchaseToEdit.game">
                    <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
                  </select>
                  <label>Игра</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="purchaseToEdit.price_at_purchase" />
                  <label>Цена покупки</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdatePurchase">Сохранить</button>
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
  fetchPurchases()
  fetchGames()
})

const purchases = ref([])
const games = ref([])
const purchaseToAdd = ref({})
const purchaseToEdit = ref({})

async function fetchPurchases() {
  const response = await axios.get("/api/purchases/")
  purchases.value = response.data
}

async function fetchGames() {
  const response = await axios.get("/api/games/")
  games.value = response.data
}

async function onPurchaseAdd() {
  await axios.post("/api/purchases/", {
    ...purchaseToAdd.value,
  })
  await fetchPurchases()
}

async function onRemoveClick(purchase) {
  await axios.delete(`/api/purchases/${purchase.id}/`)
  await fetchPurchases()
}

async function onPurchaseEditClick(purchase) {
  purchaseToEdit.value = { ...purchase }
}

async function onUpdatePurchase() {
  await axios.put(`/api/purchases/${purchaseToEdit.value.id}/`, {
    ...purchaseToEdit.value,
  })
  await fetchPurchases()
}
</script>

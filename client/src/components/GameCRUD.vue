<template>
  <div>
    <h2>Games</h2>

    <!-- CREATE -->
    <div class="card p-3 mb-4">
      <h4>Create Game</h4>
      <input v-model="newGame.game_name" placeholder="Title" class="form-control mb-2" />
      <input v-model="newGame.price" type="number" placeholder="Price" class="form-control mb-2" />
      <input v-model="newGame.score" type="number" placeholder="Score (0-10)" step="0.1" max="10" class="form-control mb-2" />
      <input v-model="newGame.info" placeholder="Info" class="form-control mb-2" />

      <select v-model="newGame.status" class="form-control mb-2">
        <option disabled value="">Select status</option>
        <option value="beta">Beta</option>
        <option value="released">Released</option>
        <option value="early access">Early Access</option>
        <option value="coming soon">Coming Soon</option>
      </select>

      <select v-model="newGame.developer_id" class="form-control mb-2">
        <option disabled value="">Select Developer</option>
        <option v-for="dev in developers" :key="dev.id" :value="dev.id">
          {{ dev.developer_name }}
        </option>
      </select>

      <h5>System Requirements</h5>
      <input v-model="newGame.system_requirements.cpu" placeholder="CPU" class="form-control mb-2" />
      <input v-model="newGame.system_requirements.gpu" placeholder="GPU" class="form-control mb-2" />
      <input v-model="newGame.system_requirements.memory" placeholder="Memory" class="form-control mb-2" />
      <input v-model="newGame.system_requirements.storage" placeholder="Storage" class="form-control mb-2" />
      <input v-model="newGame.system_requirements.os" placeholder="Operating System" class="form-control mb-2" />

      <button @click="createGame" class="btn btn-success">Create</button>
    </div>

    <!-- LIST -->
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Price</th>
          <th>Score</th>
          <th>Info</th>
          <th>Status</th>
          <th>Developer</th>
          <th>System Requirements</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="game in games" :key="game.id">
          <td>{{ game.id }}</td>
          <td><input v-model="game.game_name" class="form-control" /></td>
          <td><input v-model="game.price" type="number" class="form-control" /></td>
          <td><input v-model="game.score" type="number" step="0.1" max="10" class="form-control" /></td>
          <td><input v-model="game.info" class="form-control" /></td>

          <td>
            <select v-model="game.status" class="form-control">
              <option value="beta">Beta</option>
              <option value="released">Released</option>
              <option value="early access">Early Access</option>
              <option value="coming soon">Coming Soon</option>
            </select>
          </td>

          <td>
            <select v-model="game.developer_id" class="form-control">
              <option v-for="dev in developers" :key="dev.id" :value="dev.id">
                {{ dev.developer_name }}
              </option>
            </select>
          </td>

          <td>
            <input v-model="game.system_requirements.cpu" placeholder="CPU" class="form-control mb-1" />
            <input v-model="game.system_requirements.gpu" placeholder="GPU" class="form-control mb-1" />
            <input v-model="game.system_requirements.memory" placeholder="Memory" class="form-control mb-1" />
            <input v-model="game.system_requirements.storage" placeholder="Storage" class="form-control mb-1" />
            <input v-model="game.system_requirements.os" placeholder="OS" class="form-control mb-1" />
          </td>

          <td>
            <button @click="updateGame(game)" class="btn btn-primary me-2">Update</button>
            <button @click="deleteGame(game.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      games: [],
      developers: [],
      newGame: {
        game_name: "",
        price: 0,
        score: 0,
        info: "",
        status: "",
        developer_id: null,
        system_requirements: {
          cpu: "",
          gpu: "",
          memory: "",
          storage: "",
          os: "",
        },
      },
    };
  },

  mounted() {
    this.loadGames();
    this.loadDevelopers();
  },

  methods: {
    async loadGames() {
      const response = await axios.get("http://127.0.0.1:8000/api/games/");
      this.games = response.data;
    },

    async loadDevelopers() {
      const response = await axios.get("http://127.0.0.1:8000/api/developers/");
      this.developers = response.data;
    },

    async createGame() {
      const payload = { ...this.newGame };
      await axios.post("http://127.0.0.1:8000/api/games/", payload);
      this.loadGames();
      this.resetNewGame();
    },

    async updateGame(game) {
      const payload = {
        game_name: game.game_name,
        price: game.price,
        score: game.score,
        info: game.info,
        status: game.status,
        developer_id: game.developer_id,
        system_requirements: game.system_requirements,
      };
      await axios.put(`http://127.0.0.1:8000/api/games/${game.id}/`, payload);
      this.loadGames();
    },

    async deleteGame(id) {
      await axios.delete(`http://127.0.0.1:8000/api/games/${id}/`);
      this.loadGames();
    },

    resetNewGame() {
      this.newGame = {
        game_name: "",
        price: 0,
        score: 0,
        info: "",
        status: "",
        developer_id: null,
        system_requirements: {
          cpu: "",
          gpu: "",
          memory: "",
          storage: "",
          os: "",
        },
      };
    },
  },
};
</script>

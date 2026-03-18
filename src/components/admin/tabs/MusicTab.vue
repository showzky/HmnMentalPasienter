<template>
  <section class="music-admin">
    <div class="data-widget">
      <h3>Manage Bangerfabrikken Playlist</h3>
      <table class="playlist-table">
        <thead>
          <tr>
            <th style="width: 30px;"></th>
            <th>Title</th>
            <th>Artist</th>
            <th>SoundCloud URL</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody ref="playlistTable" class="playlist-table">
          <tr v-for="(element, index) in playlist" :key="element.id">
            <td class="drag-handle" style="cursor: grab;">☰</td>
            <td>{{ element.title }}</td>
            <td>{{ element.artist }}</td>
            <td>{{ element.soundcloudUrl }}</td>
            <td>
              <button class="delete-song" @click="$emit('deleteSong', element.id)">Delete</button>
              <button class="edit-song" @click="$emit('editSong', element.id)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="form-group-music">
        <label>Title</label>
        <input :value="newSong.title" @input="updateNewSong('title', $event.target.value)" />
      </div>
      <div class="form-group-music">
        <label>Artist</label>
        <input :value="newSong.artist" @input="updateNewSong('artist', $event.target.value)" />
      </div>
      <div class="form-group-music">
        <label>Cover URL</label>
        <input :value="newSong.cover" @input="updateNewSong('cover', $event.target.value)" />
      </div>
      <div class="form-group-music">
        <label>SoundCloud URL</label>
        <input :value="newSong.soundcloudUrl" @input="updateNewSong('soundcloudUrl', $event.target.value)" />
      </div>
      <button @click="$emit('saveSong')" class="create-role-button">
        {{ editingIndex !== null ? 'Update Song' : 'Add Song' }}
      </button>
      <div v-if="playlistMessage" class="form-message" :class="{ success: playlistSuccess, error: !playlistSuccess }">
        {{ playlistMessage }}
      </div>
    </div>
  </section>
</template>

<script>
import Sortable from 'sortablejs';

export default {
  props: [
    'playlist',
    'newSong',
    'editingIndex',
    'playlistMessage',
    'playlistSuccess'
  ],
  emits: [
    'saveSong',
    'deleteSong',
    'editSong',
    'playlistDragEnd',
    'update:newSong'
  ],
  methods: {
    updateNewSong(field, value) {
      const updatedSong = { ...this.newSong, [field]: value };
      this.$emit('update:newSong', updatedSong);
    }
  },
  mounted() {
    this.$nextTick(() => {
      const playlistTable = this.$refs.playlistTable;
      if (playlistTable && !playlistTable._sortable) {
        try {
          playlistTable._sortable = new Sortable(playlistTable, {
            swap: true,
            swapClass: 'highlighted',
            animation: 200,
            easing: "cubic-bezier(0.2, 0, 0, 1)",
            ghostClass: 'sortable-ghost',
            dragClass: 'sortable-drag',
            handle: '.drag-handle',
            onEnd: (evt) => {
              this.$emit('playlistDragEnd', evt);
            }
          });
          console.log("Sortable initialized with swap on playlist table");
        } catch (e) {
          console.error("Error initializing Sortable on playlist:", e);
        }
      }
    });
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>

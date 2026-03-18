<template>
  <section class="changelog-admin">
    <div class="data-widget">
      <h3>Create New Changelog Entry</h3>
      <form @submit.prevent="$emit('submitChangelogEntry')">
        <div class="form-group">
          <label for="version">Version</label>
          <input
            type="text"
            id="version"
            :value="newChangelog.version"
            @input="updateChangelog('version', $event.target.value)"
            placeholder="e.g., 1.1.0"
            required
          />
        </div>
        <div class="form-group">
          <label for="date">Date</label>
          <input
            type="date"
            id="date"
            :value="newChangelog.date"
            @input="updateChangelog('date', $event.target.value)"
            required
          />
        </div>
        <div class="form-group">
          <label for="added">Added</label>
          <textarea
            id="added"
            :value="newChangelog.added"
            @input="updateChangelog('added', $event.target.value)"
            placeholder="List of added features (one per line)"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="changed">Changed</label>
          <textarea
            id="changed"
            :value="newChangelog.changed"
            @input="updateChangelog('changed', $event.target.value)"
            placeholder="List of changes (one per line)"
          ></textarea>
        </div>
        <button type="submit" class="create-event-button">Add Changelog Entry</button>
      </form>
      <div v-if="changelogMessage" class="form-message" :class="{ success: changelogSuccess, error: !changelogSuccess }">
        {{ changelogMessage }}
      </div>
    </div>
    <div class="data-widget">
      <h3>Existing Changelog Entries</h3>
      <table class="changelog-table">
        <thead>
          <tr>
            <th>Version</th>
            <th>Date</th>
            <th>Added</th>
            <th>Changed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in changelogEntries" :key="entry.id">
            <td>{{ entry.version }}</td>
            <td>{{ entry.date }}</td>
            <td>
              <ul>
                <li v-for="item in entry.added" :key="item">{{ item }}</li>
              </ul>
            </td>
            <td>
              <ul>
                <li v-for="item in entry.changed" :key="item">{{ item }}</li>
              </ul>
            </td>
            <td>
              <button class="delete-button" @click="$emit('deleteChangelogEntry', entry.id)">Delete</button>
            </td>
          </tr>
          <tr v-if="changelogEntries.length === 0">
            <td colspan="5" class="no-entries">No changelog entries found</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  props: [
    'newChangelog',
    'changelogEntries',
    'changelogMessage',
    'changelogSuccess'
  ],
  emits: [
    'submitChangelogEntry', 
    'deleteChangelogEntry', 
    'update:newChangelog'
  ],
  methods: {
    updateChangelog(field, value) {
      const updatedChangelog = { ...this.newChangelog, [field]: value };
      this.$emit('update:newChangelog', updatedChangelog);
    }
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>

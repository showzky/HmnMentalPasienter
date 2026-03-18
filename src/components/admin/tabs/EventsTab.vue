<template>
  <section>
    <div class="event-list-card">
      <div class="existing-events-header">
        <h3>Existing Events</h3>
        <input type="text" :value="searchQuery" @input="$emit('update:searchQuery', $event.target.value)" placeholder="Search Events..." class="search-input" />
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width: 30px;"></th> <!-- Drag handle column -->
              <th>Event Name</th>
              <th>Date</th>
              <th>Time</th>
              <th style="width: 100px;">Actions</th>
            </tr>
          </thead>
          <tbody ref="eventsTable" class="events-table">
            <tr v-for="(element, index) in upcomingEventsData" :key="element.id">
              <td class="drag-handle" style="cursor: grab;">☰</td>
              <td>{{ element.event_name }}</td>
              <td>{{ formatDate(element.event_date) }}</td>
              <td>{{ formatTime(element.event_time) }}</td>
              <td>
                <button @click="$emit('deleteEvent', element.id)" class="delete-button">Delete</button>
              </td>
            </tr>
          </tbody>
          <tbody v-if="upcomingEventsData.length === 0">
            <tr>
              <td colspan="5" class="no-events">No events found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="create-event-card">
      <h3>Create New Event</h3>
      <div class="form-grid">
        <div class="form-group">
          <label for="event-name">Name</label>
          <input 
            type="text" 
            id="event-name" 
            :value="newEvent.event_name" 
            @input="updateNewEvent('event_name', $event.target.value)" 
            placeholder="Event Title" />
        </div>
        <div class="form-group">
          <label for="event-date">Date</label>
          <input 
            type="date" 
            id="event-date" 
            :value="newEvent.event_date" 
            @input="updateNewEvent('event_date', $event.target.value)" />
        </div>
        <div class="form-group">
          <label for="event-time">Time</label>
          <input 
            type="time" 
            id="event-time" 
            :value="newEvent.event_time" 
            @input="updateNewEvent('event_time', $event.target.value)" />
        </div>
        <div class="form-group">
          <label for="template_name">Template</label>
          <select 
            id="template_name" 
            :value="newEvent.template_name" 
            @input="updateNewEvent('template_name', $event.target.value)" 
            required>
            <option value="" disabled>Select a Template</option>
            <option value="template1">Template 1 (Image-Focused)</option>
            <option value="template2">Template 2 (Text-Focused)</option>
          </select>
        </div>
      </div>
      <div class="form-group full-width">
        <label for="event-description">Description (Optional)</label>
        <textarea 
          id="event-description" 
          :value="newEvent.event_description" 
          @input="updateNewEvent('event_description', $event.target.value)" 
          placeholder="Short event details..."></textarea>
      </div>
      <div class="form-group full-width file-upload-group">
        <label for="event_image" class="file-upload-label">
          <span>Choose an Image</span>
          <input type="file" id="event_image" @change="$emit('handleImageUpload', $event)" accept="image/*" class="hidden-file-input" />
        </label>
      </div>
      <div class="checkbox-group">
        <label class="custom-checkbox">
          <input 
            type="checkbox" 
            :checked="newEvent.notify_users" 
            @change="updateNewEvent('notify_users', $event.target.checked)" />
          Notify all users
        </label>
      </div>
      <button @click="$emit('createEvent')" class="create-event-button">Create</button>
      <div v-if="createEventMessage" class="form-message" :class="{ success: createEventSuccess, error: !createEventSuccess }">
        {{ createEventMessage }}
      </div>
    </div>
    <div class="data-widget">
      <h3>Upcoming Events</h3>
      <ul>
        <li v-for="event in upcomingEventsData" :key="event.id">
          <router-link :to="`/events/${event.id}`" class="event-link">
            {{ event.event_name }} - {{ formatDate(event.event_date) }}, {{ formatTime(event.event_time) }}
          </router-link>
        </li>
        <li v-if="upcomingEventsData.length === 0">
          <p>No upcoming events scheduled yet.</p>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
export default {
  props: [
    'searchQuery',
    'upcomingEventsData',
    'newEvent',
    'createEventMessage',
    'createEventSuccess'
  ],
  emits: [
    'deleteEvent', 
    'handleImageUpload', 
    'createEvent', 
    'update:searchQuery', 
    'update:newEvent'
  ],
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    formatTime(timeString) {
      return timeString;
    },
    updateNewEvent(field, value) {
      const updatedEvent = { ...this.newEvent, [field]: value };
      this.$emit('update:newEvent', updatedEvent);
    }
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>

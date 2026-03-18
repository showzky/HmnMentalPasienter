<template>
  <section>
    <div class="data-widget">
      <h3>Latest Activity</h3>
      <ul>
        <li v-for="item in widgets.find(w => w.id === 'latest-activity').activityItems" :key="item.text">
          {{ item.text }}
        </li>
      </ul>
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
    'upcomingEventsData',
    'widgets'
  ],
  methods: {
    formatDate(dateString) {
      // Implement formatDate method or receive it as a prop
      return new Date(dateString).toLocaleDateString();
    },
    formatTime(timeString) {
      // Implement formatTime method or receive it as a prop
      return timeString;
    }
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>

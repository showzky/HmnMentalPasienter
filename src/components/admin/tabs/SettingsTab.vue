<template>
  <div class="data-widget">
    <h3>Maintenance Settings</h3>
    <div class="maintenance-controls">
      <div class="checkbox-group">
        <label class="custom-checkbox">
          <input 
            type="checkbox" 
            :checked="maintenanceMode" 
            @change="updateMaintenanceMode($event.target.checked)" />
          Enable Maintenance Mode
        </label>
      </div>
      <div class="checkbox-group">
        <label class="custom-checkbox">
          <input 
            type="checkbox" 
            :checked="noticeMaintenanceMode" 
            @change="updateNoticeMaintenanceMode($event.target.checked)" />
          Enable Banner Maintenance Mode
        </label>
      </div>
      <div class="message-input-container" v-if="noticeMaintenanceMode">
        <input 
          type="text" 
          :value="maintenanceBannerMessage" 
          @input="updateMaintenanceBannerMessage($event.target.value)"
          placeholder="Enter maintenance message..."
        />
        <button 
          class="update-message-button" 
          @click="$emit('onToggleNoticeMaintenance')"
          :disabled="!maintenanceBannerMessage.trim()"
        >
          Update Message
        </button>
      </div>
      <div v-if="maintenanceMessage" class="form-message" :class="{ success: maintenanceSuccess, error: !maintenanceSuccess }">
        {{ maintenanceMessage }}
      </div>
      <div v-if="noticeMaintenanceMessage" class="form-message" :class="{ success: noticeMaintenanceSuccess, error: !noticeMaintenanceSuccess }">
        {{ noticeMaintenanceMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'maintenanceMode',
    'noticeMaintenanceMode',
    'maintenanceBannerMessage',
    'maintenanceMessage',
    'maintenanceSuccess',
    'noticeMaintenanceMessage',
    'noticeMaintenanceSuccess'
  ],
  emits: [
    'onToggleMaintenance', 
    'onToggleNoticeMaintenance', 
    'update:maintenanceMode',
    'update:noticeMaintenanceMode',
    'update:maintenanceBannerMessage'
  ],
  methods: {
    updateMaintenanceMode(value) {
      this.$emit('update:maintenanceMode', value);
      this.$emit('onToggleMaintenance');
    },
    updateNoticeMaintenanceMode(value) {
      this.$emit('update:noticeMaintenanceMode', value);
      this.$emit('onToggleNoticeMaintenance');
    },
    updateMaintenanceBannerMessage(value) {
      this.$emit('update:maintenanceBannerMessage', value);
    }
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>

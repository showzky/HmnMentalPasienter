<template>
  <div class="achievement-tab">
    <AchievementAdmin />
  </div>
</template>

<script>
import AchievementAdmin from '@/components/AchievementAdmin.vue';

export default {
  name: 'AchievementTab',
  components: { AchievementAdmin }
};
</script>

<style scoped>
.achievement-tab {
  width: 100%;
  height: 100%;
}
</style> 
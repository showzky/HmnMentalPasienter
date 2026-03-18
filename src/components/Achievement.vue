<template>
  <div class="achievement" :class="{ locked: !achieved }">
    <div class="achievement-icon">
      <img v-if="isImgUrlField(imageSrc)" :src="imageSrc" alt="Achievement Icon" />
      <span v-else v-html="imageSrc"></span>
    </div>
    <span class="achievement-name">{{ title }}</span>
    <span class="achievement-desc" v-if="achieved">{{ description }}</span>
    <span class="achievement-desc locked-desc" v-else>Locked</span>
    <span class="achievement-meta">Rarity: {{ rarity }}</span>
    <span class="achievement-meta">Glow Color: {{ glow_color }}</span>
  </div>
</template>

<script>
export default {
  props: {
    svg: String,
    icon: String,
    title: String,
    description: String,
    achieved: Boolean,
    rarity: String,
    glow_color: String
  },
  computed: {
    imageSrc() {
      // Prefer svg, fallback to icon
      return this.svg || this.icon;
    }
  },
  methods: {
    isImgUrlField(icon) {
      return (
        typeof icon === 'string' &&
        (
          icon.endsWith('.svg') ||
          icon.endsWith('.png') ||
          icon.endsWith('.jpg') ||
          icon.endsWith('.jpeg') ||
          icon.startsWith('data:image') ||
          icon.startsWith('http')
        )
      );
    }
  },
  mounted() {
    console.log('Achievement.vue imageSrc:', this.imageSrc);
  }
}
</script>

<style scoped>
.achievement {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
  opacity: 1;
  filter: none;
  transition: filter 0.2s, opacity 0.2s;
}
.achievement.locked {
  opacity: 0.5;
  filter: grayscale(1) brightness(0.7);
}
.achievement-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.achievement-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.achievement-name {
  font-weight: 600;
  color: #222;
  text-align: center;
}
.achievement-desc {
  font-size: 0.95em;
  color: #666;
  margin-top: 0.2em;
}
.locked-desc {
  color: #aaa;
  font-style: italic;
}
</style>
<template>
    <div class="badge-preview">
      <!-- If icon is a URL, show as image only -->
      <img
        v-if="isUrlIcon"
        :src="icon"
        class="svg-preview"
        :alt="description || 'Badge icon'"
      />
      <!-- If icon is inline SVG, render as HTML -->
      <span
        v-else-if="icon && icon.startsWith('<svg')"
        v-html="icon"
        class="svg-preview"
      ></span>
      <!-- Otherwise, render badge shape with emoji/char -->
      <span v-else class="badge" :class="rarity" :title="description">
        {{ icon || 'Badge' }}
      </span>
    </div>
  </template>
  
  <script>
  export default {
    props: ['icon', 'rarity', 'glowColor', 'description'],
    computed: {
      isUrlIcon() {
        return (
          typeof this.icon === 'string' &&
          (this.icon.startsWith('data:image/svg+xml') || this.icon.endsWith('.svg'))
        );
      }
    }
  }

  
  </script>
  
  <style scoped>
/* Remove all .badge and rarity CSS from here to use the global/shared badge styles */
.badge-preview {
  margin-top: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  display: flex; /* Center content */
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}
.svg-preview {
  width: 38px;
  height: 38px;
  background: #222;
  border-radius: 1em;
  box-shadow: 0 0 8px 1px #1e90ff22;
  padding: .28em;
  margin: .07em 0;
  display: inline-block;
  vertical-align: middle;
}
.badge {
  display: inline-block;
  font-size: 2rem;
  padding: 0.3em 0.7em;
  border-radius: 1em;
  background: #eee;
  color: #333;
  font-weight: 600;
}
  </style>
  
<template>
  <div>
    <HomeLoggedIn v-if="auth.isAuthenticated" :user="auth.user" />

    <div v-else>
      <!-- Hero Section -->
      <div class="hero">
        <h1>HMN Mental Pasienter</h1>
        <p class="slogan">Profesjonelle uansvarlige siden 2024</p>
      </div>

      <!-- Timeline Section -->
      <div class="hero">
        <div class="timeline-meme">
          <div class="timeline-item">
            <div class="timeline-emoji">🎉</div>
            <div class="timeline-text">
              <h3>Født i kaos</h3>
              <p>"Vi møttes faktisk først i 2024 alle sammen face to face" - Thomas, probably</p>
            </div>
          </div>
          <div class="timeline-item discord-highlight">
            <div class="timeline-emoji">🎮</div>
            <div class="timeline-text">
              <h3>TimeCraft Discord</h3>
              <p>
                Hovedkvarter for:
                <br />
                <span class="discord-activities">
                  Memes å gode samtaler seriøse samtaler  🗿 av og til xD 
                  <br />
                  velkommen skarru være🍕
                </span>
              </p>
              <button class="discord-btn" @click="openDiscord">
                Bli med i koret av kaos
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Meeting Section -->
      <section class="meeting-section">
        <h2>🏔️ Historisk Øyeblikk</h2>
        <div class="meeting-card">
          <p class="meeting-date">August 2024</p>
          <h3>Den store Sunndalsøra-konspirasjonen</h3>
          <p>Hva skjedde egentlig der oppe? Verden vil aldri vite...</p>
          <div class="classified">
            🔒 KLASSIFISERT
            <span class="tooltip">(Spør Kim-Andre om passord)</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import HomeLoggedIn from '@/components/HomeLoggedIn.vue';
import { useAuthStore } from '@/stores/authStore';
export default {
  name: 'Home',
  components: {
    HomeLoggedIn
  },
  setup() {
    const auth = useAuthStore();
    return { auth };
  },
  methods: {
    openDiscord() {
      window.open('https://discord.gg/z8XkcvtaRs', '_blank');
    }
  }
};
</script>

<style scoped>
/* Optional - Keep global styles in your main `style.css` file */
/* Add any section-specific tweaks here if necessary */
</style>
  
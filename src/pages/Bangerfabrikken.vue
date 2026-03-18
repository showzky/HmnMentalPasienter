<template>
  <div class="bangerfabrikken-page">
    <div class="main-content-wrapper">
      <div class="music-content">
        <!-- Hero Section -->
        <section class="hero-section redesigned-hero">
          <div class="hero-bg-animated"></div>
          <div class="hero-content">
            <h1>Bangerfabrikken 🔥</h1>
            <p class="slogan">Lager bangere på bekostning av andre</p>
            <div class="music-visualizer-placeholder">
              <!-- Placeholder for animated music visualizer -->
              <span class="bar"></span><span class="bar"></span><span class="bar"></span><span class="bar"></span>
            </div>
          </div>
        </section>

        <!-- Current Song Highlight -->
        <section v-if="currentSong" class="current-song glass-card">
          <img :src="currentSong.cover" :alt="currentSong.title" class="current-song-cover" @error="onImageError" />
          <div class="current-song-info">
            <h2>{{ currentSong.title }}</h2>
            <p>{{ currentSong.artist }}</p>
           <!-- <div class="song-progress-bar">
              ADDE SENERE KANSJE xD
              <div class="progress"></div>
            </div>-->
          </div>
        </section>

        <!-- Carousel Section -->
        <section class="carousel-section">
          <div class="swiper-container" ref="swiperContainer">
            <div class="swiper">
              <div class="swiper-wrapper" id="swiper-wrapper">
                <div
                  v-for="(song, index) in songs"
                  :key="song.id"
                  class="swiper-slide"
                  @click="currentSongIndex = index"
                >
                  <img
                    :src="song.cover"
                    :alt="song.title"
                    class="album-cover"
                    @error="onImageError"
                  />
                  <div class="overlay">
                    <h3>{{ song.title }}</h3>
                    <p>{{ song.artist }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-pagination"></div>
        </section>

        <!-- SoundCloud Player -->
        <section class="soundcloud-section">
          <div v-if="currentSong" class="soundcloud-embed">
            <iframe
              width="100%"
              height="166"
              scrolling="no"
              frameborder="no"
              :src="`https://w.soundcloud.com/player/?url=${currentSong.soundcloudUrl}&color=%23ff69b4&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false`"
            ></iframe>
          </div>
        </section>
      </div>
      <!-- News Section ADD LATER ? -->  
    <!--  <aside class="news-section">
        <h2>Nyheter</h2>
        <ul>
          <li>🎉 Ny låt sluppet i dag!</li>
          <li>📰 Sjekk ut vårt nye intervju med DJ Banger!</li>  
          <li>🔥 Konkurranse: Vinn merch!</li>
        </ul>
      </aside>-->
    </div>
  </div>
</template>


<script>
import { ref, onMounted, nextTick, computed, onUnmounted } from 'vue';
import axios from 'axios'; // Import axios to fetch the playlist
import Swiper from 'swiper';
import { Mousewheel } from 'swiper/modules';
import 'swiper/css'; // Core Swiper CSS
import 'swiper/css/effect-coverflow'; // Coverflow effect CSS

export default {
  name: 'Bangerfabrikken',
  setup() {
    // -----------------------------------------------------
    // Reactive State Variables
    // -----------------------------------------------------
    // 'songs' will hold the playlist fetched from your backend.
    const songs = ref([]);
    // 'currentSongIndex' tracks the active slide (song) in the carousel.
    const currentSongIndex = ref(0);
    // 'currentSong' computed property returns the currently active song,
    // or null if the songs array is empty.
    const currentSong = computed(() => {
      return songs.value.length ? songs.value[currentSongIndex.value] : null;
    });
    // Reference for the Swiper container element.
    const swiperContainer = ref(null);


// In Bangerfabrikken.vue, add this to the setup function:
const updateSwiperOrder = (orderMap) => {
  // 1️⃣ Build a lookup from id → song object
  const songById = songs.value.reduce((acc, song) => {
    acc[song.id] = song;
    return acc;
  }, {});

  // 2️⃣ Reconstruct the songs[] in the new admin-driven order
  songs.value = orderMap
    .slice()                                // clone so we don't mutate the incoming array
    .sort((a, b) => a.position - b.position)
    .map(({ id }) => songById[id])
    .filter(Boolean);                       // drop any missing IDs

  // 3️⃣ Reset highlight to first track
  currentSongIndex.value = 0;

  // 4️⃣ Tell Swiper to update & snap back to slide 0
  nextTick(() => {
    const inst = swiperContainer.value
                  ?.querySelector('.swiper')
                  ?.swiper;
    if (!inst) {
      console.warn('Swiper instance not found after reorder');
      return;
    }
    inst.update();                          // regenerate slides
    if (typeof inst.slideToLoop === 'function') {
      inst.slideToLoop(0);
    } else {
      inst.slideTo(0);
    }
    console.log(`Swiper carousel updated, moved to first slide`);
  });
};

// Create a named handler function for event listening
const playlistChangeHandler = function(event) {
  console.log('playlist-order-changed event received');
  updateSwiperOrder(event.detail);
};

// Then update the onMounted to use the named handler
onMounted(async () => {
  console.log('Bangerfabrikken mounting...');
  
  // Initial fetch for songs
  await fetchPlaylist();
  
  // Initialize Swiper if we have songs
  if (songs.value.length > 0) {
    await nextTick();
    console.log('Initializing Swiper with songs');
    initSwiper();
  }

  // Add listener for playlist order changes using the named handler
  console.log('Adding playlist-order-changed event listener');
  window.addEventListener('playlist-order-changed', playlistChangeHandler);
});

// Replace the onUnmounted hook with this version
onUnmounted(() => {
  console.log('Bangerfabrikken unmounting, removing event listeners');
  
  // Remove the event listener using the named handler
  window.removeEventListener('playlist-order-changed', playlistChangeHandler);
  
  // Clean up Swiper
  const swiperEl = swiperContainer.value?.querySelector('.swiper');
  const swiper = swiperEl?.swiper;
  if (swiper && typeof swiper.destroy === 'function') {
    console.log('Destroying Swiper instance');
    swiper.destroy();
  }
});

    // -----------------------------------------------------
    // Fallback Image Handler
    // -----------------------------------------------------
    // If a song cover fails to load, use a default cover.
    let loggedImageErrorOnce = false;

const onImageError = (event) => {
  if (!loggedImageErrorOnce) {
    console.warn('⚠️ One or more images failed to load, using default cover image.');
    loggedImageErrorOnce = true;
  }
  event.target.src = new URL('@/assets/albumcoversbs/default.jpg', import.meta.url).href;
};

    // -----------------------------------------------------
    // Fetch Playlist Function
    // -----------------------------------------------------
    // Fetches the playlist from the backend endpoint '/api/playlist'
    // Expected response format: { songs: [ { title, artist, cover, soundcloudUrl, ... }, ... ] }
    const fetchPlaylist = async () => {
      try {
        console.log('Fetching playlist from backend...');
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/playlist`);
        
        // Log the raw response to verify the data structure
        console.log('Raw playlist response:', res.data);
        
        if (!res.data || !res.data.songs || !Array.isArray(res.data.songs)) {
          console.error('Invalid playlist data format received:', res.data);
          return;
        }
        
        // Always sort by position to ensure consistent order
        const sortedSongs = [...res.data.songs].sort((a, b) => a.position - b.position);
        console.log('Sorted songs by position:', sortedSongs.map(s => `${s.title}:${s.position}`));
        
        // Update the songs array and always set to first song
        songs.value = sortedSongs;
        currentSongIndex.value = 0;
        console.log(`Setting to first song in playlist:`, songs.value[0]?.title);
        
        // Wait for DOM updates before updating Swiper
        await nextTick();
        
        // Update Swiper if it exists
        const swiperEl = swiperContainer.value?.querySelector('.swiper');
        const swiper = swiperEl?.swiper;
        if (swiper) {
          swiper.update();
          
          // Always move to the first song (index 0)
          if (typeof swiper.slideToLoop === 'function') {
            swiper.slideToLoop(0);
          } else {
            swiper.slideTo(0);
          }
          
          console.log(`Swiper updated after fetch, moved to first slide`);
        }
      } catch (e) {
        console.error('Error fetching playlist:', e);
      }
    };



    // -----------------------------------------------------
    // Initialize Swiper Carousel Function
    // -----------------------------------------------------
    // Initializes the Swiper carousel with coverflow effect after the DOM updates.
    const initSwiper = () => {
      if (swiperContainer.value) {
        const swiperEl = swiperContainer.value.querySelector('.swiper');
        if (swiperEl) {
          new Swiper(swiperEl, {
            modules: [Mousewheel],
            direction: 'horizontal',
            effect: 'coverflow',
            grabCursor: true,
            loop: true,
            speed: 500, // Smoother transition
            centeredSlides: true,
            slidesPerView: 'auto',
            spaceBetween: 30, // Add spacing between slides
            coverflowEffect: {
              rotate: 10, // Reduced rotation for less perspective
              stretch: 0,
              depth: 40, // Reduced depth for less zoom
              modifier: 0.7, // Reduced modifier for milder effect
              slideShadows: false, // Disable shadows for a cleaner look
            },
            freemode: {
              enabled: true,
            },
            mousewheel: {
            enabled: true, // Enable mousewheel
            forceToAxis: true,
            sensitivity: 1,
            releaseOnEdges: true,
            invert: false
        },
            navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
            },
            pagination: {
              el: '.swiper-pagination',
              clickable: true,
            },
            on: {
              slideChange: function () {
                currentSongIndex.value = this.realIndex;
              },
            },
          });
        }
      }
    };

    // Return reactive properties and functions for use in the template.
    return { songs, currentSongIndex, currentSong, swiperContainer, onImageError };
  },
};
</script>




<style scoped>
/* =============================== */
/* Global Page Styling */
/* =============================== */
.bangerfabrikken-page {
  background: var(--bg);
  color: var(--text);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  min-height: 100vh;
  transition: background-color 0.3s ease;
}
:root,
.bangerfabrikken-page {
  --current-song-title: #000000;   /* Black for light mode */
  --current-song-paragraph: #000000;
  --soundcloud-section-text: #ff0000;
}


.main-content-wrapper {
  display: flex;
  width: 100%;
  max-width: 1400px;
  gap: 32px;
  justify-content: center;
}
.music-content {
  min-width: 0;
  max-width: 900px;
}
/*.news-section {
  flex: 1;
  background: #181818;
  border-radius: 16px;
  padding: 24px 18px;
  margin-top: 40px;
  min-width: 260px;
  max-width: 350px;
  box-shadow: 0 0 20px rgba(255, 105, 180, 0.08);
  height: fit-content;
}
.news-section h2 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #ff69b4;
}
.news-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.news-section li {
  margin-bottom: 0.8rem;
  font-size: 1.05rem;
  line-height: 1.5;
  background: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 8px 12px;
}
@media (max-width: 900px) {
  .main-content-wrapper {
    flex-direction: column;
    gap: 0;
  }
  .news-section {
    margin-top: 24px;
    max-width: 100%;
    width: 100%;
  }
}*/

/* =============================== */
/* Hero Section */
/* =============================== */
.hero-section {
  text-align: center;
  margin-bottom: 40px;
  color: var(--text); /* Use variable text color */
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 10px;
  font-weight: bold;
  text-shadow: 0 0 15px rgba(117, 47, 82, 0.8);
  color: var(--primary-accent); /* Use accent color for heading */
}

.slogan {
  font-size: 1.3rem;
  opacity: 0.85;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
  color: var(--secondary-text); /* Use secondary text color */
}

/* Dark mode variables */
.dark-mode {
  --bg: #212529;
  --text: #dee2e6;
  --card-bg: #343a40;
  --primary-accent: #ffffff;
  --secondary-text: #f7f7f7;
  --border-color: #495057;
  --current-song-title: #fff;      /* White for dark mode */
  --current-song-paragraph: #eee;  /* Light gray for dark mode */
  --soundcloud-section-text: #fff;
}

/* Apply dark mode to the page when the class is active */
.dark-mode .bangerfabrikken-page {
  background: var(--bg);
  color: var(--text);
}

/* =============================== */
/* Current Song Highlight */
/* =============================== */
.current-song {
  display: flex;
  align-items: center;
  gap: 20px;
  background: linear-gradient(135deg, #1f1c2c, #292d45); /* Keep specific gradient */
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 40px;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 0 25px rgba(10, 4, 4, 0.699); /* Keep specific shadow */
}
/* Removed duplicate .bangerfabrikken-page rule */

.current-song-cover {
  width: 110px;
  height: 110px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(255, 105, 180, 0.5); /* Keep specific shadow */
}

.current-song-info h2 {
  margin: 0;
  font-size: 1.5rem;
}

.current-song-info p {
  margin: 5px 0 0;

}




/* =============================== */
/* Carousel Section */
/* =============================== */
.carousel-section {
  width: 100%;
  height: 400px;
  max-width: 1000px;
  margin: 60px 0 60px 0; /* 60px top and bottom margin */
  background: transparent;
  border-radius: 20px;
  padding: 40px 0; /* 40px top and bottom padding */
  box-shadow: none;
  overflow: hidden;
  overflow-x: hidden;
}
.swiper {
  width: 100%;
  overflow: visible;
}
.swiper-wrapper {
  overflow: visible;
}
.swiper-slide {
  position: relative;
  width: 300px;
  height: 300px;
  border-radius: 20px;
  overflow: hidden;
  background: #181a20;
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
  transition: box-shadow 0.3s, background 0.3s, transform 0.3s;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.swiper-slide .album-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 20px;
  background: #eee;
}
.overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 12px 5px 0px 10px;
  background: linear-gradient(240deg, transparent, transparent, rgba(38, 21, 149, 0.8));
  border-radius: 20px;
  color: #fff;
  z-index: 2;
  pointer-events: none;
}
.overlay h3 {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 12px 0;
}
.overlay p {
  font-size: 1.1rem;
  margin: 0 0 18px 0;
  opacity: 0.85;
}
@media (max-width: 900px) {
  .swiper-slide {
    width: 350px;
    height: 180px;
    border-radius: 14px;
  }
  .swiper-slide .album-cover {
    border-radius: 14px;
  }
  .overlay {
    padding: 12px 18px;
    border-radius: 14px;
  }
  .overlay h3 {
    font-size: 1.2rem;
  }
}

/* =============================== */
/* SoundCloud Section */
/* =============================== */
.soundcloud-section {
  width: 100%;
  max-width: 900px;
  background: linear-gradient(135deg, #1c1c1c, #2e2e2e); /* Keep specific gradient */
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3); /* Keep specific shadow */
  transition: transform 0.3s ease;
  color: var(--soundcloud-section-text);
  margin-top: 40px;

}

.soundcloud-section:hover {
  transform: scale(1.02);
  box-shadow: 0 0 30px rgba(255, 105, 180, 0.5);
}

.soundcloud-embed iframe {
  border-radius: 12px;
  overflow: hidden;
}

/* =============================== */
/* Responsive */
/* =============================== */
@media (max-width: 600px) {
  .hero-content h1 {
    font-size: 2.2rem;
  }

  .slogan {
    font-size: 1rem;
  }



  .current-song-cover {
    width: 100px;
    height: 100px;
  }

  .swiper-slide {
    width: 180px;
    height: 180px;
  }

  /* Adjust rotation on smaller screens if needed */
  .swiper-slide:not(.swiper-slide-active) {
     transform: scale(0.9) rotateY(-10deg); /* Slightly less rotation */
  }



}

/***** Redesigned Hero Section *****/
.redesigned-hero {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
  min-height: 180px;
}
.hero-bg-animated {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 0;
  background: linear-gradient(120deg, var(--primary-accent, #ff69b4) 0%, #6a82fb 100%);
  opacity: 0.18;
  filter: blur(16px);
  animation: bgMove 8s ease-in-out infinite alternate;
}
@keyframes bgMove {
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
}
.hero-content {
  position: relative;
  z-index: 1;
  padding: 36px 0 24px 0;
}
.music-visualizer-placeholder {
  display: flex;
  gap: 4px;
  margin-top: 18px;
  height: 24px;
  align-items: flex-end;
  justify-content: center;
}
.music-visualizer-placeholder .bar {
  width: 6px;
  height: 12px;
  background: var(--primary-accent, #ff69b4);
  border-radius: 3px;
  animation: visualizerBar 1.2s infinite alternate;
  opacity: 0.7;
}
.music-visualizer-placeholder .bar:nth-child(2) { animation-delay: 0.2s; }
.music-visualizer-placeholder .bar:nth-child(3) { animation-delay: 0.4s; }
.music-visualizer-placeholder .bar:nth-child(4) { animation-delay: 0.6s; }
@keyframes visualizerBar {
  0% { height: 12px; }
  100% { height: 24px; }
}

/***** Glassmorphism Card for Current Song *****/
.glass-card {
  background: rgba(170, 156, 156, 0.18);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);

  border-radius: 20px;
  border: 1.5px solid rgba(255,255,255,0.22);
  transition: background 0.3s, box-shadow 0.3s;
}
.dark-mode .glass-card {
  background: rgba(40,40,60,0.32);
  border: 1.5px solid rgba(80,80,120,0.22);
}

/***** Song Progress Bar *****/
.song-progress-bar {
  width: 100%;
  height: 7px;
  background: rgba(200,200,200,0.18);
  border-radius: 4px;
  margin-top: 18px;
  overflow: hidden;
}
.song-progress-bar .progress {
  width: 60%; /* Placeholder width, can be dynamic */
  height: 100%;
  background: linear-gradient(90deg, var(--primary-accent, #ff69b4), #6a82fb);
  border-radius: 4px;
  transition: width 0.5s;
}

/***** Responsive Adjustments *****/
@media (max-width: 600px) {
  .redesigned-hero {
    min-height: 120px;
    border-radius: 14px;
  }
  .glass-card {
    border-radius: 14px;
  }
}

/* Add this at the end of your style block: */
:global(.dark-mode) .bangerfabrikken-page {
  --current-song-title: #fff;
  --current-song-paragraph: #eee;
  --bg: #212529;
  --text: #dee2e6;
  --card-bg: #343a40;
  --primary-accent: #ffffffc9;
  --secondary-text: #f7f7f7;
  --border-color: #495057;
  --soundcloud-section-text: #fff;
}
</style>

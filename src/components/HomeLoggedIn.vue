<template>
  <div class="home-logged-in">
    <!-- Welcome Section -->
    <section class="welcome-section">
      <div class="welcome-card">
        <div class="welcome-header">
          <h2>👋 Welcome back, {{ user.username }}!</h2>
        </div>
        <div class="user-stats">
          <div class="stat-item">
            <span class="stat-label">Rank</span>
            <span class="stat-value">{{ user.roles[0]?.name || 'Member' }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Fitte Points</span>
            <span class="stat-value">{{ user.fittePoints }}</span>
          </div>
        </div>
      </div>
    </section>

    <div class="content-grid">
      <!-- What's New Section -->
      <section class="whats-new-section content-card">
        <div class="section-header">
          <h3>✨ What's News</h3>
        </div>
        <div class="news-container">
          <p v-if="newsItems.length === 0" class="no-news">No news items available right now</p>
          <div v-else class="news-items">
            <div v-for="item in topNews" :key="item.id" class="news-item">
              <div class="news-header">
                <h4 class="news-title">{{ item.title }}</h4>
                <span class="news-date">{{ new Date(item.date).toLocaleDateString() }}</span>
              </div>
              <div class="news-content" v-html="getNewsPreview(item.content)"></div>
            </div>
          </div>
        </div>
        <div class="section-footer">
          <router-link to="/news" class="view-all-link">
            <button class="secondary-button">See All News</button>
          </router-link>
        </div>
      </section>

      <!-- Community Stats -->
      <section class="community-stats content-card">
        <div class="section-header">
          <h3>👥 Community Highlights</h3>
        </div>
        <ul class="stats-list">
          <li>
            <span class="stat-icon">👥</span>
            <span>Total Users: {{ stats.totalUsers }}</span>
          </li>
          <li>
            <span class="stat-icon">🔥</span>
            <span>Active This Week: {{ stats.activeThisWeek }}</span>
          </li>
          <li>
            <span class="stat-icon">🏆</span>
            <span>Top User: {{ stats.topUser }}</span>
          </li>
        </ul>
      </section>

      <!-- Upcoming Events -->
      <section class="upcoming-events content-card">
        <div class="section-header">
          <h3>📅 Upcoming Events</h3>
        </div>
        <ul class="events-list">
          <li v-for="event in displayedEvents" :key="event.id" class="event-item">
            <span class="event-icon">🎮</span>
            <router-link :to="`/events/${event.id}`" class="event-link">
              <span class="event-name">{{ event.name }}</span>
              <span class="event-date">{{ event.date }}</span>
            </router-link>
          </li>
        </ul>
        <div class="section-footer">
          <button class="secondary-button">See Full Calendar</button>
        </div>
      </section>

      <!-- Daily Reward Button -->
      <section class="daily-reward content-card">
        <div class="section-header">
          <h3>🎁 Daily Reward</h3>
        </div>
        <div class="reward-container">
          <p>Click to get your daily Fitte Points!</p>
          <button @click="claimDailyReward" :disabled="dailyClaimed">
            Claim Daily Reward
          </button>
          <p v-if="dailyClaimed" class="claimed-message">✅ You already claimed today's reward!</p>
          <p v-if="dailyClaimed && countdown > 0" class="countdown-message">
            Next reward in {{ formatTime(countdown) }}
          </p>
        </div>
      </section>
      <section class="discord-widget content-card">
        <div class="section-header">
          <h3>
            <img
              src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png"
              alt="Discord logo" class="discord-logo" width="24" height="24" />
            Join Our Discord
          </h3>
        </div>
        <div class="discord-content">
          <p>Connect with the community, get help, and participate in voice chats!</p>
          <a href="https://discord.gg/z8XkcvtaRs" target="_blank" rel="noopener noreferrer" class="discord-button">
            Join Server
          </a>
        </div>
      </section>

      <!-- Games & Fun Card -->
      <section class="games-fun content-card">
        <div class="section-header">
          <h3>🎮 Games & Fun</h3>
        </div>
        <div class="games-fun-content">
          <p>
            <strong>Try out our upcoming games and fun features!</strong><br>
            <span class="ps-text">
              PS: <span class="highlight">Pre Alpha 1.0 is live</span> <br>
              Click the button below to check it out!
            </span>
          </p>
          <router-link to="/clicker-game">
            <button class="cookie-clicker-btn">Cookie Clicker</button>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'
import { io } from 'socket.io-client';
export default {
  name: 'HomeLoggedIn',
  props: {
    user: Object
  },
  data() {
    return {
      countdown: 0,
      countdownInterval: null,
      stats: {
        totalUsers: 0,
        activeThisWeek: 0,
        topUser: '',
        dailyClaimed: false,
        nextClaimTime: null,
      },
      events: [],
      newsItems: [],
      dailyClaimed: false,
      fittePoints: 0
    };
  },
  computed: {
    displayedEvents() {
      // Only show the first 3 events
      return this.events.slice(0, 3);
    },
    topNews() {
      return this.newsItems.slice(0, 3);
    }
  },
  methods: {
    async fetchDailyClaimStatus() {
      try {
        const res = await axios.get('get-daily-claim-status', {
          headers: { Authorization: `Bearer ${this.user.token}` }
        });
        this.dailyClaimed = res.data.dailyClaimed;
        this.nextClaimTime = res.data.nextClaimTime;

        if (this.dailyClaimed && this.nextClaimTime) {
          const now = new Date();
          const nextTime = new Date(this.nextClaimTime);
          const diffSeconds = Math.floor((nextTime - now) / 1000);

          if (diffSeconds > 0) {
            this.countdown = diffSeconds;
            this.startCountdown();
          }
        }
      } catch (err) {
        console.error('Failed to fetch daily claim status:', err);
      }
    },


    async fetchStats() {
      // placeholder → fetch from API later
      this.stats = {
        totalUsers: 123,
        activeThisWeek: 45,
        topUser: 'Showzky'
      };
    },
    async fetchEvents() {
      try {
        const res = await axios.get('events', {
          headers: { Authorization: `Bearer ${this.user.token}` }
        });

        // The API returns events in res.data.events
        this.events = res.data.events.map(event => ({
          id: event.id,
          name: event.event_name,
          date: new Date(event.event_date).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
          }),
          time: event.event_time.split(':').slice(0, 2).join(':'),
          description: event.event_description
        }));
      } catch (err) {
        console.error('Failed to fetch events:', err);
        // Fallback to placeholder data if API call fails
        this.events = [
          { id: 1, name: 'Game Night', date: 'May 20', time: '19:00' },
          { id: 2, name: 'Meme Contest', date: 'May 25', time: '20:00' },
          { id: 3, name: 'Movie Night', date: 'June 2', time: '18:00' }
        ];
      }
    },
    async fetchNewsItems() {
      try {
        const res = await axios.get('news', {
          headers: { Authorization: `Bearer ${this.user.token}` }
        });
        this.newsItems = Array.isArray(res.data) ? res.data.slice(0, 5) : [];
      } catch (err) {
        console.error('Failed to fetch news:', err);
        this.newsItems = [];
      }
    },

    startCountdown() {
      if (this.countdownInterval) clearInterval(this.countdownInterval);

      this.countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(this.countdownInterval);
          this.dailyClaimed = false;
        }
      }, 1000); // run every second
    },

    formatTime(seconds) {
      const days = Math.floor(seconds / (24 * 3600));
      const hours = Math.floor((seconds % (24 * 3600)) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;

      let parts = [];
      if (days > 0) parts.push(`${days}d`);
      if (hours > 0 || days > 0) parts.push(`${hours}h`);
      if (minutes > 0 || hours > 0 || days > 0) parts.push(`${minutes}m`);
      parts.push(`${secs.toString().padStart(2, '0')}s`);
      return parts.join(' ');
    },

    async claimDailyReward() {
      try {
        const currentPoints = this.user.fittePoints;
        const newPoints = currentPoints + 50;

        this.dailyClaimed = true;

        const res = await axios.post('update-fitte-points', {
          points: newPoints,
          is_daily_reward: true
        }, {
          headers: { Authorization: `Bearer ${this.user.token}` }
        });

        if (res.data && res.data.points) {
          this.user.fittePoints = res.data.points;
          this.fittePoints = res.data.points;

          // Update timer with server time if available
          if (res.data.nextClaimTime) {
            const now = new Date();
            const nextTime = new Date(res.data.nextClaimTime);
            const diffSeconds = Math.floor((nextTime - now) / 1000);

            if (diffSeconds > 0) {
              this.countdown = diffSeconds;
              this.startCountdown();
            }
          }

          this.$emit('daily-reward-claimed');
        } else {
          console.error('Invalid response format from update-fitte-points:', res.data);
        }
      } catch (err) {
        console.error('Failed to update Fitte Points:', err);
        // If there's an error, reset the claimed state
        this.dailyClaimed = false;
        clearInterval(this.countdownInterval);
      }
    },

    async fetchFittePoints() {
      try {
        const res = await axios.get('get-fitte-points', {
          headers: { Authorization: `Bearer ${this.user.token}` }
        });

        if (res.data && res.data.points !== undefined) {
          this.user.fittePoints = res.data.points;
          this.fittePoints = res.data.points;
        } else {
          console.error('Invalid response format from get-fitte-points:', res.data);
        }
      } catch (err) {
        console.error('Failed to fetch Fitte Points:', err);
      }
    },

    getNewsPreview(content) {
      // Remove HTML tags for preview, or keep simple tags if you want
      const text = content.replace(/<[^>]+>/g, ''); // strip HTML tags
      const maxLength = 100;
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + '...';
      }
      return text;
    },

  },
  mounted() {
    this.fetchStats();
    this.fetchEvents();
    this.fetchFittePoints();
    this.fetchNewsItems();
    this.fetchDailyClaimStatus();

    const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000';
    const socket = io(socketUrl, {
      path: '/socket.io',
      transports: ['websocket', 'polling'],
      secure: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    });

    // Add error handling
    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
    });

    socket.on('connect', () => {
      console.log('Successfully connected to socket server');
      // Emit setUserId event after successful connection
      if (this.user && this.user.id) {
        socket.emit('setUserId', this.user.id);
      }
    });

    socket.on('daily_reward_claimed', (data) => {
      if (data.user_id === this.user.id) {
        console.log('Received daily_reward_claimed event');
        this.dailyClaimed = true;
        this.countdown = data.cooldown || 24 * 3600;  // Use 10 seconds or pull this from backend later THIS IS ISSUE 
        this.startCountdown();
      }
    });
  },

}
</script>

<style scoped>
.home-logged-in {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section,
.content-card {
  margin-bottom: 2rem;
}

.welcome-card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.countdown-message {
  color: #ff9800;
  font-weight: 500;
}

.welcome-header h2 {
  margin: 0;
  color: var(--primary);
  font-size: 1.8rem;
}

.user-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.ps-text {
  display: block;
  margin-top: 0.7em;
  font-size: 1.08em;
  color: #235c88;
  background: #f5fafd;
  padding: 0.7em 1em;
  border-radius: 0.6em;
  font-weight: 500;
  box-shadow: 0 1px 6px #b3d0ea33;
}
.highlight {
  color: #ff006e;
  font-weight: 700;
  background: #fffbe7;
  padding: 0.1em 0.4em;
  border-radius: 0.4em;
}


/* Card Styling */
.content-card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-self: start;
}

/* Section Headers */
.section-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.75rem;
}

.section-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

/* Section Footer */
.section-footer {
  margin-top: auto;
  padding-top: 1rem;
  display: flex;
  justify-content: center;
}

/* News Items */
.news-container {
  padding: 0.5rem;
}

.no-news {
  text-align: center;
  color: #64748b;
  font-style: italic;
  padding: 1rem;
}

.news-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.news-item {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1.25rem;
  transition: all 0.2s ease;
  border: 1px solid #e2e8f0;
}

.news-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.news-title {
  margin: 0;
  font-size: 1.1rem;
  color: var(--primary, #2c3e50);
  font-weight: 600;
}

.news-date {
  font-size: 0.9rem;
  color: #64748b;
}

.news-content {
  color: #4b5563;
  font-size: 0.95rem;
  line-height: 1.5;
}

.news-content :deep(p) {
  margin: 0.5rem 0;
}

.news-content :deep(a) {
  color: var(--primary, #3b82f6);
  text-decoration: none;
}

.news-content :deep(a:hover) {
  text-decoration: underline;
}

.view-all-link {
  text-decoration: none;
}

/* Stats List */
.stats-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stats-list li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stat-icon {
  font-size: 1.25rem;
}

/* Events List */
.events-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.event-icon {
  font-size: 1.25rem;
}

.event-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-grow: 1;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  text-decoration: none;
  color: var(--primary, #333);
  transition: background-color 0.2s ease;
}

.event-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.event-name {
  font-weight: 500;
}

.event-date {
  color: #666;
}

/* Reward Section */
.reward-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.claimed-message {
  color: #4caf50;
  font-weight: 500;
}

/* Buttons */
button {
  padding: 0.5rem 1rem;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

button:disabled {
  background: #e0e0e0;
  color: #888;
  cursor: not-allowed;
}

.secondary-button {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--primary);
}

.secondary-button:hover {
  background: rgba(var(--primary-rgb, 0, 123, 255), 0.1);
}

.daily-reward button {
  background: linear-gradient(to bottom right, #ffd700, #ffaa00);
  color: black;
  font-weight: bold;
  padding: 0.7rem 1.2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.daily-reward button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.daily-reward button:disabled {
  background: #e0e0e0;
  color: #888;
}

.discord-logo {
  vertical-align: middle;
  margin-right: 8px;
}

.discord-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
}

.discord-button {
  background-color: #5865F2;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.discord-button:hover {
  background-color: #4752C4;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.games-fun-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  text-align: center;
}

.cookie-clicker-btn {
  background: linear-gradient(90deg, #ffd700 60%, #ffb300 100%);
  color: #235c88;
  font-weight: bold;
  font-size: 1.1rem;
  padding: 0.7rem 2.2rem;
  border: none;
  border-radius: 0.7rem;
  cursor: pointer;
  box-shadow: 0 2px 8px #ffd70080;
  transition: background 0.18s, filter 0.2s;
  margin-top: 0.7rem;
  text-shadow: 0 2px 6px #fffbe7bb;
}

.cookie-clicker-btn:hover {
  filter: brightness(1.08) drop-shadow(0 0 8px #ffd700);
}
</style>

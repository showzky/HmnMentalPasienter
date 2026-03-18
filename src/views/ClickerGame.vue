<template>
  <div class="clicker-game gamified-bg">
    <div class="game-header">
      <h2>Fitte Clicker</h2>
      <div class="score-bar">
        <span class="score-label">Fitte Points:</span>
        <span class="score-value">{{ score.toLocaleString('nb-NO') }}</span>
        <span class="score-pps">/ per click: {{ totalPointsPerClick }}</span>
        <span v-if="totalAutoClickers > 0" class="score-auto">/ auto: {{ totalAutoClickers }}/s</span>
      </div>
    </div>
    <div class="game-flex">
      <!-- Left: Cookie + Score -->
      <div class="cookie-area">
        <div class="score-display">
          <div class="main-score">{{ score.toLocaleString() }}</div>
          <div class="per-click">per click: {{ totalPointsPerClick }}</div>
          <div v-if="totalAutoClickers > 0" class="per-auto">Auto: {{ totalAutoClickers }}/s</div>
        </div>
        <div class="cookie-spotlight">
          <div class="cookie-wrapper larger-cookie">
            <svg
              @click="handleCookieClick"
              :class="{'cookie-svg': true, 'pop': cookiePopping}"
              width="300" height="300" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg"
            >
              <circle cx="110" cy="110" r="85" fill="#2679b8" opacity="0.9"/>
              <ellipse cx="95" cy="95" rx="45" ry="18" fill="#fff" opacity="0.13"/>
              <rect x="105" y="60" width="14" height="80" rx="7" fill="#fff"/>
              <path d="M110 73 Q85 60 75 95 Q100 90 110 92" fill="#fff"/>
              <path d="M110 73 Q135 60 145 95 Q120 90 110 92" fill="#fff"/>
              <circle cx="110" cy="66" r="12" fill="#fff"/>
              <path d="M110 100 Q117 110 110 120 Q103 130 110 140 Q117 150 110 160 Q103 170 110 180" stroke="#fff" stroke-width="6" fill="none"/>
              <ellipse cx="110" cy="180" rx="9" ry="6" fill="#fff" />
            </svg>
            <transition-group name="float" tag="div" class="floaters badge-floaters">
<div
  v-for="floater in floaters"
  :key="floater.id"
  class="floater"
  :class="{ crit: floater.value.toString().startsWith('CRIT!') }"
  :style="{ left: floater.x + 'px', top: floater.y + 'px' }"
>
  +{{ floater.value }}
</div>

            </transition-group>
<div
  v-for="n in totalAutoClickers"
  :key="n"
  class="auto-clicker-visual"
  :class="{ tap: activeAutoClickers.includes(n - 1) }"
  :style="autoClickerStyle(n, totalAutoClickers, activeAutoClickers.includes(n - 1))"
>
  <template v-if="autoClickerUpgrade && isUrl(autoClickerUpgrade.icon)">
    <img :src="autoClickerUpgrade.icon" class="auto-clicker-icon-img" />
  </template>
  <template v-else-if="autoClickerUpgrade">
    <span v-html="autoClickerUpgrade.icon"></span>
  </template>
</div>

          </div>
        </div>
        <button v-if="score > 0" @click="resetScore" class="reset-btn">Reset</button>
      </div>

      <!-- Center: Convert -->
      <div class="convert-center">
        <div class="convert-card prominent-convert-card">
          <div class="fitte-balance-badge">
            <span class="fitte-balance-label">Your Fitte Points:</span>
            <span class="fitte-balance-value">{{ fittePoints.toLocaleString('nb-NO') }}</span>
          </div>
          <div class="convert-title">Convert Points to Fitte Points</div>
          <div class="convert-guide">
            Convert your clicker points to Fitte Points!<br>
            <span class="convert-tier">Conversion rates:</span><br>
            <span>First 10,000 points: <b>1,000</b> = 1 Fitte Point</span><br>
            <span>Next 40,000: <b>2,000</b> = 1</span><br>
            <span>After 50,000: <b>5,000</b> = 1</span>
          </div>
          <div class="convert-summary">
            <span>You will get <b>{{ conversionResult.fittePoints }}</b> Fitte Points</span><br>
            <span>Points used: <b>{{ conversionResult.pointsUsed }}</b></span><br>
            <span>Points left: <b>{{ conversionResult.pointsLeft }}</b></span>
          </div>
          <button class="convert-btn" :disabled="conversionResult.fittePoints === 0" @click="convertToFittePoints">
            Convert
          </button>
        </div>
      </div>


      
      <!-- Right: Shop -->
<div class="shop-panel">
  <div class="store-header-row">
  <div class="store-header">Store</div>
    <button class="leaderboard-btn" @click="$router.push('/clicker-leaderboard')">
    🏆 Leaderboard
  </button>
  </div>
  <div class="sidebar-upgrade-list scrollable-store">
          <div v-for="upgrade in upgrades" :key="upgrade.id" class="sidebar-upgrade-card" :class="{ disabled: score < upgrade.cost || (upgrade.unlocksAfter && !canUnlock(upgrade)) }">
            <div class="sidebar-upgrade-row">
              <span class="sidebar-upgrade-icon">
  <template v-if="isUrl(upgrade.icon)">
    <img :src="upgrade.icon" alt="" class="upgrade-icon-img" />
  </template>
  <template v-else>
    <span v-html="upgrade.icon"></span>
  </template>
</span>
              <span class="sidebar-upgrade-name">
                {{ upgrade.name }}
                <span class="sidebar-upgrade-qty">
                  <template v-if="upgrade.id === 'click'">x{{ upgrade.amountOwned }}</template>
                  <template v-else-if="upgrade.id === 'auto'">x{{ upgrade.amountOwned }}</template>
                  <template v-else>x{{ upgrade.amountOwned }}</template>
                </span>
              </span>
              <span class="sidebar-upgrade-cost">Cost: {{ upgrade.cost }}</span>
              <button
                class="sidebar-upgrade-buy-btn"
                :disabled="score < upgrade.cost || (upgrade.unlocksAfter && !canUnlock(upgrade))"
                @click="buyUpgradeCard(upgrade)"
              >
                <template v-if="upgrade.unlocksAfter && !canUnlock(upgrade)">🔒</template>
                <template v-else>Buy</template>
              </button>
            </div>
            <div class="sidebar-upgrade-desc">{{ upgrade.desc }}</div>
            <div class="xp-bar" style="margin: 6px 0 0 0;">
              <div class="xp-bar-fill" :style="{ width: getUpgradeBarWidth(upgrade) }"></div>
            </div>
            <div v-if="upgrade.unlocksAfter && !canUnlock(upgrade)" class="sidebar-upgrade-locked-msg">
              <small>Unlocks after {{ upgrade.unlocksAfter.count }} Fitte Power upgrades.</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <SnackBar
      v-if="snackbar.show"
      :message="snackbar.message"
      :type="snackbar.type"
      @close="hideSnackBar"
    />
    <AchievementPopup
      ref="achievementPopup"
      :title="popupTitle"
      :description="popupDescription"
      :image="popupImage"
      :duration="4000"
    />
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { ref, reactive, computed, onMounted, onUnmounted ,watch } from 'vue';
import axios from '@/axios';
import { useAuthStore } from '@/stores/authStore';
import SnackBar from '@/components/SnackBar.vue';
import AchievementPopup from '@/components/AchievementPopup.vue';
import upgradesList from '@/views/upgrades.js'


const auth = useAuthStore();
const { user, token } = storeToRefs(auth);

const snackbar = ref({
    show: false,
    message: '',
    type: 'success',
});
const score = ref(0);
const pointsPerClick = ref(1);
const cookiePopping = ref(false);
const floaters = ref([]);
const autoClickers = ref(0);
const fittePoints = ref(0);
const isLoadingFittePoints = ref(false);
const activeAutoClickers = ref([]);
const popupTitle = ref('');
const popupDescription = ref('');
const orbitAngle = ref(0);
const popupImage = ref('');
const autoClickerUpgrade = computed(() => upgrades.value.find(u => u.id === 'auto'));
const achievementPopup = ref(null);
let floaterId = 0;
let autoClickerInterval = null;
let pendingClicks = 0;
let batchTimer = null;
const BATCH_INTERVAL = 3000; // This is 3 seconds cus its ms
function isUrl(icon) {
  return typeof icon === 'string' && (icon.startsWith('http://') || icon.startsWith('https://'));
}
// Centralized upgrade state
const upgrades = ref(upgradesList);

// Computed values for UI display
const totalPointsPerClick = computed(() => {
  return 1 + upgrades.value.reduce((total, upgrade) => {
    if (upgrade.effectType === 'addPPC') {
      return total + (upgrade.effectAmount * (upgrade.amountOwned || 0));
    }
    if (upgrade.effectType === 'addPPCFraction') {
      return total + (upgrade.effectAmount * (upgrade.amountOwned || 0));
    }
    return total;
  }, 0);
});

const totalAutoClickers = computed(() => {
  return upgrades.value.reduce((total, upgrade) => {
    if (upgrade.effectType === 'addAuto') {
      return total + (upgrade.effectAmount * (upgrade.amountOwned || 0));
    }
    return total;
  }, 0);
});

// Watch for changes in auto clickers to update the interval
watch(totalAutoClickers, (newValue) => {
  autoClickers.value = newValue;
  stopAutoClickers();
  startAutoClickers();
});

// Watch for changes in points per click
watch(totalPointsPerClick, (newValue) => {
  pointsPerClick.value = newValue;
});

// 1. Define all achievements here (copy from your JSON)
const achievements = [
  {
    id: "click_10",
    name: "First Ten!",
    desc: "Click the cookie 10 times.",
    icon: "https://res.cloudinary.com/di8fs1bcm/image/upload/v1748161559/first10_aahrke.png",
    type: "clicks",
    value: 10
  },
  {
    id: "click_100",
    name: "Centurion",
    desc: "Click the cookie 100 times.",
    icon: "https://res.cloudinary.com/di8fs1bcm/image/upload/v1748169352/100times_jkmtd2.png",
    type: "clicks",
    value: 100
  },
  {
    id: "auto_1",
    name: "Automation!",
    desc: "Buy your first auto-clicker.",
    icon: "https://res.cloudinary.com/di8fs1bcm/image/upload/v1748169472/automation_tbmgvy.png",
    type: "autoClickers",
    value: 1
  }
  // To add more achievements, just add more objects here.
];

// 2. Track unlocked achievements from server
const unlockedAchievements = ref(new Set());
const hasLoadedServerAchievements = ref(false);

// 3. Fetch unlocked achievements from server
async function fetchUnlockedAchievements() {
  try {
    const { data } = await axios.get('/clicker-achievements');
    const unlockedIds = new Set();
    data.forEach(ach => {
      if (ach.achieved) {
        unlockedIds.add(ach.id);
      }
    });
    unlockedAchievements.value = unlockedIds;
    hasLoadedServerAchievements.value = true;
    console.log('Loaded unlocked achievements:', unlockedIds);
  } catch (error) {
    console.error('Failed to fetch achievements:', error);
    hasLoadedServerAchievements.value = true; // Don't block if server fails
  }
}

// 4. Generic watcher for all achievement types (only after server data is loaded)
watch([score, autoClickers, hasLoadedServerAchievements], ([newScore, newAutoClickers, loaded]) => {
  if (!loaded) return; // Don't check until we've loaded server data
  
  achievements.forEach(ach => {
    if (unlockedAchievements.value.has(ach.id)) return; // Already unlocked
    
    if (
      (ach.type === 'clicks' && newScore >= ach.value) ||
      (ach.type === 'autoClickers' && newAutoClickers >= ach.value)
    ) {
      // Mark as unlocked locally and show popup
      unlockedAchievements.value.add(ach.id);
      showAchievementPopup({
        title: ach.name,
        description: ach.desc,
        image: ach.icon,
        duration: 4000
      });
    }
  });
});

function showSnackbar(message, type = 'success') {
    snackbar.value = {
        show: false,
        message,
        type,
    };
    setTimeout(() => {
        snackbar.value.show = true;
    }, 10);
    function hideSnackBar() {
        snackbar.value.show = false;
    }
}

function incrementScore() {
  score.value += pointsPerClick.value;
  localStorage.setItem('clicker-score', score.value);
}

async function resetScore() {
  await sendBatchClicks();
  score.value = 0;
  
  // Reset all upgrades to initial state
  upgrades.value = upgrades.value.map(u => ({
    ...u,
    amountOwned: 0,
    cost: u.initialCost
  }));

  // Save reset state
  localStorage.setItem('clicker-score', 0);
  upgrades.value.forEach(u => {
    localStorage.setItem(`upgrade-${u.id}-owned`, 0);
    localStorage.setItem(`upgrade-${u.id}-cost`, u.initialCost);
  });

  stopAutoClickers();
  startAutoClickers();
}

async function buyUpgradeCard(upgrade) {
  await sendBatchClicks();
  if (score.value < upgrade.cost) return;

  // Update the upgrade in the array
  upgrades.value = upgrades.value.map(u => {
    if (u.id === upgrade.id) {
      // Subtract cost and update cost
      score.value -= u.cost;
      const nextCost = Math.floor(u.cost * (u.costScale || 1.7));
      return { 
        ...u, 
        cost: nextCost, 
        amountOwned: (u.amountOwned || 0) + 1 
      };
    }
    return u;
  });

  // Save to localStorage
  localStorage.setItem('clicker-score', score.value);
  upgrades.value.forEach(u => {
    localStorage.setItem(`upgrade-${u.id}-owned`, u.amountOwned || 0);
    localStorage.setItem(`upgrade-${u.id}-cost`, u.cost);
  });
}

// Returns the total critical click chance (as a decimal, e.g. 0.15 for 15%)
function getCritChance() {
  const critUpgrade = upgrades.value.find(u => u.id === 'crit_clicks');
  return critUpgrade ? (critUpgrade.amountOwned || 0) * (critUpgrade.effectAmount || 0) : 0;
}

// Returns the total double tap chance (as a decimal, e.g. 0.25 for 25%)
function getDoubleTapChance() {
  const doubleTapUpgrade = upgrades.value.find(u => u.id === 'double_tap');
  return doubleTapUpgrade ? (doubleTapUpgrade.amountOwned || 0) * (doubleTapUpgrade.effectAmount || 0) : 0;
}

async function handleCookieClick() {
  cookiePopping.value = true;
  setTimeout(() => { cookiePopping.value = false; }, 120);
  const x = 80;
  const y = 80 + Math.random() * 20;

  // --- Crit Logic Start ---
  let crit = false;
  let clickPoints = pointsPerClick.value;

  const critChance = getCritChance();
  if (Math.random() < critChance) {
    clickPoints *= 2; // Double points on crit
    crit = true;
  }

  // --- Double Tap Logic Start ---
  let doubleTap = false;
  const doubleTapChance = getDoubleTapChance();
  if (Math.random() < doubleTapChance) {
    clickPoints += pointsPerClick.value; // Add another click worth of points
    doubleTap = true;
  }

  floaters.value.push({
    id: floaterId++,
    value: crit ? `CRIT! +${clickPoints}` : doubleTap ? `DOUBLE! +${clickPoints}` : clickPoints,
    x,
    y
  });
  setTimeout(() => {
    floaters.value.shift();
  }, 900);

  score.value += clickPoints;
  pendingClicks += clickPoints;
  localStorage.setItem('clicker-score', score.value);
  // --- Crit & Double Tap Logic End ---
  
  if(!batchTimer) {
    batchTimer = setTimeout(sendBatchClicks, BATCH_INTERVAL);
  }
}

async function sendBatchClicks() {
  if (pendingClicks >0) {
    try {
        await axios.post('/clicker/update', {
    clicks: score.value,
    autoClickers: autoClickers.value,
    perClick: pointsPerClick.value,
    delta: pendingClicks,
  });
    }catch (e) {
      console.error('Failed to send Batch clicks', e);
    }
    pendingClicks = 0;
  }
  batchTimer = null;
}

function startAutoClickers() {
  if (autoClickerInterval) clearInterval(autoClickerInterval);
  if (autoClickers.value > 0) {
    autoClickerInterval = setInterval(() => {
      for (let i = 0; i < autoClickers.value; i++) {
        handleAutoClicker();
      }
    }, 1000);
  }
}

function stopAutoClickers() {
  if (autoClickerInterval) clearInterval(autoClickerInterval);
}

function handleAutoClicker() {
  if (autoClickers.value === 0) return;
  const handIndex = Math.floor(Math.random() * autoClickers.value);
  activeAutoClickers.value.push(handIndex);

  setTimeout(() => {
    const idx = activeAutoClickers.value.indexOf(handIndex);
    if (idx !== -1) activeAutoClickers.value.splice(idx, 1);
  }, 350);

  const x = 80 + (Math.random() - 0.5) * 40;
  const y = 80 + Math.random() * 40;
  floaters.value.push({
    id: floaterId++,
    value: pointsPerClick.value,
    x,
    y
  });
  setTimeout(() => {
    floaters.value.shift();
  }, 900);
  incrementScore();
}

function autoClickerStyle(n, total, isTapping = false) {
  const angle = ((n - 1) / total) * 2 * Math.PI - Math.PI / 2 + orbitAngle.value;
  const cookieRadius = 150;
  const cookieCenterX = 150;
  const cookieCenterY = 150;
  const handWidth = 40;
  const handHeight = 40;
  const handTipOffsetY = handHeight;
  const radius = cookieRadius - 4;
  

  const x = cookieCenterX + Math.cos(angle) * radius - handWidth / 2;
  const y = cookieCenterY + Math.sin(angle) * radius - handTipOffsetY;

  const rotationDegrees = (angle * 180 / Math.PI) + 270;

  // Compose transforms
  let transform = `rotate(${rotationDegrees}deg)`;
  if (isTapping) {
    transform += " scale(0.85) translateY(12px)";
  }

  return {
    position: 'absolute',
    left: `${x}px`,
    top: `${y}px`,
    transform,
    transformOrigin: '50% 80%',
    transition: 'transform 0.2s',
    zIndex: 2
  };
}





function calculateFittePoints(clickerPoints) {
  let remaining = clickerPoints;
  let fitte = 0;
  let used = 0;
  const tier1 = Math.min(remaining, 10000);
  fitte += Math.floor(tier1 / 100);
  used += Math.floor(tier1 / 100) * 100; // change back to 1000
  remaining -= tier1;
  if (remaining > 0) {
    const tier2 = Math.min(remaining, 40000);
    fitte += Math.floor(tier2 / 2000);
    used += Math.floor(tier2 / 2000) * 2000;
    remaining -= tier2;
  }
  if (remaining > 0) {
    fitte += Math.floor(remaining / 5000);
    used += Math.floor(remaining / 5000) * 5000;
    remaining = remaining % 5000;
  }
  return {
    fittePoints: fitte,
    pointsUsed: used,
    pointsLeft: clickerPoints - used
  };
}

// Returns { amountOwned, max } for any upgrade
function getUpgradeProgress(upgrade) {
  // If the upgrade unlocks after another upgrade, use that one for progress
  if (upgrade.unlocksAfter) {
    const dep = upgrades.value.find(u => u.id === upgrade.unlocksAfter.id);
    return {
      amountOwned: dep?.amountOwned || 0,
      max: upgrade.unlocksAfter.count || 1
    };
  }
  // Otherwise, default to own amountOwned/max
  return {
    amountOwned: upgrade.amountOwned || 0,
    max: upgrade.max || 1
  };
}


function getUpgradeBarWidth(upgrade) {
  const { amountOwned, max } = getUpgradeProgress(upgrade);
  // Clamp between 0 and 100
  let percent = Math.max(0, Math.min(100, (amountOwned / max) * 100));
  return percent + '%';
}

const conversionResult = computed(() => calculateFittePoints(score.value));

async function fetchFittePoints() {
  isLoadingFittePoints.value = true;
  try {
    const token = computed(() => auth.token);
    console.log('Token used for Fitte Points:', token);
    if (!token) {
      console.warn('No token found for Fitte Points fetch');
      return;
    }
    const res = await axios.get('get-fitte-points', {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.data && res.data.points !== undefined) {
      fittePoints.value = res.data.points;
      console.log('Fetched Fitte Points:', res.data, 'Set fittePoints:', fittePoints.value);
    } else {
      console.log('No points in response:', res.data);
    }
  } catch (e) {
    console.error('Error fetching Fitte Points:', e);
  } finally {
    isLoadingFittePoints.value = false;
  }
}

async function updateFittePoints(newPoints, isDailyReward = false) {
  if (!token) return;
  await axios.post('update-fitte-points', {
    points: newPoints,
    is_daily_reward: isDailyReward
  }, {
    headers: { Authorization: `Bearer ${token.value}` }
  });
}

async function convertToFittePoints() {
  await sendBatchClicks();
  const { fittePoints: fp, pointsUsed } = conversionResult.value;
  if (fp > 0) {
    const newFittePoints = fittePoints.value + fp;
    await updateFittePoints(newFittePoints);
    score.value -= pointsUsed;
    localStorage.setItem('clicker-score', score.value);
    await fetchFittePoints();
    showSnackbar(`Converted ${pointsUsed} points for ${fp} Fitte Points!`, 'success');
  }
}

function showAchievementPopup(achievement) {
  popupTitle.value = achievement.title;
  popupDescription.value = achievement.description;
  popupImage.value = achievement.image;
  achievementPopup.value?.show();
}

function canUnlock(upgrade) {
  if (!upgrade.unlocksAfter) return true;
  if (upgrade.unlocksAfter.id === 'click') {
    const clickUpgrade = upgrades.value.find(u => u.id === 'click');
    return (clickUpgrade?.amountOwned || 0) >= upgrade.unlocksAfter.count;
  }
  return true;
}

onMounted(() => {
  // Load saved score
  const saved = localStorage.getItem('clicker-score');
  if (saved) score.value = parseInt(saved, 10);

  // Load saved upgrades
  upgrades.value = upgrades.value.map(u => {
    const owned = localStorage.getItem(`upgrade-${u.id}-owned`);
    const cost = localStorage.getItem(`upgrade-${u.id}-cost`);
    return {
      ...u,
      amountOwned: owned ? parseInt(owned, 10) : 0,
      cost: cost ? parseInt(cost, 10) : u.initialCost
    };
  });

  startAutoClickers();
  console.log('Pinia user in ClickerGame:', user.value);
  fetchFittePoints();
  fetchUnlockedAchievements(); // Load server achievements
  window.addEventListener('beforeunload', sendBatchClicks);

  let last = performance.now();
  function animateOrbit(now) {
    const delta = now - last;
    orbitAngle.value += 0.0001 * delta; // speed
    last = now;
    requestAnimationFrame(animateOrbit);
  }
  requestAnimationFrame(animateOrbit);
});

onUnmounted(() => {
  window.removeEventListener('beforeunload', sendBatchClicks);
});
</script>

<style scoped>
/* ==== MAIN LAYOUT ==== */
.gamified-bg {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: var(--bg-color);
  font-family: 'Segoe UI', 'Arial', sans-serif;
  padding: 0;
  box-sizing: border-box;
  position: relative;
  overflow-x: hidden;
}

.game-header {
  margin: 2.5rem 0 1.5rem 0;
  text-align: center;
  z-index: 1;
}

.game-header h2 {
  font-size: 2.6rem;
  color: var(--text-color);
  font-weight: bold;
  letter-spacing: 3px;
  text-shadow: 0 3px 12px var(--card-bg), 0 1px 0 var(--text-color);
  margin-bottom: 0.6rem;
}

.score-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  background: var(--card-bg);
  border-radius: 1rem;
  box-shadow: 0 2px 10px var(--border-color);
  border: 1.5px solid var(--border-color);
  padding: 0.8rem 2.4rem;
  font-size: 1.22rem;
  color: var(--text-color);
}

.score-label { font-weight: 700; color: var(--text-color); }
.score-value { font-size: 1.7rem; color: var(--primary); font-weight: bold; }
.score-pps, .score-auto { color: var(--text-color); font-size: 1.12rem; }

.xp-bar {
  height: 7px;
  background: #cde3fa;
  border-radius: 7px;
  width: 100%;
  overflow: hidden;
  box-shadow: 0 1px 3px #9ed7fd44;
  margin-top: 4px;
}
.xp-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #52dbfc 40%, #389aff 100%);
  border-radius: 7px;
  transition: width 0.5s cubic-bezier(.54,.08,.57,.97);
  box-shadow: 0 1px 3px #fff9;
}
/* ==== THREE COLUMN GAME LAYOUT ==== */
.game-flex {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 0;
  width: 100%;
  max-width: 1520px;
  margin: 0 auto;
  min-height: 670px;
  position: relative;
}

/* ==== LEFT: COOKIE COLUMN ==== */
.cookie-area {
  flex: 1 1 430px;
  min-width: 350px;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 3px solid var(--border-color);
  position: relative;
  padding: 0 2.2rem 0 0;
}

.score-display {
  margin-bottom: 1.3rem;
  text-align: center;
}

.main-score {
  font-size: 2.7rem;
  color: var(--text-color);
  font-weight: bold;
  text-shadow: 0 3px 12px var(--card-bg), 0 1px 0 var(--text-color);
  margin-bottom: 0.2rem;
}

.per-click, .per-auto {
  color: var(--text-color);
  font-size: 1.13rem;
  line-height: 1.1;
  margin-bottom: 0.08rem;
}

.cookie-spotlight {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 0 2rem 0;
  padding: 2rem;
  border-radius: 50%;
}
.leaderboard-btn {
  background: #2679b8;
  color: #fff;
  border: none;
  border-radius: 0.7rem;
  padding: 0.4em 1.2em;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.8em;
  margin-left: 1em;
  cursor: pointer;
  box-shadow: 0 2px 8px #2679b820;
  transition: background 0.18s;
}

.leaderboard-btn:hover {
  background: #15507c;
}
.store-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cookie-wrapper.larger-cookie {
  width: 300px;
  height: 300px;
  position: relative;
  z-index: 2;
}
.upgrade-icon-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  display: inline-block;
  vertical-align: middle;
}
.cookie-svg {
  width: 300px;
  height: 300px;
  cursor: pointer;
  transition: transform 0.15s;
}
.cookie-svg:hover {
  transform: scale(1.07) rotate(-1deg);
}

.reset-btn {
  background: #2679b8;
  color: #fff;
  font-size: 1.01rem;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 0.6rem;
  margin: 0.7rem 0 0 0;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px #b3d0ea;
}
.reset-btn:hover { background: #235c88; }

.badge-floaters {
  position: absolute;
  left: 0; top: 0;
  width: 160px; height: 160px;
  pointer-events: none;
}
.floater {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  color: #ffb300;
  font-size: 1.35rem;
  font-weight: bold;
  text-shadow: 0 2px 8px #fffbe7, 0 1px 0 #fff;
  opacity: 1;
  animation: floatUp 0.9s cubic-bezier(.4,1.6,.6,1) forwards;
}
@keyframes floatUp {
  0% { opacity: 1; top: 60px; }
  80% { opacity: 1; }
  100% { opacity: 0; top: 10px; }
}

/* ==== CENTER: CONVERT PANEL ==== */
.convert-center {
  flex: 1 1 410px;
  min-width: 340px;
  max-width: 470px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0 2.2rem;
}

.auto-clicker-icon-img {
  width: 40px;
  height: 40px;
  pointer-events: none;
  user-select: none;
  /* Optional: Remove drag effect */
  -webkit-user-drag: none;
}
.floater.crit {
  color: #FFD700;
  font-size: 1.65rem;
  text-shadow:
    0 2px 18px #fffbce,
    0 1px 0 #ffd700,
    0 0 10px #ffd700;
  font-weight: 900;
  animation: critFloatUp 0.9s cubic-bezier(.4,1.6,.6,1) forwards;
  transform: scale(1.18) rotate(-5deg);
}

@keyframes critFloatUp {
  0%   { opacity: 1; top: 60px; transform: scale(1.3) rotate(-5deg);}
  70%  { opacity: 1; }
  90%  { filter: brightness(2);}
  100% { opacity: 0; top: 10px; transform: scale(1) rotate(0deg);}
}


.convert-card {
  background: var(--card-bg);
  border-radius: 1.5rem;
  box-shadow: 0 4px 36px 0 var(--border-color), 0 0 0 4px var(--border-color);
  border: 2.5px solid var(--primary);
  margin: 2.5rem 0 0 0;
  width: 100%;
  max-width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1.4rem 1.6rem 1.4rem;
  animation: popConvertCard 0.7s cubic-bezier(.4,1.6,.6,1);
  z-index: 1;
}
@keyframes popConvertCard {
  0% { transform: scale(0.97); opacity: 0.7; }
  80% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
.convert-title {
  color: var(--text-color);
  font-size: 1.18rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}
.convert-guide {
  color: var(--text-color);
  font-size: 0.98rem;
  text-align: center;
  margin-bottom: 0.2rem;
}
.convert-tier {
  color: var(--primary);
  font-weight: 600;
}
.convert-summary {
  color: var(--text-color);
  font-size: 1.05rem;
  text-align: center;
  margin-bottom: 0.2rem;
}
.convert-btn {
  background: linear-gradient(90deg, #ffd700 65%, #ffb300 100%);
  color: #235c88;
  font-weight: bold;
  font-size: 1.07rem;
  padding: 0.7rem 2.2rem;
  border: none;
  border-radius: 0.7rem;
  cursor: pointer;
  box-shadow: 0 2px 8px #ffd70080;
  transition: background 0.18s, filter 0.2s;
  margin-top: 0.7rem;
  text-shadow: 0 2px 6px #fffbe7bb;
}
.convert-btn:disabled {
  background: #eee;
  color: #aaa;
  cursor: not-allowed;
  filter: grayscale(0.6);
}
.convert-btn:not(:disabled):hover {
  filter: brightness(1.08) drop-shadow(0 0 8px #ffd700);
}
.fitte-balance-badge {
  background: linear-gradient(90deg, #e3f0fa 60%, #b3d0ea 100%);
  border-radius: 1.2rem;
  box-shadow: 0 2px 8px 0 #b3d0ea;
  border: 1.5px solid #b3d0ea;
  padding: 0.7rem 1.2rem;
  margin-bottom: 0.7rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 1.1rem;
  color: #235c88;
  font-weight: 600;
}
.fitte-balance-label { color: #2679b8; font-weight: 700; margin-right: 0.3rem; }
.fitte-balance-value {
  color: #007bff;
  font-size: 1.3rem;
  font-weight: bold;
  text-shadow: 0 2px 8px #b3d0ea, 0 1px 0 #fff;
}

/* ==== RIGHT: SHOP PANEL ==== */
.shop-panel {
  max-width: 440px;
  min-width: 320px;
  width: 100%;
  padding: 1.2rem 0.6rem;
  border-left: 2px solid var(--border-color);
  background: var(--card-bg);
  box-shadow: 0 4px 24px 0 #b3d0ea55;
  border-radius: 1.2rem;
  align-items: flex-start;
  margin-top: 1.2rem;
  min-height: 700px;
}

.store-header-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  width: 100%;
  margin-bottom: 0.7rem;
}

.store-header {
  font-size: 2.1rem;
  font-weight: bold;
  color: #2679b8;
  text-align: center;
  letter-spacing: 2px;
  text-shadow:
    0 2px 12px #e3f0fa80,
    0 0px 2px #fff,
    0 1px 0 #2679b877;
  background:
    url('https://res.cloudinary.com/di8fs1bcm/image/upload/v1748206293/storeheaderbg_axwros.png') center/cover no-repeat,
    linear-gradient(90deg, #e3f0fa 60%, #b3d0ea 100%);
  border-radius: 1.2rem;
  box-shadow: 0 2px 16px 0 #b3d0ea55;
  padding: 0.7rem 1.2rem;
  width: 60%;
  max-width: 260px;
  margin: 0;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.leaderboard-btn {
  background: #2679b8;
  color: #fff;
  border: none;
  border-radius: 0.7rem;
  padding: 0.4em 1.2em;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px #2679b820;
  transition: background 0.18s;
  margin: 0;
}

.leaderboard-btn:hover {
  background: #15507c;
}

.scrollable-store {
  height: calc(100% - 110px); /* Adjust for header and padding */
  max-height: none;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
  margin-top: 0.5rem;
}

.sidebar-upgrade-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
}

.sidebar-upgrade-card {
  display: flex;
  flex-direction: column;
  background:
    url('https://res.cloudinary.com/di8fs1bcm/image/upload/v1748206296/cardbp_wpab2t.png') center/100% 100% no-repeat,
    linear-gradient(90deg, #e3f0fa88 60%, #b3d0ea88 100%);
  border-radius: 0.8rem;
  border: 1.5px solid var(--border-color);
  box-shadow: 0 2px 12px #b3d0ea33;
  padding: 1.2rem 1.8rem 1.2rem 1.8rem;
  min-height: 100px;
  max-width: 100%;
  width: 100%;
  font-size: 1.07rem;
  position: relative;
  box-sizing: border-box;
  transition: box-shadow 0.18s, transform 0.15s;
  margin-bottom: 0.8rem;
}
.sidebar-upgrade-card:hover {
  box-shadow: 0 4px 24px #2679b8aa, 0 1px 6px #b3d0ea33;
  transform: translateY(-2px) scale(1.025);
  z-index: 2;
}
.sidebar-upgrade-card.disabled {
  opacity: 0.6;
  filter: grayscale(0.6);
}

.sidebar-upgrade-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.7rem;
  width: 100%;
  min-height: 38px;
}

.sidebar-upgrade-icon {
  font-size: 1.4rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.3rem;
}

.sidebar-upgrade-name {
  font-weight: 700;
  font-size: 1.08rem;
  color: var(--text-color);
  margin-right: 0.3rem;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.sidebar-upgrade-qty {
  font-size: 1rem;
  color: #888;
  margin-left: 0.1rem;
}

.sidebar-upgrade-cost {
  color: var(--primary);
  font-size: 1.05rem;
  margin-left: auto;
  margin-right: 0.4rem;
  white-space: nowrap;
}

.sidebar-upgrade-buy-btn {
  font-size: 1rem;
  padding: 0.2rem 0.9rem;
  border-radius: 0.5rem;
  background: linear-gradient(90deg, #b3d0ea 60%, #2679b8 100%);
  color: #fff;
  font-weight: 600;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(35, 92, 136, 0.08);
  transition: background 0.18s, filter 0.15s;
  margin-left: 0.2rem;
}
.sidebar-upgrade-buy-btn:disabled {
  background: #eee;
  color: #aaa;
  cursor: not-allowed;
  filter: grayscale(0.6);
}
.sidebar-upgrade-buy-btn:not(:disabled):hover {
  filter: brightness(1.12) drop-shadow(0 0 8px #2679b8);
}
.sidebar-upgrade-desc {
  color: #aaa;
  font-size: 0.95rem;
  margin: 0.1rem 0 0.1rem 2.1rem;
  line-height: 1.2;
}
.sidebar-upgrade-locked-msg {
  color: #b88;
  font-size: 0.9rem;
  margin-left: 2.1rem;
  margin-top: 0.1rem;
}


/* ==== RESPONSIVE ==== */
@media (max-width: 1200px) {
  .game-flex {
    flex-direction: column;
    min-height: unset;
  }
  .cookie-area, .convert-center, .shop-panel {
    border: none !important;
    min-width: 0;
    max-width: 100vw;
    padding: 0 !important;
    margin: 0 auto 2rem auto;
  }
  .upgrade-shop, .convert-card {
    margin-top: 0;
  }
}
.shop-panel {
  max-height: 300px;

}
@media (max-width: 700px) {
  .game-header h2 { font-size: 2rem; }
  .score-bar { flex-direction: column; gap: 0.7rem; padding: 0.7rem 1.1rem; }
  .game-flex { flex-direction: column; padding: 0 0.4rem; }
  .cookie-area, .convert-center, .shop-panel { max-width: 98vw; }
  .cookie-spotlight, .cookie-wrapper.larger-cookie, .cookie-svg { width: 180px !important; height: 180px !important; }
  .convert-card, .upgrade-shop { padding: 1.1rem 0.6rem 0.9rem 0.6rem; }
  .shop-title { font-size: 1.05rem; }
}

@keyframes autoClickerAnim {
  0% { transform: rotate(var(--rotation)) scale(1); }
  50% { transform: rotate(var(--rotation)) scale(0.9); }
  100% { transform: rotate(var(--rotation)) scale(1); }
}



.auto-clicker-hand {
  width: 40px;
  height: 40px;
}

.auto-clicker-visual.tap {
  transform: rotate(var(--rotation)) scale(0.8) translateY(16px);
  filter: brightness(1.4) drop-shadow(0 0 12px #FFD700);
  z-index: 4;
}
.store-header {
  font-size: 2rem;
  font-weight: bold;
  color: #2679b8;
  text-align: center;
  margin: 1rem 0 0.4rem 0;
  letter-spacing: 2px;
  text-shadow:
    0 2px 12px #e3f0fa80,
    0 0px 2px #fff,
    0 1px 0 #2679b877;
background:
  url('https://res.cloudinary.com/di8fs1bcm/image/upload/v1748206293/storeheaderbg_axwros.png') center/cover no-repeat,
  linear-gradient(90deg, #e3f0fa 60%, #b3d0ea 100%);
  border-radius: 1.2rem;
  box-shadow: 0 2px 16px 0 #b3d0ea55;
  padding: 0.7rem 1.2rem;
  width: 96%;
  max-width: 330px;
  margin-left: auto;
  margin-right: auto;
  user-select: none;
  position: relative;
  overflow: hidden;
}

.scrollable-store {
  max-height: 500px;     /* Or whatever fits your design */
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
  margin-top: 0.5rem;
}

</style>

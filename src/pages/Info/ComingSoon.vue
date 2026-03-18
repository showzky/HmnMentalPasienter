<template>
  <div class="coming-soon-bg">
    <div class="coming-soon-container">
      <div class="glow-circle"></div>
      <div class="glow-circle2"></div>
      <h1 class="coming-soon-title">
        <span class="icon">🚧</span>
        <span>Coming Soon!</span>
        <span class="icon">🚧</span>
      </h1>
      <p class="coming-soon-text">
        This feature is not ready yet.<br>
        <span class="wait-text">Check back soon for something awesome!</span>
      </p>
      <div class="release-date">Release Date Beta: <b>TBA</b></div>
      <div class="loader">
        <span></span><span></span><span></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.coming-soon-bg {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #24243e 0%, #302b63 54%, #0f2027 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}
.coming-soon-container {
  position: relative;
  background: rgba(255,255,255,0.11);
  box-shadow: 0 8px 40px #00d2ff33, 0 2px 24px #fff9;
  border-radius: 2.5rem;
  padding: 3.5rem 2.7rem 2.6rem 2.7rem;
  text-align: center;
  z-index: 2;
  backdrop-filter: blur(13px) saturate(1.2);
  border: 2.5px solid #ffffff25;
  animation: pop-in 1.2s cubic-bezier(.6,1.6,.3,1) 1;
}
@keyframes pop-in {
  0% { transform: scale(0.88) translateY(80px); opacity: 0; }
  70% { transform: scale(1.04) translateY(-6px); opacity: 1; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}
.coming-soon-title {
  font-size: 2.8rem;
  letter-spacing: 1.8px;
  color: #fff;
  text-shadow: 0 2px 16px #00d2ff80, 0 1px 0 #fff;
  font-weight: 800;
  margin-bottom: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.3rem;
  animation: shine-title 2.5s infinite linear;
}
@keyframes shine-title {
  0% { text-shadow: 0 2px 16px #00d2ff90, 0 1px 0 #fff; }
  60% { text-shadow: 0 2px 32px #fff7, 0 1px 0 #fff; }
  100% { text-shadow: 0 2px 16px #00d2ff90, 0 1px 0 #fff; }
}
.coming-soon-title .icon {
  filter: drop-shadow(0 0 8px #fdc400cc);
  font-size: 2.2rem;
  animation: bounce 1.6s infinite cubic-bezier(.65,.02,.6,1.03);
}
@keyframes bounce {
  0%, 100% { transform: translateY(0);}
  30% { transform: translateY(-13px);}
  70% { transform: translateY(2px);}
}
.coming-soon-text {
  font-size: 1.32rem;
  color: #fff;
  margin-bottom: 1.8rem;
  font-weight: 400;
  letter-spacing: 1px;
  text-shadow: 0 1px 9px #fff8;
  line-height: 1.5;
}
.wait-text {
  color: #00f7ff;
  font-weight: 700;
  text-shadow: 0 1px 14px #00fff7cc;
  letter-spacing: 1.6px;
  font-size: 1.12em;
}

.loader {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
.loader span {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fdc400 50%, #00d2ff 100%);
  box-shadow: 0 2px 16px #00d2ff88;
  animation: bounce-dot 1.3s infinite alternate;
  opacity: 0.9;
}
.loader span:nth-child(2) { animation-delay: .25s; }
.loader span:nth-child(3) { animation-delay: .5s; }
@keyframes bounce-dot {
  to { transform: translateY(-17px); }
}

/* Glowing circles for background effect */
.glow-circle, .glow-circle2 {
  position: absolute;
  border-radius: 50%;
  z-index: 1;
  opacity: 0.42;
  pointer-events: none;
}
.glow-circle {
  width: 290px; height: 290px;
  left: -110px; top: -85px;
  background: radial-gradient(circle, #00f7ffcc 0%, #1b2736 90%);
  filter: blur(13px);
  animation: floatA 11s infinite alternate;
}
.glow-circle2 {
  width: 230px; height: 230px;
  right: -90px; bottom: -60px;
  background: radial-gradient(circle, #fdc400bb 0%, #1b2736 90%);
  filter: blur(11px);
  animation: floatB 13s infinite alternate;
}
@keyframes floatA {
  0% { transform: scale(1) translateY(0);}
  100% { transform: scale(1.09) translateY(23px);}
}
@keyframes floatB {
  0% { transform: scale(1) translateY(0);}
  100% { transform: scale(1.14) translateY(-27px);}
}

.release-date {
  color: #fdc400;
  font-size: 1.18rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  text-shadow: 0 1px 8px #fff5, 0 0px 8px #fdc40055;
}
</style>

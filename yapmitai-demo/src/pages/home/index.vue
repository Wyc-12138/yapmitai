<template>
  <div class="os-landing">
    <nav>
      <button type="button" class="nav-logo" @click="goHome">YAPMIT<span>AI</span></button>
      <ul class="nav-center">
        <li><button type="button" :class="{ active: activePage === 'home' }" @click="goHome">平台</button></li>
        <li v-for="portal in portals" :key="portal.key">
          <button type="button" class="nav-portal" @click="enterPortal(portal.path)">{{ portal.label }}</button>
        </li>
      </ul>
      <div class="nav-right">
        <button type="button" class="nav-ask" @click="askMeOpen = true">
          <span class="nav-ask-dot"></span>
          Ask Me
        </button>
        <button type="button" class="nav-login" @click="enterPortal('/enterprise/dashboard')">登录系统</button>
      </div>
    </nav>

    <div v-if="activePage === 'home'" class="page">
      <section class="hero">
        <div class="hero-grid"></div>
        <div class="hero-orb"></div>
        <div class="hero-badge"><span class="badge-dot"></span>AI Operating System · yapmitai.com</div>
        <h1>行业智能<br>从 <em>底座</em> 开始</h1>
        <p class="hero-sub">YAPMIT AI OS 将大模型能力封装为垂直行业标准化工作流——品牌增长、跨境出海、导购文旅、招商引资，一套底座，四个行业空间。</p>
        <div class="hero-actions">
          <button type="button" class="btn-primary" @click="scrollToIndustry">探索行业空间</button>
          <button type="button" class="btn-ask" @click="askMeOpen = true">
            <span style="font-size: 16px">💬</span> Ask Me AI
          </button>
          <button type="button" class="btn-ghost" @click="enterPortal('/enterprise/dashboard')">登录系统</button>
        </div>
      </section>

      <div class="login-portal">
        <div class="login-portal-inner">
          <span class="portal-label">登录入口</span>
          <div class="portal-divider"></div>
          <div class="portal-cards">
            <button
              v-for="portal in portals"
              :key="portal.key"
              type="button"
              class="portal-card"
              @click="enterPortal(portal.path)"
            >
              <div class="portal-icon">{{ portal.emoji }}</div>
              <div class="portal-info">
                <div class="portal-name">{{ portal.label }}</div>
                <div class="portal-hint">{{ portal.desc }}</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div class="askme-banner-wrap">
        <div class="askme-banner" @click="askMeOpen = true">
          <div class="askme-left">
            <div class="askme-icon">💬</div>
            <div>
              <div class="askme-title">Ask Me — AI 智能问答</div>
              <div class="askme-desc">基于 YAPMIT 自建知识库、产品库、行业数据库，像 Perplexity 一样直接问，立刻得到行业专属答案。</div>
            </div>
          </div>
          <button type="button" class="askme-action" @click.stop="askMeOpen = true">立即体验 →</button>
        </div>
      </div>

      <div class="stats-bar">
        <div v-for="item in stats" :key="item.label" class="stat">
          <div class="stat-number">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </div>
      </div>

      <div class="section">
        <div class="section-eyebrow">系统架构</div>
        <div class="section-title">一个 OS，驱动四个行业</div>
        <div class="section-desc">从底层算力到顶层行业应用，YAPMIT AI OS 提供完整垂直栈——每一层独立可调用，也可协同运作。</div>
        <div class="os-stack">
          <template v-for="(layer, index) in osStackLayers" :key="layer.name">
            <div v-if="index > 0" class="stack-connector"></div>
            <div class="stack-layer">
              <div class="stack-icon" :style="{ background: layer.bg }">{{ layer.icon }}</div>
              <div class="stack-info">
                <div class="stack-name">{{ layer.name }}</div>
                <div class="stack-desc">{{ layer.desc }}</div>
              </div>
              <div class="stack-tag">{{ layer.tag }}</div>
            </div>
          </template>
        </div>
      </div>

      <div id="industry-section" class="section" style="padding-top: 0">
        <div class="section-eyebrow">行业空间</div>
        <div class="section-title">选择你的行业</div>
        <div class="section-desc">每个 Industry Space 内置专属 Agent Team、Skill 库和工作流模板，开箱即用。</div>
        <div class="industry-grid">
          <button
            v-for="card in industryCards"
            :key="card.slug"
            type="button"
            class="industry-card"
            :class="card.cardClass"
            @click="showIndustry(card.slug)"
          >
            <div class="card-icon-wrap">{{ card.icon }}</div>
            <div class="card-title">{{ card.title }} <span class="card-tag">{{ card.tag }}</span></div>
            <div class="card-subtitle">{{ card.subtitle }}</div>
            <div class="card-desc">{{ card.desc }}</div>
            <div class="card-features">
              <div v-for="feature in card.features" :key="feature" class="card-feature">{{ feature }}</div>
            </div>
            <div class="card-cta">
              深入了解
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M2 7h10M7 2l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
          </button>
        </div>
      </div>

      <footer>
        <div class="footer-logo">YAPMIT<span>AI</span></div>
        <div class="footer-links">
          <button type="button" class="footer-link">关于我们</button>
          <button type="button" class="footer-link">文档</button>
          <button type="button" class="footer-link" @click="askMeOpen = true">Ask Me</button>
          <button type="button" class="footer-link">联系我们</button>
        </div>
        <div class="footer-copy">© 2025 YAPMITAI Inc. · AI makes you better · yapmitai.com</div>
      </footer>
    </div>

    <IndustryPage
      v-else-if="currentIndustry"
      :data="currentIndustry"
      @back="goHome"
      @ask-me="askMeOpen = true"
    />

    <AskMeModal v-model:open="askMeOpen" />
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import AskMeModal from "./AskMeModal.vue";
import IndustryPage from "./IndustryPage.vue";
import { industries, industryCards, osStackLayers, stats } from "./industry-data.js";
import { portals } from "./portals.js";
import "./os-landing.css";

const router = useRouter();
const activePage = ref("home");
const askMeOpen = ref(false);

const currentIndustry = computed(() => industries[activePage.value] || null);

function enterPortal(path) {
  router.push(path);
}

function goHome() {
  activePage.value = "home";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showIndustry(slug) {
  activePage.value = slug;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToIndustry() {
  document.getElementById("industry-section")?.scrollIntoView({ behavior: "smooth" });
}
</script>

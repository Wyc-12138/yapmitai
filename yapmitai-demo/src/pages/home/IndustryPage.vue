<template>
  <div class="os-industry-page" :style="{ '--ind-color': data.color }">
    <div class="industry-hero">
      <button type="button" class="back-btn" @click="$emit('back')">← 返回主页</button>
      <div class="industry-hero-tag" :style="{ background: data.tagBg, color: data.color, border: `1px solid ${data.tagBorder}` }">{{ data.tag }}</div>
      <div class="industry-hero-en">{{ data.en }}</div>
      <h1 v-html="data.title"></h1>
      <p>{{ data.subtitle }}</p>
      <div class="hero-actions">
        <button type="button" class="btn-primary" :style="primaryStyle">{{ data.primaryLabel }}</button>
        <button type="button" class="btn-ask" @click="$emit('ask-me')"><span>💬</span> Ask Me</button>
        <button type="button" class="btn-ghost">{{ ghostLabel }}</button>
      </div>
    </div>

    <div class="kpi-row">
      <div class="kpi-inner">
        <div v-for="kpi in data.kpis" :key="kpi.label" class="kpi">
          <div class="kpi-num" :style="{ color: data.color }" v-html="kpi.value"></div>
          <div class="kpi-label" v-html="kpi.label"></div>
        </div>
      </div>
    </div>

    <div class="use-cases">
      <div class="section-eyebrow">核心场景</div>
      <div class="section-title">6 个{{ data.tag }} AI 场景</div>
      <div class="use-case-grid">
        <div v-for="item in data.useCases" :key="item.title" class="use-case-card">
          <div class="uc-icon">{{ item.icon }}</div>
          <div class="uc-title">{{ item.title }}</div>
          <div class="uc-desc">{{ item.desc }}</div>
        </div>
      </div>
    </div>

    <div class="workflow-section">
      <div class="section-eyebrow">工作流</div>
      <div class="section-title">{{ data.workflowTitle }}</div>
      <div class="workflow-steps">
        <div v-for="(step, index) in data.steps" :key="step.title" class="workflow-step">
          <div class="step-num">{{ String(index + 1).padStart(2, "0") }}</div>
          <div class="step-content">
            <div class="step-title">{{ step.title }}</div>
            <div class="step-desc">{{ step.desc }}</div>
            <div class="step-tools">
              <span v-for="tool in step.tools" :key="tool" class="tool-chip">{{ tool }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="cta-block">
      <h2>{{ data.ctaTitle }}</h2>
      <p>{{ data.ctaDesc }}</p>
      <button type="button" class="btn-primary" :style="ctaStyle">{{ data.ctaLabel }}</button>
    </div>

    <footer>
      <div class="footer-logo">YAPMIT<span>AI</span></div>
      <div class="footer-links"><button type="button" class="footer-link" @click="$emit('back')">返回主页</button></div>
      <div class="footer-copy">© 2025 YAPMITAI Inc. · AI makes you better</div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  data: { type: Object, required: true }
});

defineEmits(["back", "ask-me"]);

const ghostLabels = {
  brand: "查看案例",
  cross: "了解方案",
  commerce: "合作咨询",
  invest: "政府合作咨询"
};

const ghostLabel = computed(() => ghostLabels[props.data.slug] || "了解更多");

const primaryStyle = computed(() => ({
  background: props.data.color,
  boxShadow: `0 0 30px color-mix(in srgb, ${props.data.color} 30%, transparent)`,
  color: props.data.primaryDarkText ? "#000" : "white"
}));

const ctaStyle = computed(() => ({
  background: props.data.color,
  boxShadow: `0 0 30px color-mix(in srgb, ${props.data.color} 30%, transparent)`,
  color: props.data.ctaDarkText ? "#000" : "white"
}));
</script>

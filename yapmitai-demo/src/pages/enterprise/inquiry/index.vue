<template>
  <section class="inquiry-page">
    <PageHeader
      eyebrow="Songnan International Trade"
      title="询盘转化 AI 系统"
      description="三大 Agent 串联处理询盘：意图识别 → 智能回复 → 跟进策略。"
    />

    <div class="inquiry-toolbar">
      <button class="ghost-btn" @click="router.push('/enterprise/inquiry/history')">查看历史询盘</button>
    </div>

    <div class="inquiry-input-card">
      <label>输入客户询盘内容</label>
      <textarea
        v-model="inquiryText"
        placeholder="请输入或粘贴客户询盘内容..."
        @input="onInquiryInput"
      ></textarea>

      <div class="inquiry-source-row">
        <span>来源：</span>
        <button
          v-for="item in sourceOptions"
          :key="item"
          type="button"
          :class="{ active: source === item }"
          @click="source = item"
        >
          {{ item }}
        </button>
      </div>

      <div class="inquiry-sample-row">
        <span>样例：</span>
        <button
          v-for="sample in inquirySamples"
          :key="sample.label"
          type="button"
          :class="{ active: activeSampleLabel === sample.label }"
          @click="applySample(sample)"
        >
          {{ sample.label }}
        </button>
      </div>

      <div class="inquiry-toolbar">
        <button class="primary-btn" :disabled="loading" @click="analyze">
          {{ loading ? "三大 Agent 分析中…" : "启动三大 AI 智能体分析" }}
        </button>
      </div>
      <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>
    </div>

    <div v-if="started" class="inquiry-steps">
      <div
        v-for="(agent, index) in agentSteps"
        :key="agent.label"
        class="inquiry-step"
        :class="stepClass(index)"
      >
        <span>{{ agent.label }}</span>
        <strong>{{ agent.title }}</strong>
        <small>{{ agent.description }}</small>
        <em class="inquiry-step-status">{{ stepStatus(index) }}</em>
      </div>
    </div>

    <div v-if="result" class="inquiry-result-card">
      <h3>🔍 Agent 1 · 询盘分析结果</h3>
      <div class="inquiry-grid-2">
        <div class="inquiry-meta">
          <span>客户意图</span>
          <strong>{{ intentLabels[a1.intent] || a1.intent || "-" }}</strong>
        </div>
        <div class="inquiry-meta">
          <span>客户语言</span>
          <strong>{{ a1.language || "-" }}</strong>
        </div>
        <div class="inquiry-meta">
          <span>紧急程度</span>
          <strong>{{ urgencyText }}</strong>
        </div>
        <div class="inquiry-meta">
          <span>是否需要人工</span>
          <strong>{{ a1.need_human ? "⚠️ 需要转人工" : "✅ AI 可处理" }}</strong>
        </div>
        <div class="inquiry-meta" style="grid-column: 1 / -1">
          <span>核心需求</span>
          <strong>{{ a1.brief_summary || summary.briefSummary || "-" }}</strong>
        </div>
        <div v-if="a1.human_reason" class="inquiry-meta" style="grid-column: 1 / -1">
          <span>转人工原因</span>
          <strong>{{ a1.human_reason }}</strong>
        </div>
      </div>
    </div>

    <div v-if="a2" class="inquiry-result-card">
      <h3>💬 Agent 2 · AI 建议回复</h3>
      <div class="inquiry-reply-box">{{ a2.reply }}</div>
      <div class="inquiry-toolbar">
        <button class="ghost-btn" @click="copyReply">📋 复制回复</button>
      </div>
    </div>

    <div v-if="a3" class="inquiry-result-card">
      <h3>📅 Agent 3 · 跟进计划</h3>
      <div class="inquiry-meta">
        <span>客户优先级</span>
        <strong>{{ priorityLabel(a3.priority) }}</strong>
      </div>
      <div v-for="(step, index) in a3.follow_up_plan || []" :key="index" class="inquiry-follow-step">
        <strong>{{ step.timing }}</strong>（{{ step.method }}）
        <div class="inquiry-follow-msg">{{ step.message }}</div>
      </div>
      <div class="inquiry-meta" style="margin-top: 14px">
        <span>业务员备注</span>
        <strong>{{ a3.strategy_note || summary.strategyNote || "-" }}</strong>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import PageHeader from "../../../components/PageHeader.vue";
import { inquiryApi } from "./api/index.js";
import { inquirySamples, intentLabels, resolveSampleLabel, sourceOptions } from "./samples.js";
import "./inquiry.css";

const router = useRouter();
const route = useRoute();

const agentSteps = [
  {
    label: "Agent 1",
    title: "询盘分析师",
    description: "识别意图、语言、紧急程度"
  },
  {
    label: "Agent 2",
    title: "智能客服",
    description: "基于产品知识库生成专业回复"
  },
  {
    label: "Agent 3",
    title: "跟进策略师",
    description: "制定后续跟进计划和消息"
  }
];

const inquiryText = ref("");
const source = ref("WhatsApp");
const activeSampleLabel = ref(null);
const loading = ref(false);
const started = ref(false);
const activeStep = ref(-1);
const result = ref(null);
const errorMessage = ref("");

const a1 = computed(() => result.value?.steps?.[0]?.output || {});
const a2 = computed(() => result.value?.steps?.[1]?.output || null);
const a3 = computed(() => result.value?.steps?.[2]?.output || null);
const summary = computed(() => result.value?.summary || {});

const urgencyText = computed(() => {
  const score = Number(a1.value.urgency_score ?? summary.value.urgency ?? 0);
  if (!score) return "-";
  return "★".repeat(Math.min(5, Math.max(1, score))) + ` (${score}/5)`;
});

function stepClass(index) {
  const status = stepStatus(index);
  if (status === "任务已完成") return "done";
  if (status === "正在执行当前任务") return "active";
  return "pending";
}

function stepStatus(index) {
  const steps = result.value?.steps || [];
  const hasOutput = Boolean(steps[index]?.output && Object.keys(steps[index].output).length);

  if (hasOutput || activeStep.value > index || activeStep.value >= 3) {
    return "任务已完成";
  }
  if (activeStep.value === index && loading.value) {
    return "正在执行当前任务";
  }
  return "等待执行";
}

function priorityLabel(value) {
  if (value === "high") return "高优先级";
  if (value === "medium") return "中优先级";
  if (value === "low") return "低优先级";
  return value || "-";
}

function onInquiryInput() {
  activeSampleLabel.value = null;
}

function applySample(sample) {
  inquiryText.value = sample.text;
  source.value = sample.source;
  activeSampleLabel.value = sample.label;
}

async function analyze() {
  if (!inquiryText.value.trim()) {
    errorMessage.value = "请输入询盘内容。";
    return;
  }

  loading.value = true;
  started.value = true;
  activeStep.value = 0;
  result.value = null;
  errorMessage.value = "";

  const timer = window.setInterval(() => {
    if (activeStep.value < 2) activeStep.value += 1;
  }, 3500);

  try {
    const response = await inquiryApi.analyze({
      inquiry_text: inquiryText.value.trim(),
      source: source.value,
      sample_label: activeSampleLabel.value || undefined
    });
    result.value = response.data;
    activeStep.value = 3;
    if (result.value?.status === "error") {
      errorMessage.value = result.value.errorMessage || result.value.error || "分析失败";
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    window.clearInterval(timer);
    loading.value = false;
  }
}

async function copyReply() {
  const text = a2.value?.reply || summary.value.suggestedReply || "";
  if (!text) return;
  await navigator.clipboard.writeText(text);
}

async function loadRecord(id) {
  try {
    const response = await inquiryApi.getHistory(id);
    result.value = response.data;
    inquiryText.value = response.data?.inquiryText || "";
    source.value = response.data?.source || "WhatsApp";
    activeSampleLabel.value = resolveSampleLabel(
      inquiryText.value,
      response.data?.sampleLabel
    );
    started.value = true;
    activeStep.value = 3;
  } catch (error) {
    errorMessage.value = error.message;
  }
}

onMounted(async () => {
  if (route.query.id) {
    await loadRecord(String(route.query.id));
  }
});
</script>

<style scoped></style>

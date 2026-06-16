<template>
  <section v-if="!isDetail" class="workflow-list-page">
    <PageHeader
      eyebrow="AI Team Orchestration"
      title="AI 工作流"
      description="每个任务对应一个 AI 团队，自由调整员工执行顺序，一句话生成完整报告。"
    />

    <div class="workflow-list-toolbar">
      <div class="workflow-metrics">
        <span><strong>{{ tasks.length }}</strong> 全部任务</span>
        <span><strong>{{ runningCount }}</strong> 正在执行</span>
        <span><strong>{{ completedCount }}</strong> 已完成</span>
      </div>
      <div class="workflow-list-actions">
        <input v-model.trim="keyword" type="search" placeholder="搜索任务或团队">
        <button class="primary-btn" @click="openCreate">新增工作流</button>
      </div>
    </div>

    <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

    <div class="workflow-task-grid">
      <article
        v-for="item in filteredTasks"
        :key="item.id"
        class="workflow-task-card"
        @click="router.push(`/enterprise/workflows/${item.id}`)"
      >
        <div class="workflow-task-head">
          <span class="workflow-task-icon">WF</span>
          <span class="workflow-status" :class="item.status">{{ statusText(item.status) }}</span>
        </div>
        <h2>{{ item.name }}</h2>
        <p>{{ item.description || "暂无任务说明" }}</p>
        <div class="workflow-team-line">
          <span>AI 团队</span>
          <strong>{{ item.teamName }}</strong>
        </div>
        <div class="workflow-card-meta">
          <span>{{ item.agentCount }} 位 AI 员工</span>
          <time>{{ formatDate(item.updatedAt) }}</time>
        </div>
        <div class="workflow-card-actions" @click.stop>
          <button class="tiny-btn" @click="openEdit(item)">编辑</button>
          <button class="danger-btn" @click="removeTask(item)">删除</button>
          <button class="primary-btn" @click="router.push(`/enterprise/workflows/${item.id}`)">
            打开任务
          </button>
        </div>
      </article>

      <button class="workflow-task-card workflow-add-card" @click="openCreate">
        <span>+</span>
        <strong>创建工作流任务</strong>
        <small>选择一个 AI 团队开始编排</small>
      </button>
    </div>

    <div v-if="drawerOpen" class="drawer-backdrop">
      <aside class="drawer workflow-task-drawer">
        <div class="drawer-head">
          <div>
            <h2>{{ form.id ? "编辑工作流" : "新增工作流" }}</h2>
            <span>Workflow Task</span>
          </div>
          <button class="icon-btn" title="关闭" @click="closeDrawer">×</button>
        </div>
        <div class="drawer-form">
          <label>任务名称
            <input v-model.trim="form.name" placeholder="例如 海外品牌增长计划">
          </label>
          <label>对应 AI 团队
            <select v-model.number="form.teamId" :disabled="Boolean(form.id)">
              <option :value="0" disabled>请选择团队</option>
              <option v-for="team in teamOptions" :key="team.id" :value="team.id">
                {{ team.name }} · {{ team.agents.length }} 位员工
              </option>
            </select>
          </label>
          <label>任务说明
            <textarea v-model.trim="form.description" placeholder="填写任务目标和报告要求"></textarea>
          </label>
          <label class="drawer-check">
            <input v-model="form.enabled" type="checkbox">
            启用该工作流
          </label>
          <p v-if="drawerError" class="form-error">{{ drawerError }}</p>
        </div>
        <button class="primary-btn full" :disabled="saving" @click="saveTask">
          {{ saving ? "正在保存..." : form.id ? "确认保存" : "创建并配置顺序" }}
        </button>
      </aside>
    </div>
  </section>

  <section v-else class="workflow-sequence-page">
    <div class="workflow-sequence-header">
      <button class="icon-btn" title="返回工作流列表" @click="router.push('/enterprise/workflows')">←</button>
      <div>
        <span class="eyebrow">Sequential Agent Workflow</span>
        <h1>{{ task.name || "AI 工作流" }}</h1>
        <p>{{ task.teamName }} · 拖动员工卡片调整执行顺序</p>
      </div>
      <span class="workflow-status" :class="runStatus">{{ statusText(runStatus) }}</span>
    </div>

    <div class="workflow-sequence-layout">
      <div class="workflow-request-panel">
        <div class="workflow-section-heading">
          <div>
            <span class="eyebrow">One-line Brief</span>
            <h2>输入一句任务需求</h2>
          </div>
          <span>{{ agents.length }} 个执行步骤</span>
        </div>
        <textarea
          v-model.trim="prompt"
          class="workflow-requirement-input"
          :disabled="running"
          placeholder="例如：为海南椰子水品牌制定进入东南亚市场的完整增长方案，预算50万元。"
        ></textarea>

        <div class="workflow-run-actions">
          <button class="ghost-btn" :disabled="running || orderSaving" @click="saveOrder">
            {{ orderSaving ? "保存中..." : orderSaved ? "顺序已保存" : "保存执行顺序" }}
          </button>
          <button class="primary-btn" :disabled="running || !prompt" @click="startRun">
            {{ running ? "AI 团队执行中..." : "运行并生成报告" }}
          </button>
        </div>
        <p v-if="pageError" class="form-error">{{ pageError }}</p>

        <div class="workflow-report-state">
          <div>
            <strong>{{ reportTitle }}</strong>
            <span>{{ reportDescription }}</span>
          </div>
          <button
            v-if="pdfReady"
            class="primary-btn"
            @click="downloadReport"
          >
            下载完整 PDF 报告
          </button>
        </div>

        <div v-if="reportSections.length" class="workflow-report-preview">
          <h3>报告章节预览</h3>
          <article v-for="section in reportSections" :key="section.agentId">
            <span>{{ section.title }}</span>
            <p>{{ sectionSummary(section.content) }}</p>
          </article>
        </div>
      </div>

      <div class="workflow-order-panel">
        <div class="workflow-section-heading">
          <div>
            <span class="eyebrow">Execution Order</span>
            <h2>AI 员工执行顺序</h2>
          </div>
          <small>按住卡片拖动</small>
        </div>

        <div class="workflow-agent-order-list">
          <article
            v-for="(agent, index) in agents"
            :key="agent.id"
            class="workflow-order-card"
            :class="[agent.runStatus, { dragging: dragIndex === index }]"
            draggable="true"
            @dragstart="onDragStart(index)"
            @dragover.prevent
            @drop="onDrop(index)"
            @dragend="dragIndex = -1"
          >
            <span class="workflow-order-number">{{ index + 1 }}</span>
            <i>{{ avatarText(agent) }}</i>
            <div>
              <strong>{{ agent.name }}</strong>
              <span>{{ agent.category }}<template v-if="agent.model"> · {{ agent.model }}</template></span>
              <small>{{ agentStatusText(agent.runStatus) }}</small>
              <p v-if="agent.output">{{ sectionSummary(agent.output) }}</p>
              <p v-if="agent.errorMessage" class="form-error">{{ agent.errorMessage }}</p>
            </div>
            <b class="workflow-live-dot"></b>
            <span class="workflow-drag-handle" title="拖动排序">⋮⋮</span>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import PageHeader from "../../../components/PageHeader.vue";
import { workflowsApi } from "./api/index.js";

const route = useRoute();
const router = useRouter();
const isDetail = computed(() => Boolean(route.params.id));
const tasks = ref([]);
const teamOptions = ref([]);
const keyword = ref("");
const errorMessage = ref("");
const drawerError = ref("");
const drawerOpen = ref(false);
const saving = ref(false);
const task = reactive({ id: null, name: "", teamId: null, teamName: "", status: "ready" });
const agents = ref([]);
const prompt = ref("");
const pageError = ref("");
const orderSaving = ref(false);
const orderSaved = ref(false);
const dragIndex = ref(-1);
const runId = ref("");
const runStatus = ref("idle");
const pdfReady = ref(false);
const reportSections = ref([]);
let pollTimer = null;

const defaults = () => ({ id: null, name: "", teamId: 0, description: "", enabled: true });
const form = reactive(defaults());
const running = computed(() => runStatus.value === "running");
const runningCount = computed(() => tasks.value.filter((item) => item.status === "running").length);
const completedCount = computed(() => tasks.value.filter((item) => item.status === "completed").length);
const filteredTasks = computed(() => {
  const value = keyword.value.toLowerCase();
  return value
    ? tasks.value.filter((item) =>
        `${item.name} ${item.teamName} ${item.description}`.toLowerCase().includes(value)
      )
    : tasks.value;
});
const reportTitle = computed(() => {
  if (runStatus.value === "completed") return "完整报告已生成";
  if (runStatus.value === "failed") return "报告生成失败";
  if (runStatus.value === "running") return "AI 团队正在协作";
  return "等待开始任务";
});
const reportDescription = computed(() => {
  if (runStatus.value === "completed") return "所有 Agent 已按顺序完成任务，可以下载 PDF。";
  if (runStatus.value === "failed") return "请检查模型配置或 Agent 错误后重新运行。";
  if (runStatus.value === "running") return "后一个 Agent 会读取前面 Agent 的累计结果。";
  return "保存员工顺序并输入需求后，系统将自动生成完整报告。";
});

function statusText(status) {
  return {
    idle: "尚未运行",
    draft: "草稿",
    ready: "已就绪",
    running: "执行中",
    completed: "已完成",
    failed: "执行失败"
  }[status] || status;
}

function agentStatusText(status) {
  return {
    idle: "等待任务",
    queued: "等待前序 Agent",
    running: "正在执行当前任务",
    completed: "任务已完成",
    failed: "任务执行失败"
  }[status] || "等待任务";
}

function avatarText(agent) {
  return (agent.nameEn || agent.name || "AI").slice(0, 2).toUpperCase();
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString("zh-CN", { hour12: false }) : "";
}

function sectionSummary(value) {
  const content = value?.summary || value?.data?.summary || value?.message || value;
  if (typeof content === "string") return content.slice(0, 160);
  return JSON.stringify(content).slice(0, 160);
}

async function loadList() {
  try {
    const [taskResponse, teamResponse] = await Promise.all([
      workflowsApi.list(),
      workflowsApi.teams()
    ]);
    tasks.value = taskResponse.data || [];
    teamOptions.value = teamResponse.data || [];
  } catch (error) {
    errorMessage.value = error.message;
  }
}

async function loadDetail() {
  pageError.value = "";
  try {
    const response = await workflowsApi.detail(route.params.id);
    Object.assign(task, response.data);
    agents.value = response.data.agents || [];
    const latest = response.data.latestRun;
    if (latest) {
      runId.value = latest.id;
      runStatus.value = latest.status;
      prompt.value = latest.prompt || "";
      pdfReady.value = Boolean(latest.pdfReady);
      if (latest.status === "running") pollTimer = window.setTimeout(pollRun, 500);
      if (latest.status === "completed") await refreshRun();
    }
  } catch (error) {
    pageError.value = error.message;
  }
}

function openCreate() {
  Object.assign(form, defaults());
  drawerError.value = "";
  drawerOpen.value = true;
}

function openEdit(item) {
  Object.assign(form, {
    id: item.id,
    name: item.name,
    teamId: item.teamId,
    description: item.description,
    enabled: item.enabled
  });
  drawerError.value = "";
  drawerOpen.value = true;
}

function closeDrawer() {
  if (window.confirm("关闭后未保存内容将丢失，确定关闭吗？")) drawerOpen.value = false;
}

async function saveTask() {
  if (!form.name || !form.teamId) {
    drawerError.value = "请填写任务名称并选择 AI 团队";
    return;
  }
  saving.value = true;
  try {
    const payload = {
      name: form.name,
      team_id: form.teamId,
      description: form.description || null,
      enabled: form.enabled
    };
    if (form.id) {
      await workflowsApi.update(form.id, payload);
      drawerOpen.value = false;
      await loadList();
    } else {
      const response = await workflowsApi.create(payload);
      drawerOpen.value = false;
      router.push(`/enterprise/workflows/${response.data.id}`);
    }
  } catch (error) {
    drawerError.value = error.message;
  } finally {
    saving.value = false;
  }
}

async function removeTask(item) {
  if (!window.confirm(`确定删除工作流“${item.name}”及其运行记录吗？`)) return;
  try {
    await workflowsApi.delete(item.id);
    await loadList();
  } catch (error) {
    errorMessage.value = error.message;
  }
}

function onDragStart(index) {
  if (running.value) return;
  dragIndex.value = index;
}

function onDrop(index) {
  if (running.value || dragIndex.value < 0 || dragIndex.value === index) return;
  const next = [...agents.value];
  const [moved] = next.splice(dragIndex.value, 1);
  next.splice(index, 0, moved);
  agents.value = next;
  dragIndex.value = -1;
  orderSaved.value = false;
}

async function saveOrder() {
  orderSaving.value = true;
  pageError.value = "";
  try {
    const response = await workflowsApi.saveOrder(
      task.id,
      agents.value.map((agent) => agent.id)
    );
    agents.value = response.data.agents || agents.value;
    orderSaved.value = true;
  } catch (error) {
    pageError.value = error.message;
  } finally {
    orderSaving.value = false;
  }
}

async function startRun() {
  await saveOrder();
  if (pageError.value) return;
  pdfReady.value = false;
  reportSections.value = [];
  try {
    const response = await workflowsApi.run(task.id, prompt.value);
    runId.value = response.data.runId;
    runStatus.value = "running";
    agents.value = agents.value.map((agent) => ({ ...agent, runStatus: "queued", output: null }));
    pollTimer = window.setTimeout(pollRun, 500);
  } catch (error) {
    pageError.value = error.message;
    runStatus.value = "failed";
  }
}

async function refreshRun() {
  const response = await workflowsApi.runStatus(task.id, runId.value);
  runStatus.value = response.data.status;
  pdfReady.value = Boolean(response.data.pdfReady);
  reportSections.value = response.data.reportData?.sections || [];
  agents.value = response.data.agents || agents.value;
  pageError.value = response.data.errorMessage || "";
  return response.data.status;
}

async function pollRun() {
  try {
    const status = await refreshRun();
    if (status === "running") pollTimer = window.setTimeout(pollRun, 900);
  } catch (error) {
    pageError.value = error.message;
    runStatus.value = "failed";
  }
}

async function downloadReport() {
  try {
    await workflowsApi.downloadReport(task.id, runId.value);
  } catch (error) {
    pageError.value = error.message;
  }
}

watch(
  () => route.params.id,
  (id) => {
    window.clearTimeout(pollTimer);
    if (id) loadDetail();
    else loadList();
  }
);

onMounted(() => {
  if (isDetail.value) loadDetail();
  else loadList();
});

onUnmounted(() => window.clearTimeout(pollTimer));
</script>

<style scoped>
/* Page-specific styles are maintained in the global stylesheet. */
</style>

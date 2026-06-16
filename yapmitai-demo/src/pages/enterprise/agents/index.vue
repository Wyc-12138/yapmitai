<template>
  <section>
    <PageHeader
      eyebrow="Super AI Agent Center"
      title="超级AI员工中心"
      description="统一管理企业智能体、增长团队角色、模型和系统提示词。"
    />

    <div class="page-toolbar">
      <div class="tabs agent-category-tabs">
        <button
          v-for="item in categories"
          :key="item"
          :class="{ active: filter === item }"
          @click="filter = item"
        >
          {{ item }}
        </button>
      </div>
      <button class="primary-btn" @click="openCreate">新增AI员工</button>
    </div>

    <p v-if="errorMessage && !drawerOpen" class="form-error">{{ errorMessage }}</p>

    <div class="agent-grid agent-crud-grid">
      <article v-for="agent in visibleAgents" :key="agent.id" class="agent-card">
        <div class="agent-card-top">
          <div class="avatar-ring" :class="agent.status">
            {{ avatarText(agent) }}
          </div>
          <span class="status-badge" :class="agent.status">
            {{ statusText(agent.status) }}
          </span>
        </div>
        <strong>{{ agent.name }}</strong>
        <small>{{ agent.nameEn || agent.code }}</small>
        <p>{{ agent.description || "暂无角色说明" }}</p>
        <div class="agent-meta">
          <span>{{ agent.category }}</span>
          <span>{{ agent.model || "未选择模型" }}</span>
        </div>
        <div class="agent-card-footer">
          <span>今日完成 <b>{{ agent.todayDone }}</b> 项</span>
          <span>月KPI <b>{{ agent.monthKPI }}%</b></span>
        </div>
        <div class="row-actions agent-card-actions">
          <button class="tiny-btn" @click="openEdit(agent)">编辑</button>
          <button class="danger-btn" @click="removeAgent(agent)">删除</button>
        </div>
      </article>

      <button class="agent-card add-card" @click="openCreate">
        <span>+</span>
        添加新AI员工
      </button>
    </div>

    <div v-if="drawerOpen" class="drawer-backdrop agent-editor-backdrop">
      <aside class="drawer agent-editor-drawer">
        <div class="drawer-head">
          <div>
            <h2>{{ form.id ? "编辑AI员工" : "新增AI员工" }}</h2>
            <span>{{ form.nameEn || "Agent Profile" }}</span>
          </div>
          <button class="icon-btn" title="关闭" @click="closeDrawer">×</button>
        </div>

        <div class="drawer-form agent-editor-form">
          <div class="agent-form-grid">
            <label>角色编码
              <input v-model.trim="form.code" placeholder="例如 growth-market-research">
            </label>
            <label>中文名称
              <input v-model.trim="form.name" placeholder="例如 市场研究 Agent">
            </label>
            <label>英文名称
              <input v-model.trim="form.nameEn" placeholder="Market Research">
            </label>
            <label>分类
              <input v-model.trim="form.category" list="agent-categories" placeholder="例如 品牌增长">
              <datalist id="agent-categories">
                <option v-for="item in categories.slice(1)" :key="item" :value="item"></option>
              </datalist>
            </label>
            <label>Chat 模型
              <select v-model="form.chatModelConfigId">
                <option :value="null">使用系统默认模型</option>
                <option v-for="model in chatModels" :key="model.id" :value="model.id">
                  {{ model.displayName }}{{ model.isDefault ? " · 默认" : "" }}
                </option>
              </select>
            </label>
            <label>运行状态
              <select v-model="form.status">
                <option value="standby">待命中</option>
                <option value="working">工作中</option>
                <option value="offline">离线</option>
              </select>
            </label>
            <label>今日完成
              <input v-model.number="form.todayDone" type="number" min="0">
            </label>
            <label>月KPI
              <input v-model.number="form.monthKPI" type="number" min="0" max="100">
            </label>
          </div>

          <label>头像地址
            <input v-model.trim="form.avatar" placeholder="可选，填写图片 URL">
          </label>
          <label>角色说明
            <textarea v-model.trim="form.description" placeholder="说明该 Agent 的职责和使用场景"></textarea>
          </label>
          <label>System Prompt
            <textarea
              v-model="form.systemPrompt"
              class="agent-prompt-input"
              placeholder="定义角色、输入输出要求和工作边界"
            ></textarea>
          </label>
          <label class="drawer-check">
            <input v-model="form.enabled" type="checkbox">
            启用该 AI 员工
          </label>
          <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>
        </div>

        <button class="primary-btn full agent-editor-submit" :disabled="saving" @click="saveAgent">
          {{ saving ? "正在保存..." : form.id ? "确认保存" : "确认新增" }}
        </button>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import PageHeader from "../../../components/PageHeader.vue";
import { agentsApi } from "./api/index.js";

const agents = ref([]);
const chatModels = ref([]);
const filter = ref("全部");
const loading = ref(false);
const saving = ref(false);
const drawerOpen = ref(false);
const errorMessage = ref("");

const defaults = () => ({
  id: null,
  code: "",
  name: "",
  nameEn: "",
  description: "",
  avatar: "",
  chatModelConfigId: null,
  systemPrompt: "",
  category: "品牌增长",
  status: "standby",
  enabled: true,
  todayDone: 0,
  monthKPI: 0
});

const form = reactive(defaults());
const categories = computed(() => [
  "全部",
  ...new Set(["品牌增长", ...agents.value.map((item) => item.category).filter(Boolean)])
]);
const visibleAgents = computed(() =>
  filter.value === "全部"
    ? agents.value
    : agents.value.filter((item) => item.category === filter.value)
);

function avatarText(agent) {
  return (agent.nameEn || agent.name || "AI").slice(0, 2).toUpperCase();
}

function statusText(status) {
  return { working: "工作中", standby: "待命中", offline: "离线" }[status] || status;
}

function resetForm(value = {}) {
  Object.assign(form, defaults(), value);
}

async function loadData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [agentResponse, modelResponse] = await Promise.all([
      agentsApi.list(),
      agentsApi.chatModels()
    ]);
    agents.value = agentResponse.data || [];
    chatModels.value = modelResponse.data || [];
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  resetForm();
  errorMessage.value = "";
  drawerOpen.value = true;
}

function openEdit(agent) {
  resetForm(agent);
  errorMessage.value = "";
  drawerOpen.value = true;
}

function closeDrawer() {
  if (!window.confirm("退出后当前内容不会保存，确定退出吗？")) return;
  drawerOpen.value = false;
}

function buildPayload() {
  return {
    code: form.code,
    name: form.name,
    name_en: form.nameEn || null,
    description: form.description || null,
    avatar: form.avatar || null,
    chat_model_config_id: form.chatModelConfigId || null,
    system_prompt: form.systemPrompt,
    category: form.category,
    status: form.status,
    enabled: form.enabled,
    today_done: Number(form.todayDone) || 0,
    month_kpi: Number(form.monthKPI) || 0
  };
}

async function saveAgent() {
  if (!form.code || !form.name || !form.category) {
    errorMessage.value = "请填写角色编码、中文名称和分类。";
    return;
  }
  if (!/^[a-z0-9-]+$/.test(form.code)) {
    errorMessage.value = "角色编码只能使用小写字母、数字和短横线。";
    return;
  }
  saving.value = true;
  errorMessage.value = "";
  try {
    if (form.id) {
      await agentsApi.update(form.id, buildPayload());
    } else {
      await agentsApi.create(buildPayload());
    }
    drawerOpen.value = false;
    await loadData();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    saving.value = false;
  }
}

async function removeAgent(agent) {
  if (!window.confirm(`确定删除 AI 员工“${agent.name}”吗？删除后相关工作流可能无法运行。`)) return;
  try {
    await agentsApi.delete(agent.id);
    await loadData();
  } catch (error) {
    errorMessage.value = error.message;
  }
}

onMounted(loadData);
</script>

<style scoped>
</style>

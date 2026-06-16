<template>
  <section class="teams-page">
    <PageHeader
      eyebrow="AI Team Workspace"
      title="AI团队"
      description="将不同能力的 AI 员工自由组合为协作团队，并统一维护团队状态。"
    />

    <div class="team-summary-grid">
      <article>
        <span>团队总数</span>
        <strong>{{ summary.teamCount }}</strong>
      </article>
      <article>
        <span>启用团队</span>
        <strong>{{ summary.enabledCount }}</strong>
      </article>
      <article>
        <span>成员关系</span>
        <strong>{{ summary.memberLinks }}</strong>
      </article>
      <button class="primary-btn" @click="openCreate">新增AI团队</button>
    </div>

    <p v-if="errorMessage && !drawerOpen" class="form-error">{{ errorMessage }}</p>

    <div class="team-grid">
      <article v-for="team in teams" :key="team.id" class="team-card">
        <div class="team-card-head">
          <div>
            <span class="eyebrow">AI Team · {{ team.id }}</span>
            <h2>{{ team.name }}</h2>
          </div>
          <span class="team-enabled" :class="{ disabled: !team.enabled }">
            {{ team.enabled ? "启用" : "停用" }}
          </span>
        </div>
        <p>{{ team.description || "暂无团队说明" }}</p>
        <div class="team-member-heading">
          <strong>{{ team.memberCount }} 位 AI 员工</strong>
          <span>{{ formatDate(team.updatedAt) }}</span>
        </div>
        <div v-if="team.agents.length" class="team-member-list">
          <span v-for="agent in team.agents" :key="agent.id" class="team-member-chip">
            <i>{{ avatarText(agent) }}</i>
            {{ agent.name }}
          </span>
        </div>
        <div v-else class="team-empty-members">尚未选择团队成员</div>
        <div class="row-actions team-card-actions">
          <button class="tiny-btn" @click="openEdit(team)">编辑团队</button>
          <button class="danger-btn" @click="removeTeam(team)">删除</button>
        </div>
      </article>

      <button class="team-card team-add-card" @click="openCreate">
        <span>+</span>
        <strong>创建新的 AI 团队</strong>
        <small>自由选择一个或多个 AI 员工</small>
      </button>
    </div>

    <div v-if="drawerOpen" class="drawer-backdrop team-drawer-backdrop">
      <aside class="drawer team-drawer">
        <div class="drawer-head">
          <div>
            <h2>{{ form.id ? "编辑AI团队" : "新增AI团队" }}</h2>
            <span>{{ form.id ? `${form.agentIds.length} 位成员` : "Team Builder" }}</span>
          </div>
          <button class="icon-btn" title="关闭" @click="closeDrawer">×</button>
        </div>

        <div class="drawer-form team-drawer-form">
          <label>团队名称
            <input v-model.trim="form.name" placeholder="例如 海外品牌增长团队">
          </label>
          <label>团队说明
            <textarea v-model.trim="form.description" placeholder="说明团队目标、职责和适用场景"></textarea>
          </label>
          <label class="drawer-check">
            <input v-model="form.enabled" type="checkbox">
            启用该团队
          </label>

          <div class="team-selector-head">
            <div>
              <strong>选择 AI 员工</strong>
              <span>已选择 {{ form.agentIds.length }} 位</span>
            </div>
            <button class="tiny-btn" @click="toggleAll">
              {{ allSelected ? "取消全选" : "全选" }}
            </button>
          </div>

          <div class="team-agent-selector">
            <label
              v-for="agent in agentOptions"
              :key="agent.id"
              class="team-agent-option"
              :class="{ selected: form.agentIds.includes(agent.id) }"
            >
              <input v-model="form.agentIds" type="checkbox" :value="agent.id">
              <span class="team-agent-avatar">{{ avatarText(agent) }}</span>
              <span>
                <strong>{{ agent.name }}</strong>
                <small>{{ agent.category }} · {{ statusText(agent.status) }}</small>
              </span>
            </label>
          </div>
          <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>
        </div>

        <button class="primary-btn full team-submit" :disabled="saving" @click="saveTeam">
          {{ saving ? "正在保存..." : form.id ? "确认保存" : "确认新增" }}
        </button>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import PageHeader from "../../../components/PageHeader.vue";
import { teamsApi } from "./api/index.js";

const teams = ref([]);
const agentOptions = ref([]);
const summary = reactive({ teamCount: 0, enabledCount: 0, memberLinks: 0 });
const drawerOpen = ref(false);
const saving = ref(false);
const errorMessage = ref("");

const defaults = () => ({
  id: null,
  name: "",
  description: "",
  enabled: true,
  agentIds: []
});
const form = reactive(defaults());

const allSelected = computed(
  () =>
    agentOptions.value.length > 0 &&
    form.agentIds.length === agentOptions.value.length
);

function resetForm(value = {}) {
  Object.assign(form, defaults(), value, {
    agentIds: [...(value.agentIds || [])]
  });
}

function avatarText(agent) {
  return (agent.nameEn || agent.name || "AI").slice(0, 2).toUpperCase();
}

function statusText(status) {
  return { working: "工作中", standby: "待命中", offline: "离线" }[status] || status;
}

function formatDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString("zh-CN");
}

async function loadData() {
  errorMessage.value = "";
  try {
    const [teamResponse, agentResponse, summaryResponse] = await Promise.all([
      teamsApi.list(),
      teamsApi.agentOptions(),
      teamsApi.summary()
    ]);
    teams.value = teamResponse.data || [];
    agentOptions.value = agentResponse.data || [];
    Object.assign(summary, summaryResponse.data || {});
  } catch (error) {
    errorMessage.value = error.message;
  }
}

function openCreate() {
  resetForm();
  errorMessage.value = "";
  drawerOpen.value = true;
}

function openEdit(team) {
  resetForm(team);
  errorMessage.value = "";
  drawerOpen.value = true;
}

function closeDrawer() {
  if (!window.confirm("退出后当前内容不会保存，确定退出吗？")) return;
  drawerOpen.value = false;
}

function toggleAll() {
  form.agentIds = allSelected.value
    ? []
    : agentOptions.value.map((agent) => agent.id);
}

async function saveTeam() {
  if (!form.name) {
    errorMessage.value = "请填写团队名称。";
    return;
  }
  saving.value = true;
  errorMessage.value = "";
  const payload = {
    name: form.name,
    description: form.description || null,
    enabled: form.enabled,
    agent_ids: form.agentIds
  };
  try {
    form.id
      ? await teamsApi.update(form.id, payload)
      : await teamsApi.create(payload);
    drawerOpen.value = false;
    await loadData();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    saving.value = false;
  }
}

async function removeTeam(team) {
  if (!window.confirm(`确定删除 AI 团队“${team.name}”吗？团队成员不会被删除。`)) return;
  try {
    await teamsApi.delete(team.id);
    await loadData();
  } catch (error) {
    errorMessage.value = error.message;
  }
}

onMounted(loadData);
</script>

<style scoped>
</style>

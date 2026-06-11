<template>
  <section>
    <PageHeader eyebrow="Super AI Agent Center" title="超级AI员工中心" description="像管理团队一样管理AI。" />
    <div class="page-toolbar"><div class="tabs"><button v-for="item in categories" :key="item" :class="{ active: filter === item }" @click="filter = item">{{ item }}</button></div><button class="primary-btn">新增AI员工</button></div>
    <div class="agent-grid">
      <button v-for="agent in visible" :key="agent.id" class="agent-card" @click="selected = agent">
        <div class="avatar-ring" :class="agent.status">AI</div><strong>{{ agent.name }}</strong><small>{{ agent.nameEn }}</small>
        <span class="status-badge" :class="agent.status">{{ statusText(agent.status) }}</span>
        <div class="agent-card-footer"><span>今日完成 <b>{{ agent.completedTasks }}</b> 项</span><span>月KPI <b>{{ agent.monthKPI }}</b></span></div>
        <div class="card-actions"><span>查看详情</span><span>分配任务</span></div>
      </button>
      <button class="agent-card add-card">+ 添加新AI员工</button>
    </div>

    <div v-if="selected" class="drawer-backdrop" @click.self="closeDrawer">
      <aside class="drawer">
        <div class="drawer-head"><div><h2>{{ selected.name }}</h2><span>{{ selected.nameEn }}</span></div><button class="icon-btn" @click="closeDrawer">×</button></div>
        <p class="drawer-desc">{{ selected.description }}</p>
        <ProgressBar label="本月完成率" :value="selected.monthKPI" />
        <ProgressBar label="质量分" :value="Math.min(99, selected.monthKPI + 3)" />
        <h3>今日工作日志</h3><div class="timeline"><div v-for="item in selected.todayLog" :key="`${item.time}-${item.action}`"><time>{{ item.time }}</time><span>{{ item.action }}</span></div></div>
        <button class="primary-btn full" @click="taskOpen = true; submitted = false">分配任务</button>
      </aside>
    </div>

    <div v-if="taskOpen" class="modal-backdrop" @click.self="taskOpen = false">
      <div class="modal"><h2>分配任务</h2>
        <div v-if="submitted" class="success-state"><strong>任务已进入队列</strong><span>AI员工状态已更新为进行中</span></div>
        <template v-else><label class="field-label">任务描述</label><textarea v-model="task.description" placeholder="例如：生成品牌出海内容包（英文版）"></textarea><label class="field-label">截止时间</label><input v-model="task.deadline" readonly><label class="field-label">优先级</label><select v-model="task.priority"><option>高</option><option>中</option><option>低</option></select><button class="primary-btn full" @click="submitted = true">提交任务</button></template>
      </div>
    </div>
  </section>
</template>
<script setup>
import { computed, reactive, ref } from "vue";
import PageHeader from "../../../components/PageHeader.vue";
import ProgressBar from "../../../components/ProgressBar.vue";
import { agents } from "../../../data/mock.js";
const categories = ["全部", "营销类", "运营类", "客服类", "数据类", "管理类"];
const filter = ref("全部");
const selected = ref(null);
const taskOpen = ref(false);
const submitted = ref(false);
const task = reactive({ description: "", deadline: "今天 18:00", priority: "高" });
const visible = computed(() => filter.value === "全部" ? agents : agents.filter((item) => item.category === filter.value));
const statusText = (status) => ({ working: "工作中", standby: "待命中", offline: "离线" })[status] || status;
function closeDrawer() { selected.value = null; taskOpen.value = false; }
</script>
<style scoped></style>

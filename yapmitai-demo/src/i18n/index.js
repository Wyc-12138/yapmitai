import { ref } from "vue";
import { translateTexts } from "./api.js";

const STORAGE_KEY = "yapmitai-language";
const CACHE_KEY = "yapmitai-en-translation-cache";
const CHINESE_PATTERN = /[\u3400-\u9fff]/;
const SKIPPED_TAGS = new Set(["SCRIPT", "STYLE", "CODE", "PRE", "TEXTAREA"]);
const TRANSLATED_ATTRIBUTES = ["placeholder", "title", "aria-label"];
const textOriginals = new WeakMap();
const attributeOriginals = new WeakMap();
const pending = new Map();

export const language = ref(window.localStorage.getItem(STORAGE_KEY) === "en" ? "en" : "zh");

let rootElement = null;
let observer = null;
let flushTimer = null;
let applyingTranslations = false;

const immediateTranslations = {
  "切换入口": "Switch Portal",
  "企业入口": "Enterprise Portal",
  "员工入口": "Employee Portal",
  "政府入口": "Government Portal",
  "联盟入口": "Alliance Portal",
  "返回入口首页": "Back to portal home",
  "展开侧边栏": "Expand sidebar",
  "收起侧边栏": "Collapse sidebar",
  "当前首页": "Current Home",
  "工作总览": "Overview",
  "企业控制台": "Enterprise Dashboard",
  "AI组织": "AI Organization",
  "超级AI员工": "AI Employees",
  "AI团队": "AI Teams",
  "AI工作流": "AI Workflows",
  "能力中心": "Capabilities",
  "AI工具中心": "AI Tools",
  "企业智库": "Knowledge",
  "AI创作配置": "AI Creation",
  "AI拓客配置": "AI Outreach",
  "个微Agent": "Personal WeChat Agent",
  "企微Agent": "Enterprise WeChat Agent",
  "系统管理": "System",
  "模型配置": "Model Configurations",
  "Agent总配置": "Agent Gateway",
  "调用日志": "Call Logs",
  "新增": "Add",
  "编辑": "Edit",
  "修改": "Edit",
  "删除": "Delete",
  "保存": "Save",
  "取消": "Cancel",
  "关闭": "Close",
  "搜索": "Search",
  "确认": "Confirm",
  "启用": "Enabled",
  "停用": "Disabled",
  "加载中": "Loading"
};

const translationCache = loadCache();
Object.assign(translationCache, immediateTranslations);

function loadCache() {
  try {
    return JSON.parse(window.localStorage.getItem(CACHE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveCache() {
  try {
    const entries = Object.entries(translationCache).slice(-2000);
    window.localStorage.setItem(CACHE_KEY, JSON.stringify(Object.fromEntries(entries)));
  } catch {
    // Translation remains usable in memory when browser storage is unavailable.
  }
}

function isTranslatable(text) {
  const normalized = text.trim();
  return normalized.length > 0 && normalized.length <= 1200 && CHINESE_PATTERN.test(normalized);
}

function isSkipped(element) {
  return !element ||
    SKIPPED_TAGS.has(element.tagName) ||
    Boolean(element.closest?.(".no-translate"));
}

function applyTextTranslation(node, source, translation) {
  if (language.value !== "en" || !node.isConnected) return;
  const current = node.nodeValue || "";
  const leading = current.match(/^\s*/)?.[0] || "";
  const trailing = current.match(/\s*$/)?.[0] || "";
  applyingTranslations = true;
  node.nodeValue = `${leading}${translation}${trailing}`;
  applyingTranslations = false;
  textOriginals.set(node, source);
}

function queueTextNode(node) {
  if (isSkipped(node.parentElement)) return;
  const source = (node.nodeValue || "").trim();
  if (!isTranslatable(source)) return;
  textOriginals.set(node, source);
  const cached = translationCache[source];
  if (cached) {
    applyTextTranslation(node, source, cached);
    return;
  }
  if (!pending.has(source)) pending.set(source, []);
  pending.get(source).push({ type: "text", target: node, source });
}

function queueAttribute(element, attribute) {
  const source = (element.getAttribute(attribute) || "").trim();
  if (!isTranslatable(source) || isSkipped(element)) return;
  const originals = attributeOriginals.get(element) || {};
  originals[attribute] = source;
  attributeOriginals.set(element, originals);
  const cached = translationCache[source];
  if (cached) {
    applyingTranslations = true;
    element.setAttribute(attribute, cached);
    applyingTranslations = false;
    return;
  }
  if (!pending.has(source)) pending.set(source, []);
  pending.get(source).push({ type: "attribute", target: element, attribute, source });
}

function scan(root) {
  if (!root || language.value !== "en") return;
  if (root.nodeType === Node.TEXT_NODE) {
    queueTextNode(root);
  } else if (root.nodeType === Node.ELEMENT_NODE) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node = walker.nextNode();
    while (node) {
      queueTextNode(node);
      node = walker.nextNode();
    }
    const elements = [root, ...root.querySelectorAll("*")];
    for (const element of elements) {
      for (const attribute of TRANSLATED_ATTRIBUTES) {
        if (element.hasAttribute(attribute)) queueAttribute(element, attribute);
      }
    }
  }
  scheduleFlush();
}

function scheduleFlush() {
  if (!pending.size || flushTimer) return;
  flushTimer = window.setTimeout(flushPending, 80);
}

async function flushPending() {
  flushTimer = null;
  const sources = [...pending.keys()].slice(0, 60);
  const jobs = new Map(sources.map((source) => [source, pending.get(source) || []]));
  sources.forEach((source) => pending.delete(source));
  try {
    const translations = await translateTexts(sources);
    Object.assign(translationCache, translations);
    saveCache();
    if (language.value === "en") {
      for (const [source, targets] of jobs) {
        const translation = translations[source];
        if (!translation) continue;
        for (const job of targets) {
          if (job.type === "text") {
            applyTextTranslation(job.target, source, translation);
          } else if (job.target.isConnected) {
            applyingTranslations = true;
            job.target.setAttribute(job.attribute, translation);
            applyingTranslations = false;
          }
        }
      }
    }
  } catch (error) {
    console.warn("Page translation is temporarily unavailable:", error);
  } finally {
    if (pending.size) scheduleFlush();
  }
}

function restoreChinese(root) {
  if (!root) return;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let node = walker.nextNode();
  applyingTranslations = true;
  while (node) {
    const original = textOriginals.get(node);
    if (original) {
      const current = node.nodeValue || "";
      const leading = current.match(/^\s*/)?.[0] || "";
      const trailing = current.match(/\s*$/)?.[0] || "";
      node.nodeValue = `${leading}${original}${trailing}`;
    }
    node = walker.nextNode();
  }
  for (const element of [root, ...root.querySelectorAll("*")]) {
    const originals = attributeOriginals.get(element);
    if (!originals) continue;
    for (const [attribute, original] of Object.entries(originals)) {
      element.setAttribute(attribute, original);
    }
  }
  applyingTranslations = false;
  pending.clear();
}

export function setLanguage(nextLanguage) {
  language.value = nextLanguage === "en" ? "en" : "zh";
  window.localStorage.setItem(STORAGE_KEY, language.value);
  document.documentElement.lang = language.value === "en" ? "en" : "zh-CN";
  if (language.value === "en") {
    scan(rootElement);
  } else {
    restoreChinese(rootElement);
  }
}

export function toggleLanguage() {
  setLanguage(language.value === "zh" ? "en" : "zh");
}

export function installRuntimeI18n(root) {
  rootElement = root;
  document.documentElement.lang = language.value === "en" ? "en" : "zh-CN";
  observer?.disconnect();
  observer = new MutationObserver((mutations) => {
    if (applyingTranslations || language.value !== "en") return;
    for (const mutation of mutations) {
      if (mutation.type === "characterData") {
        queueTextNode(mutation.target);
      } else {
        mutation.addedNodes.forEach((node) => scan(node));
      }
    }
    scheduleFlush();
  });
  observer.observe(root, { childList: true, characterData: true, subtree: true });
  if (language.value === "en") window.setTimeout(() => scan(root), 0);
}

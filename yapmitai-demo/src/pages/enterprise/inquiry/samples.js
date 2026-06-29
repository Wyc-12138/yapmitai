export const inquirySamples = [
  {
    label: "英文询价",
    source: "WhatsApp",
    text:
      "Hi, I am interested in your products. Could you please send me the price list for your stainless steel water bottles? We are looking to order around 500 pieces."
  },
  {
    label: "西班牙语样品",
    source: "WhatsApp",
    text:
      "Hola, me gustaría recibir muestras de sus productos. Somos una empresa de distribución en México. ¿Pueden enviarme información sobre precios y muestras?"
  },
  {
    label: "高紧急大单",
    source: "WhatsApp",
    text:
      "We need 50,000 pieces of your product urgently. Can you confirm availability and best price? We need to ship before July 31."
  },
  {
    label: "投诉转人工",
    source: "WhatsApp",
    text:
      "I received my order last week but the quality is terrible. Many products are defective. I need a refund or replacement. This is unacceptable!"
  }
];

export const intentLabels = {
  price_inquiry: "💰 询价",
  product_info: "📦 产品咨询",
  sample_request: "🎁 申请样品",
  comparison: "🔄 比较竞品",
  complaint: "⚠️ 投诉",
  other: "❓ 其他"
};

export const sourceOptions = ["WhatsApp", "Email", "独立站"];

export function resolveSampleLabel(inquiryText, sampleLabel = null) {
  if (sampleLabel) return sampleLabel;
  const text = (inquiryText || "").trim();
  if (!text) return null;
  const matched = inquirySamples.find((sample) => sample.text.trim() === text);
  return matched?.label ?? null;
}

import { createHash } from "node:crypto";
import { parse, compileScript } from "@vue/compiler-sfc";

export default function vueSfcPlugin() {
  return {
    name: "yapmitai-vue-sfc",
    enforce: "pre",
    transform(source, id) {
      if (!id.endsWith(".vue")) return null;

      const { descriptor, errors } = parse(source, { filename: id });
      if (errors.length) {
        throw errors[0];
      }

      const scopeId = createHash("sha256").update(id).digest("hex").slice(0, 8);
      const compiled = compileScript(descriptor, {
        id: scopeId,
        inlineTemplate: true,
        templateOptions: {
          compilerOptions: descriptor.styles.some((style) => style.scoped)
            ? { scopeId: `data-v-${scopeId}` }
            : {}
        }
      });

      return {
        code: compiled.content,
        map: null
      };
    }
  };
}

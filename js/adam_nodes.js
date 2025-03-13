import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
  name: "AdamWhiteC",

  beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "AdamTextBox") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated?.apply(this, arguments);
        return r;
      };

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);

        for (const widget of this.widgets) {
          if (widget.type === "customtext") {
            widget.value = message.text.join("");
          }
        }

        this.onResize?.(this.size);
      };
    }
    
    // 修改对AdamRandomizeText节点的支持
    if (nodeData.name === "AdamRandomizeText") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated?.apply(this, arguments);
        return r;
      };

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);

        // 更新显示结果/ShowResult字段
        for (const widget of this.widgets) {
          if (widget.name === "显示结果/ShowResult") {
            // 检查message.result是否存在并且是数组
            if (message.result && Array.isArray(message.result)) {
              // 使用第一个输出（全部文本）作为显示结果
              widget.value = message.result[0];
            }
          }
        }

        this.onResize?.(this.size);
      };
    }
    
    if (nodeData.name === "ImageSizeInfo") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated?.apply(this, arguments);
        const iw = ComfyWidgets["INT"](this, "width", ["INT", {}], app).widget;
        const ih = ComfyWidgets["INT"](this, "height", ["INT", {}], app).widget;
        return r;
      };

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);

        for (const widget of this.widgets) {
          if (widget.name == "width") {
            widget.value = message.width[0];
          }
          if (widget.name == "height") {
            widget.value = message.height[0];
          }
        }

        this.onResize?.(this.size);
      };
    }
  },
});

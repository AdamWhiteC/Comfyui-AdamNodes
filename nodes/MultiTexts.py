import os

class AdamMultiTextNodes:
    """
    Adam多行文本texts节点 - Adam Multi-line Text Node
    支持多行文本输入和合并输出
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "连接符/Connector": ("STRING", {"default": ", "}),
            }
        }
        
        # 添加10个文本输入框
        for i in range(1, 11):
            inputs["required"].update({
                f"文本{i}/Text{i}": ("STRING", {"default": ""}),  # 移除 multiline 参数
            })
            
        return inputs
    
    RETURN_TYPES = tuple(["STRING"]*11)
    RETURN_NAMES = (
        *[f"文本{i}/Text{i}" for i in range(1,11)],
        "合并文本/Combined"
    )
    FUNCTION = "process_texts"
    CATEGORY = "Adam/文本Text"
    
    def process_texts(self, **kwargs):
        # 处理10个文本行
        individual_outputs = []
        processed_lines = []
        
        for i in range(1, 11):
            text = kwargs[f"文本{i}/Text{i}"].strip()
            individual_outputs.append(text)
            if text:  # 仅保留非空文本
                processed_lines.append(text)
        
        # 生成合并文本
        connector = kwargs["连接符/Connector"]
        combined_text = connector.join(processed_lines)
        
        return (*individual_outputs, combined_text)
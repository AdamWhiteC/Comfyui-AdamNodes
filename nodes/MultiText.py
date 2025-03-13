import os
import re

class AdamMultiTextNode:
    """
    Adam多行文本texts节点 - Adam Multi-line Text Node
    支持多行文本输入，正则替换，全局前后缀，可扩展文本处理
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                # 控制参数组
                "定义开关/Definition Switch": ("BOOLEAN", {"default": True}),
                "正则开关/Regex Mode": ("BOOLEAN", {"default": False}),
                "连接符换行/Connector Newline": ("BOOLEAN", {"default": False}),
                "定义分隔符/Definition Separator": ("STRING", {"default": ""}),
                "全局前缀/Global Prefix": ("STRING", {"default": ""}),
                "全局后缀/Global Suffix": ("STRING", {"default": ""}),
                
                # 合并参数组
                "合并连接符1/Connector1": ("STRING", {"default": ", "}),
                "合并连接符2/Connector2": ("STRING", {"default": "\n"}),
                "合并连接符3/Connector3": ("STRING", {"default": " | "}),
                
                # 替换参数组
                "被替换文本/Replace Targets": ("STRING", {"default": ""}),
                "替换文本/Replacements": ("STRING", {"default": ""}),
            },
            "optional": {}  # 添加可选输入部分
        }
        
        # 第一阶段：添加所有定义和文本框到可选部分
        for i in range(1, 11):
            inputs["optional"].update({
                f"定义{i}/Definition{i}": ("STRING", {"default": f"文本{i}/Text{i}"}),
                f"文本{i}/Text{i}": ("STRING", {"default": "", "multiline": True}),
            })
            
        # 第二阶段：添加所有前缀到可选部分
        for i in range(1, 11):
            inputs["optional"][f"前缀{i}/Prefix{i}"] = ("STRING", {"default": ""})
            
        # 第三阶段：添加所有后缀到可选部分
        for i in range(1, 11):
            inputs["optional"][f"后缀{i}/Suffix{i}"] = ("STRING", {"default": ""})
            
        return inputs
    
    RETURN_TYPES = tuple(["STRING"]*13)
    RETURN_NAMES = (
        *[f"文本{i}/Text{i}" for i in range(1,11)],
        "合并文本1/Combined1",
        "合并文本2/Combined2",
        "合并文本3/Combined3"
    )
    FUNCTION = "process_texts"
    CATEGORY = "Adam/文本Text"
    
    def apply_replacements(self, text, replace_rules, use_regex):
        """应用替换规则到文本"""
        for target, replacement in replace_rules:
            if not target.strip():
                continue
            try:
                if use_regex:
                    text = re.sub(target.strip(), replacement.strip(), text, flags=re.MULTILINE)
                else:
                    text = text.replace(target.strip(), replacement.strip())
            except Exception as e:
                print(f"替换错误: {str(e)}")
        return text
    
    def process_texts(self, **kwargs):
        # 参数提取
        definition_switch = kwargs.get("定义开关/Definition Switch", True)
        use_regex = kwargs.get("正则开关/Regex Mode", False)
        connector_newline = kwargs.get("连接符换行/Connector Newline", False)
        definition_separator = kwargs.get("定义分隔符/Definition Separator", "")
        global_prefix = kwargs.get("全局前缀/Global Prefix", "")
        global_suffix = kwargs.get("全局后缀/Global Suffix", "")
        
        # 处理替换规则
        replace_targets = kwargs.get("被替换文本/Replace Targets", "")
        replacements = kwargs.get("替换文本/Replacements", "")
        replace_rules = list(zip(
            replace_targets.split("||") if replace_targets else [],
            replacements.split("||") if replacements else []
        ))
        
        # 处理10个文本行
        individual_outputs = []
        processed_lines = []
        
        for i in range(1, 11):
            # 获取组件（按新顺序），使用get方法提供默认值
            definition = kwargs.get(f"定义{i}/Definition{i}", f"文本{i}/Text{i}")
            raw_text = kwargs.get(f"文本{i}/Text{i}", "").strip()
            prefix = kwargs.get(f"前缀{i}/Prefix{i}", "")
            suffix = kwargs.get(f"后缀{i}/Suffix{i}", "")
            
            # 构建文本行
            components = []
            # 先添加单独前缀，再添加全局前缀
            if prefix:
                components.append(prefix)
            if global_prefix:
                components.append(global_prefix)
                
            if definition_switch and definition:
                components.append(definition)
                if definition_separator:  # 在定义后添加分隔符
                    components.append(definition_separator)
            if raw_text:
                components.append(raw_text)
                
            # 先添加全局后缀，再添加单独后缀
            if global_suffix:
                components.append(global_suffix)
            if suffix:
                components.append(suffix)
            
            # 应用替换规则
            processed_text = self.apply_replacements(
                text="".join(components).strip(),
                replace_rules=replace_rules,
                use_regex=use_regex
            )
            
            individual_outputs.append(processed_text)
            if raw_text:  # 仅保留有原始文本的行
                processed_lines.append(processed_text)
        
        # 生成合并文本
        connectors = [
            kwargs.get("合并连接符1/Connector1", ", "),
            kwargs.get("合并连接符2/Connector2", "\n"),
            kwargs.get("合并连接符3/Connector3", " | ")
        ]
        
        combined_texts = []
        for connector in connectors:
            # 如果启用了换行，在每个连接符后添加换行符
            actual_connector = connector + "\n" if connector_newline and connector != "\n" else connector
            merged = actual_connector.join(processed_lines)
            merged = self.apply_replacements(merged, replace_rules, use_regex)
            combined_texts.append(merged)
        
        return (*individual_outputs[:10], *combined_texts)
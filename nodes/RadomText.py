import random
import time
import uuid
import re

class AdamRandomizeText:
    # 添加类变量作为计数器
    execution_counter = 0
    # 添加上次执行时间记录
    last_execution_time = 0
    # 添加类变量存储最后一次生成的文本
    last_generated_text = ""
    # 添加类变量存储最后一次生成的单个文本
    last_generated_single_text = ""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "使用换行符/UseNewline": (["是", "否"], {"default": "是"}),
                "分隔符/Separator": ("STRING", {"default": ","}),
                "正则开关/RegexMode": ("BOOLEAN", {"default": False}),
                "被替换文本/ReplaceTargets": ("STRING", {"default": ""}),
                "替换文本/Replacements": ("STRING", {"default": ""}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    # 修改返回类型，添加单个文本输出
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("全部文本/AllText", "单个文本/SingleText",)
    FUNCTION = "RandomizeText"
    CATEGORY = "Adam/文本Text"
    OUTPUT_NODE = True
    
    # 添加IS_CHANGED方法，确保每次右键执行时都会重新计算
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 每次检查变化时更新时间戳，确保节点被视为已更改
        current_time = time.time()
        cls.last_execution_time = current_time
        return current_time
    
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
    
    def RandomizeText(self, text, unique_id=None, extra_pnginfo=None, **kwargs):
        # 获取参数值，使用kwargs字典获取中文参数名
        use_newline = kwargs.get("使用换行符/UseNewline", "是")
        separator = kwargs.get("分隔符/Separator", ",")
        regex_mode = kwargs.get("正则开关/RegexMode", False)
        replace_targets = kwargs.get("被替换文本/ReplaceTargets", "")
        replacements = kwargs.get("替换文本/Replacements", "")
        
        # 每次执行时递增计数器
        AdamRandomizeText.execution_counter += 1
        
        # 使用时间戳、随机UUID和计数器组合作为种子，确保每次执行都不同
        seed_value = time.time() + hash(str(uuid.uuid4())) + AdamRandomizeText.execution_counter
        random.seed(seed_value)
        
        # 根据use_newline选择分隔符
        actual_separator = "\n" if use_newline == "是" else separator
        
        # 使用分隔符拆分文本
        text_parts = text.split(actual_separator)
        # 过滤掉空字符串
        text_parts = [part for part in text_parts if part.strip()]
        # 随机打乱顺序
        random.shuffle(text_parts)
        
        # 获取第一个文本作为单个文本输出
        single_text = text_parts[0].strip() if text_parts else ""
        
        # 使用分隔符重新连接
        RandomizedText = actual_separator.join(text_parts)
        
        # 处理替换规则
        replace_rules = list(zip(
            replace_targets.split("||") if replace_targets else [],
            replacements.split("||") if replacements else []
        ))
        
        # 应用替换规则
        if replace_rules:
            RandomizedText = self.apply_replacements(
                text=RandomizedText,
                replace_rules=replace_rules,
                use_regex=regex_mode
            )
            # 同样对单个文本应用替换规则
            single_text = self.apply_replacements(
                text=single_text,
                replace_rules=replace_rules,
                use_regex=regex_mode
            )
        
        # 更新类变量存储最后一次生成的文本
        AdamRandomizeText.last_generated_text = RandomizedText
        AdamRandomizeText.last_generated_single_text = single_text
        
        # 更新节点UI显示
        if unique_id is not None and extra_pnginfo is not None:
            try:
                if not isinstance(extra_pnginfo, list):
                    print("Error: extra_pnginfo is not a list")
                elif not isinstance(extra_pnginfo[0], dict) or "workflow" not in extra_pnginfo[0]:
                    print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
                else:
                    workflow = extra_pnginfo[0]["workflow"]
                    node = next(
                        (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id)),
                        None,
                    )
                    if node:
                        # 直接设置widgets_values为生成的文本
                        node["widgets_values"] = [RandomizedText]
            except Exception as e:
                print(f"更新节点UI时出错: {str(e)}")
        
        # 返回结果
        return {"ui": {"text": RandomizedText}, "result": (RandomizedText, single_text)}
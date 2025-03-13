import re

class AdamTextRegexProcessor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True}),
                "regex_pattern": ("STRING", {"default": r"\w+"}),
                "replace_with": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_text"
    CATEGORY = "Adam/文本Text"

    def process_text(self, input_text, regex_pattern, replace_with):
        try:
            result = re.sub(regex_pattern, replace_with, input_text)
            return (result,)
        except re.error:
            return ("正则表达式错误",)

NODE_CLASS_MAPPINGS = {
    "AdamTextRegexProcessor": AdamTextRegexProcessor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdamTextRegexProcessor": "Adam文本正则处理器"
}
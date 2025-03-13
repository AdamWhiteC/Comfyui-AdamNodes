from .nodes.image_name_processor import AdamImageNameProcessor
from .nodes.text_regex_processor import AdamTextRegexProcessor
from .nodes.MultiText import AdamMultiTextNode
from .nodes.MultiTexts import AdamMultiTextNodes
from .nodes.RadomText import AdamRandomizeText
from .nodes.TextBox import AdamTextBox  # 新增导入

WEB_DIRECTORY = "js"
__all__ = ["NODE_CLASS_MAPPINGS"]

NODE_CLASS_MAPPINGS = {
    "AdamImageNameProcessor": AdamImageNameProcessor,
    "AdamTextRegexProcessor": AdamTextRegexProcessor,
    "MultiText": AdamMultiTextNode,
    "MultiTexts": AdamMultiTextNodes,
    "AdamRandomizeText": AdamRandomizeText,
    "AdamTextBox": AdamTextBox,  # 新增节点映射
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdamImageNameProcessor": "Adam的图像名称处理器",
    "TextRegexProcessor": "Adam文本正则处理器",
    "MultiText": "Adam多行文本Multi-line_Text",
    "MultiTexts": "Adam简易多行文本Multi-line_TextS",
    "AdamRandomizeText": "Adam文本随机化randomize_Text",
    "AdamTextBox": "Adam文本框TextBox",  # 新增显示名称
}
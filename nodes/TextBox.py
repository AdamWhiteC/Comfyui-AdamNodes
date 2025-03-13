class AdamTextBox:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "forceInput": False,
                        "print_to_screen": True,
                    },
                ),
                "use_passthrough使用传递": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "passthrough": (
                    "STRING",
                    {"default": "", "multiline": True, "forceInput": True},
                )
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "textbox"
    CATEGORY = "Adam/文本Text"

    def textbox(self, text="", use_passthrough使用传递=True, passthrough=""):
        if use_passthrough使用传递 and passthrough != "":
            text = passthrough
        return {"ui": {"text": text}, "result": (text,)}
import os

class AdamImageNameProcessor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_a_names": ("STRING", {"multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_names"
    CATEGORY = "Adam/图像image"

    def process_names(self, image_a_names):
        names = [name.strip() for name in image_a_names.split(',')]
        if not names:
            return ("",)
        
        common_prefix = os.path.commonprefix(names)
        if common_prefix.endswith('_'):
            common_prefix = common_prefix[:-1]
        
        return (common_prefix + ".jpg",)
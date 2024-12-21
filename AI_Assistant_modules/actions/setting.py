import os
import configparser
import gradio as gr
from PIL import Image

from AI_Assistant_modules.output_image_gui import OutputImage
from AI_Assistant_modules.prompt_analysis import PromptAnalysis
from utils.prompt_utils import execute_prompt, remove_duplicates
from utils.request_api import upscale_and_save_images

LANCZOS = (Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)

class Setting:
    def __init__(self, app_config):
        self.app_config = app_config
        self.input_image = None
        self.output = None
        self.default_negative_prompt = ""
        self.config_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "setting.ini"
        )
        self.load_config()

    def load_config(self):
        """設定ファイルを読み込む"""
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            if config.has_option('DEFAULT', 'output_dir'):
                self.app_config.output_dir = config.get('DEFAULT', 'output_dir')
            if config.has_option('DEFAULT', 'negative_prompt'):
                self.app_config.negative_prompt = config.get('DEFAULT', 'negative_prompt')
            else:
                self.app_config.negative_prompt = self.default_negative_prompt
            if config.has_option('DEFAULT', 'replace_prompt'):
                self.app_config.replace_prompt = config.get('DEFAULT', 'replace_prompt')
            else:
                self.app_config.replace_prompt = ""

    def save_config(self, output_dir, prompt_add, negative_prompt, replace_prompt):
        """設定を保存する"""
        try:
            normalized_path = self._validate_config(output_dir, prompt_add, negative_prompt, replace_prompt)
            
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')
            if 'DEFAULT' not in config:
                config['DEFAULT'] = {}
            
            config['DEFAULT']['output_dir'] = normalized_path
            config['DEFAULT']['prompt_add'] = prompt_add
            config['DEFAULT']['negative_prompt'] = negative_prompt
            config['DEFAULT']['replace_prompt'] = replace_prompt
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            
            if not os.path.exists(normalized_path):
                os.makedirs(normalized_path)
            
            self.app_config.output_dir = normalized_path
            self.app_config.negative_prompt = negative_prompt
            self.app_config.replace_prompt = replace_prompt
            return self.app_config.lang_util.get_text("result_word_ok")
        except PermissionError:
            return self.app_config.lang_util.get_text("permission_error")
        except Exception as e:
            return self.app_config.lang_util.get_text("general_error").format(str(e))

    def _validate_config(self, output_dir, prompt_add, negative_prompt, replace_prompt):
        if not output_dir:
            raise ValueError(self.app_config.lang_util.get_text("error_output_dir_required"))
        if not os.path.isabs(output_dir):
            try:
                return os.path.abspath(os.path.join(self.app_config.dpath, output_dir))
            except:
                raise ValueError(self.app_config.lang_util.get_text("error_invalid_path"))
        return output_dir

    def layout(self):
        """設定画面のレイアウトを構築する"""
        lang_util = self.app_config.lang_util
        
        config = configparser.ConfigParser()
        output_dir_value = ""
        negative_prompt_value = self.default_negative_prompt
        prompt_add_value = ""
        replace_prompt_value = ""
        
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            if config.has_option('DEFAULT', 'output_dir'):
                output_dir_value = config.get('DEFAULT', 'output_dir')
            if config.has_option('DEFAULT', 'negative_prompt'):
                negative_prompt_value = config.get('DEFAULT', 'negative_prompt')
            if config.has_option('DEFAULT', 'prompt_add'):
                prompt_add_value = config.get('DEFAULT', 'prompt_add')
            if config.has_option('DEFAULT', 'replace_prompt'):
                replace_prompt_value = config.get('DEFAULT', 'replace_prompt')
        
        with gr.Row() as self.block:
            with gr.Column():
                output_dir = gr.Textbox(
                    label=lang_util.get_text("output_destination"),
                    value=output_dir_value,
                    lines=1
                )
                prompt_add = gr.Textbox(
                    label=lang_util.get_text("prompt_add"),
                    value=prompt_add_value,
                    lines=3
                )
                negative_prompt = gr.Textbox(
                    label=lang_util.get_text("negative_prompt_set"),
                    value=negative_prompt_value,
                    lines=3
                )
                replace_prompt = gr.Textbox(
                    label=lang_util.get_text("replace_prompt"),
                    value=replace_prompt_value,
                    lines=3
                )
                save_btn = gr.Button(lang_util.get_text("save"))
                self.output = gr.Textbox(
                    label=lang_util.get_text("result"),
                    interactive=False
                )
                save_btn.click(
                    fn=self.save_config,
                    inputs=[output_dir, prompt_add, negative_prompt, replace_prompt],
                    outputs=[self.output]
                )
        return self.block
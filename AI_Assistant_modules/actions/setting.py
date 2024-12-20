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

    def save_config(self, output_dir):
        """出力ディレクトリの設定を保存する"""
        try:
            # パスの正規化
            normalized_path = os.path.normpath(output_dir)
            
            # 絶対パスに変換
            if not os.path.isabs(normalized_path):
                normalized_path = os.path.abspath(os.path.join(self.app_config.dpath, normalized_path))

            # 設定ファイルの処理
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')

            if 'DEFAULT' not in config:
                config['DEFAULT'] = {}
            config['DEFAULT']['output_dir'] = normalized_path

            # 設定の保存
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            # 出力ディレクトリの作成
            if not os.path.exists(normalized_path):
                os.makedirs(normalized_path)
            
            # アプリケーション設定の更新
            self.app_config.output_dir = normalized_path
            return "設定を保存しました"

        except PermissionError:
            return "ディレクトリへのアクセス権限がありません"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    def layout(self):
        """設定画面のレイアウトを構築する"""
        lang_util = self.app_config.lang_util
        
        # setting.iniから出力先を取得
        config = configparser.ConfigParser()
        output_dir_value = ""
        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            if config.has_option('DEFAULT', 'output_dir'):
                output_dir_value = config.get('DEFAULT', 'output_dir')
        
        # 設定が空の場合はプロジェクトルート直下のoutputを設定
        if not output_dir_value:
            output_dir_value = os.path.join(self.app_config.dpath, "output")
            # 設定を保存
            config['DEFAULT'] = {'output_dir': output_dir_value}
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        
        self.app_config.output_dir = output_dir_value
        
        with gr.Row() as self.block:
            with gr.Column():
                output_dir = gr.Textbox(
                    label=lang_util.get_text("output_destination"),
                    value=output_dir_value,
                    lines=1
                )
                save_btn = gr.Button(lang_util.get_text("save"))
                self.output = gr.Textbox(
                    label=lang_util.get_text("result"),
                    interactive=False
                )
                save_btn.click(
                    fn=self.save_config,
                    inputs=[output_dir],
                    outputs=[self.output]
                )
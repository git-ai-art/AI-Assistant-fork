import os
import configparser

import gradio as gr

from utils.prompt_utils import remove_color
from utils.tagger import modelLoad, analysis


class PromptAnalysis:
    def __init__(self, app_config, post_filter=True):
        self.app_config = app_config
        self.post_filter = post_filter
        self.model = None
        self.model_dir = os.path.join(app_config.dpath, 'models/tagger')
        
        # インスタンス変数の初期化
        self.prompt_add_tag = ""
        self.negative_prompt_text = ""  # negative_promptの値を保持する変数
        self.prompt = None
        self.negative_prompt = None  # gr.Textboxのインスタンスを保持
        self.replace_tags = {}  # 空の辞書として初期化
        
        # 設定ファイルの読み込み
        self.config_file = os.path.join(app_config.dpath, "setting.ini")
        self._load_config()
        self._load_replace_tags()  # replace_tagsの読み込みを追加

        # 出力ディレクトリの作成
        os.makedirs(os.path.dirname(self.app_config.output_dir), exist_ok=True)
        
        # prompt_add_tagの初期化
        self.prompt_add_tag = ""
        self._load_prompt_add_tag()

    def _load_config(self):
        """設定ファイルを読み込む"""
        try:
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')
                if config.has_option('DEFAULT', 'prompt_add'):
                    self.prompt_add_tag = config.get('DEFAULT', 'prompt_add')
                if config.has_option('DEFAULT', 'negative_prompt'):
                    self.negative_prompt_text = config.get('DEFAULT', 'negative_prompt')
        except configparser.ParsingError as e:
            print(f"設定ファイルのパースエラー: {e}")
        except Exception as e:
            print(f"設定ファイルの読み込みエラー: {e}")

    def _load_prompt_add_tag(self):
        """setting.iniからprompt_addを読み込む"""
        try:
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')
                if config.has_option('DEFAULT', 'prompt_add'):
                    self.prompt_add_tag = config.get('DEFAULT', 'prompt_add')
        except Exception as e:
            print(f"prompt_addの読み込みエラー: {e}")

    def _load_replace_tags(self):
        """setting.iniからreplace_promptを読み込んで辞書に変換"""
        try:
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')
                if config.has_option('DEFAULT', 'replace_prompt'):
                    replace_prompt = config.get('DEFAULT', 'replace_prompt')
                    # 行ごとに分割
                    lines = [line.strip() for line in replace_prompt.split('\n')]
                    self.replace_tags = {}
                    for line in lines:
                        if ':' in line:
                            key, value = map(str.strip, line.split(':', 1))
                            self.replace_tags[key] = value
        
        except Exception as e:
            print(f"replace_promptの読み込みエラー: {e}")

    def layout(self, lang_util, input_image):
        """UIレイアウトの構築"""
        self._load_config()
        
        with gr.Column():
            with gr.Row():
                self.prompt_analysis_button = gr.Button(
                    lang_util.get_text("analyze_prompt")
                )
            with gr.Row():
                self.prompt = gr.Textbox(
                    label=lang_util.get_text("prompt"), 
                    lines=3
                )
            with gr.Row():
                self.negative_prompt = gr.Textbox(
                    label=lang_util.get_text("negative_prompt"),
                    lines=3,
                    value=self.negative_prompt_text  # 保存された値を使用
                )

        self.prompt_analysis_button.click(
            self.process_prompt_analysis,
            inputs=[input_image],
            outputs=self.prompt
        )
        return [self.prompt, self.negative_prompt]

    def replace_specific_tags(self, tags_list):
        """特定のタグを置換または削除"""
        # 最新の設定を読み込み
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file, encoding='utf-8')
            if config.has_option('DEFAULT', 'replace_prompt'):
                replace_prompt = config.get('DEFAULT', 'replace_prompt')
                lines = [line.strip() for line in replace_prompt.split('\n')]
                self.replace_tags = {}
                for line in lines:
                    if ':' in line:
                        key, value = map(str.strip, line.split(':', 1))
                        self.replace_tags[key] = value
        except Exception as e:
            print(f"replace_promptの再読み込みエラー: {e}")

        # カンマで分割してクリーニング
        tags = [tag.strip() for tag in tags_list.split(',') if tag.strip()]
        
        # 置換処理
        replaced_tags = []
        for tag in tags:
            replaced = False
            for search, replace in self.replace_tags.items():
                if search in tag:  # 部分一致で検索
                    if replace:  # 置換値がある場合
                        # 元のタグ内の検索文字列を置換値で置き換え
                        new_tag = tag.replace(search, replace)
                        replaced_tags.append(new_tag)
                    replaced = True
                    break
            if not replaced:
                replaced_tags.append(tag)
        
        return ', '.join(dict.fromkeys(replaced_tags))

    def process_prompt_analysis(self, input_image_path):
        if self.model is None:
            self.model = modelLoad(self.model_dir)
        
        # 最新の設定を読み込み
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file, encoding='utf-8')  # force=Trueを削除
            self._load_config()
            self._load_replace_tags()
            self._load_prompt_add_tag()
        except Exception as e:
            print(f"設定の再読み込みエラー: {e}")
        
        tags = analysis(input_image_path, self.model_dir, self.model)
        tags_list = tags      
        if self.post_filter:
            tags_list = remove_color(tags)
        
        # タグの置換処理
        tags_list = self.replace_specific_tags(tags_list)
        
        return tags_list + ",\n" + self.prompt_add_tag

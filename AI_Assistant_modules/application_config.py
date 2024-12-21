import datetime
import os
import sys
import configparser

from gradio.utils import colab_check, is_zero_gpu_space


class ApplicationConfig:
    def __init__(self, lang_util, dpath):
        self.lang_util = lang_util
        self.fastapi_url = None
        self.dpath = dpath
        self.config_file = os.path.join(dpath, "setting.ini")
        self.output_dir = None
        self.load_config()
        self.exui = False

        device_mapping = {
            'darwin': 'mac',
            'linux': 'linux',
            'win32': 'windows'
        }
        if colab_check() or is_zero_gpu_space() or os.environ.get("GRADIO_CLOUD") == "1":
            self.device = "cloud"
        elif os.path.exists('/.dockerenv'):
            self.device = "docker"
        else:
            self.device = device_mapping.get(sys.platform.split()[0], 'unknown')

    def set_fastapi_url(self, url):
        self.fastapi_url = url

    def load_config(self):
        """設定ファイルから出力先を読み込む"""
        try:
            config = configparser.ConfigParser()
            if os.path.exists(self.config_file):
                # 既存の設定を保持
                current_output_dir = self.output_dir
                current_negative_prompt = getattr(self, 'negative_prompt', '')
                current_replace_prompt = getattr(self, 'replace_prompt', '')
                current_prompt_add = getattr(self, 'prompt_add', '')

                # 設定ファイルを読み込み
                config.read(self.config_file, encoding='utf-8')

                # 各設定を更新（存在しない場合は既存の値を維持）
                self.output_dir = config.get('DEFAULT', 'output_dir', fallback=current_output_dir)
                self.negative_prompt = config.get('DEFAULT', 'negative_prompt', fallback=current_negative_prompt)
                self.replace_prompt = config.get('DEFAULT', 'replace_prompt', fallback=current_replace_prompt)
                self.prompt_add = config.get('DEFAULT', 'prompt_add', fallback=current_prompt_add)

            if not self.output_dir:
                self.output_dir = os.path.join(self.dpath, "output")

        except configparser.ParsingError as e:
            print(f"設定ファイルのパースエラー: {e}")
            if not hasattr(self, 'output_dir') or not self.output_dir:
                self.output_dir = os.path.join(self.dpath, "output")
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")
            if not hasattr(self, 'output_dir') or not self.output_dir:
                self.output_dir = os.path.join(self.dpath, "output")

    def make_output_path(self, filename=None):
        """出力パスを生成する"""
        if filename is None:
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # 設定の再読み込み
        self.load_config()
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return os.path.join(self.output_dir, filename + ".png")

[日本語](README.md) | [EN](README_en.md) | [中文](README_zh_CN.md)

# AI-Assistant-fork
[tori29umai](https://github.com/tori29umai0123)氏の[AI-Assistant](https://github.com/tori29umai0123/AI-Assistant)に機能追加を実施したものとなります。

## 追加機能(fork-V5.1)
### 設定タブの追加
![01](https://github.com/user-attachments/assets/deaf5918-ba33-4b98-9a39-c82113284b9c)
以下の機能が利用可能です。

- **出力先フォルダの変更**  
  デフォルトはプロジェクトフォルダ配下outputフォルダとなります。

- **追加プロンプト**  
  プロンプト分析後、末尾に改行後、入力したタブを追加します。

- **ネガティブプロンプト**  
  デフォルトで設定されるネガティブプロンプトを変更します(再起動後反映)。

- **置換・削除プロンプト**  
  プロンプト分析後、対象のプロンプトを置換または削除します。
  以下の形式で入力します。タグ内の部分一致も可能です(red⇒blackに変更等)

```
source_tag1:target_tag1
source_tag2:target_tag2
source_tag3:target_tag3
remove_tag1:
remove_tag2:
remove_tag3:
```

## 開発中機能(fork-V5.2)
- モデル選択機能
- (オプション)VPrev系モデル対応
- CFGスケール設定機能
- 生成SEED値表示および固定機能

## 起動方法
- pyファイルへの改修が頻繁に入るため、現在はPythonでの起動を想定しています。  
  (tori29umai氏のページに記載されているexeファイル作成方法でおそらく作成は可能です）

- コマンドプロンプトまたはPowerShellにてGitHubからプロジェクトをcloneしてください。

```
cd (インストールフォルダ)
git clone https://github.com/git-ai-art/AI-Assistant-fork
```

- 以下を実行し、必要なファイルをダウンロードしてください。

```
AI_Assistant_model_DL.cmd
```

- 以下を実行し、環境のビルドを実行してください。

```
AI_Assistant_install.ps1
```

- 次回以降の起動時は以下を実行してください。

```
cd (インストールフォルダ)
python AI_Assistant.py --nowebui --xformers --skip-python-version-check --skip-torch-cuda-test --lang=jp
```

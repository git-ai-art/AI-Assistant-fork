[Japanese](README.md) | [EN](README_en.md) | [Chinese](README_zh_CN.md)

# AI-Assistant-fork
This is a modified version of [AI-Assistant](https://github.com/tori29umai0123/AI-Assistant) by [tori29umai](https://github.com/tori29umai0123) with added features.

## Additional Features (fork-V5.1)
### Added Settings Tab
![01](https://github.com/user-attachments/assets/deaf5918-ba33-4b98-9a39-c82113284b9c)
The following features are available:

- **Change Output Folder**  
  The default is the `output` folder under the project directory.

- **Additional Prompt**  
  After prompt analysis, a newline followed by the entered tab will be added to the end.

- **Negative Prompt**  
  The default negative prompt can be modified (applied after restarting).

- **Replace/Delete Prompt**  
  After prompt analysis, the target prompt can be replaced or deleted.
  Enter the following format. Partial matches within tags are also possible (e.g., changing `red` to `black`).

```
source_tag1:target_tag1
source_tag2:target_tag2
source_tag3:target_tag3
remove_tag1:
remove_tag2:
remove_tag3:
```

## Features Under Development (fork-V5.2)
- Model selection feature
- (Optional) Support for VPrev models
- CFG scale adjustment feature
- Display and lock SEED values for generation

## How to Launch
- Since modifications to `.py` files are frequent, the current assumption is to launch using Python.  
  (It is likely possible to create an `.exe` file using the method described on [tori29umai's page](https://github.com/tori29umai0123/AI-Assistant))

- Clone the project from GitHub using Command Prompt or PowerShell.

```
cd (installation folder)
git clone https://github.com/git-ai-art/AI-Assistant-fork
```

- Run the following command to download the necessary files.

```
AI_Assistant_model_DL.cmd
```

- Run the following command to build the environment.

```
AI_Assistant_install.ps1
```

- For subsequent launches, execute the following command:

```
cd (installation folder)
python AI_Assistant.py --nowebui --xformers --skip-python-version-check --skip-torch-cuda-test --lang=en
```

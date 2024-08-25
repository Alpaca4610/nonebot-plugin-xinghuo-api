<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-xinghuo-api
</div>

# 介绍
- 本插件是适配科大讯飞星火大模型官方API的聊天机器人插件，同时具有上下文记忆回复功能。已适配版本：Ultra，Max，Pro，Pro-128K，V2.0，Lite。
- 当前版本可能会与LittlePaimon机器人冲突
# 安装

* 手动安装
  ```
  git clone https://github.com/Alpaca4610/nonebot-plugin-xinghuo-api.git
  ```

  下载完成后在bot项目的pyproject.toml文件手动添加插件：

  ```
  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-xinghuo-api"]
  ```
* 使用 pip
  ```
  pip install nonebot-plugin-xinghuo-api
  ```

# 配置文件

必选内容: 在Bot根目录下的.env文件中填入科大讯飞提供的API调用鉴权信息：

```
xinghuo_app_id = xxxxxxxx
xinghuo_api_secret = xxxxxxxx
xinghuo_api_key = xxxxxxxx
```

可选内容：
```
xinghuo_enable_private_chat = True   # 私聊开关，默认开启，改为False关闭
xinghuo_api_version = ""    #星火大模型的版本，默认为免费的Lite模型，可选填：Ultra，Max，Pro，Pro-128K，V2.0，Lite
```

# 使用方法

- xh 获取回复，没有上下文回复的能力
- XH 获取回复，具有上下文回复的能力
- xh_clear 清除当前用户的聊天记录

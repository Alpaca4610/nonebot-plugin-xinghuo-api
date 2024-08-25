from pydantic import Extra, BaseModel
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    xinghuo_app_id: Optional[str] = ""
    xinghuo_api_secret: Optional[str] = ""
    xinghuo_api_key: Optional[str] = ""

    xinghuo_enable_private_chat: bool = True # 私聊开关，默认开启，改为False关闭
    xinghuo_group_public: bool = False  # 群聊是否开启公共会话
    xinghuo_api_version: str = "Lite" #星火大模型的版本，选填：Ultra，Max，Pro，Pro-128K，V2.0，Lite


class ConfigError(Exception):
    pass

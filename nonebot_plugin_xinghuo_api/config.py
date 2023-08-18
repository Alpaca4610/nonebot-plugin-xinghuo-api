from pydantic import Extra, BaseModel
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    xinghuo_app_id: Optional[str] = ""
    xinghuo_api_secret: Optional[str] = ""
    xinghuo_api_key: Optional[str] = ""

    xinghuo_enable_private_chat: bool = True
    xinghuo_group_public: bool = False  # 群聊是否开启公共会话
    xinghuo_api_v2: bool = False #是否使用星火大模型V2.0


class ConfigError(Exception):
    pass

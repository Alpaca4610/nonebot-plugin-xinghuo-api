from pydantic import Extra, BaseModel
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    xinghuo_app_id: Optional[str] = ""
    xinghuo_api_secret: Optional[str] = ""
    xinghuo_api_key: Optional[str] = ""

    xinghuo_enable_private_chat: bool = True # 私聊开关，默认开启，改为False关闭
    xinghuo_group_public: bool = False  # 群聊是否开启公共会话
    xinghuo_api_version: str = "v2" #星火大模型的版本，默认为v1.5。使用2.0版本请填入v2，使用3.0版本请填入v3。使用助手API请输入助手id，在https://xinghuo.xfyun.cn/botcenter/createbot获取


class ConfigError(Exception):
    pass

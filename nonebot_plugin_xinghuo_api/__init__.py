import random
import string
import nonebot
import asyncio

from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from .config import Config, ConfigError

from . import SparkApi

__plugin_meta__ = PluginMetadata(
    name="科大讯飞星火大模型聊天",
    description="Nonebot框架下的科大讯飞星火大模型聊天插件,已适配V2.0版API",
    usage=
    '''
    直接@机器人进行问答时，机器人没有上下文回复的能力
    xh 使用该命令进行问答时，机器人具有上下文回复的能力
    xh_clear 清除当前用户的聊天记录
    ''',
    config=Config,
    extra={},
    type="application",
    homepage="https://github.com/Alpaca4610/nonebot-plugin-xinghuo-api",
    supported_adapters={"~onebot.v11"}
)

# 配置导入
plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())

if not plugin_config.xinghuo_app_id or not plugin_config.xinghuo_app_id or not plugin_config.xinghuo_api_key:
    raise ConfigError("请设置星火大模型API信息")

appid = plugin_config.xinghuo_app_id
api_secret = plugin_config.xinghuo_api_secret
api_key = plugin_config.xinghuo_api_key

if len(plugin_config.xinghuo_api_version) == 2:  # v1 v3 v3
    API_URL = "ws://spark-api.xf-yun.com/" + plugin_config.xinghuo_api_version + ".1/chat"
    domain = "general" + plugin_config.xinghuo_api_version.replace("v1", "")
else:  # assistant_id
    API_URL = "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/" + plugin_config.xinghuo_api_version
    domain = "generalv2"

public = plugin_config.xinghuo_group_public
session = {}

# 带上下文的聊天
chat_record = on_command("xh", block=False, priority=1)

# 不带上下文的聊天
chat_request = on_command("", rule=to_me(), block=False, priority=1)

# 清除历史记录
clear_request = on_command("xh_clear", block=True, priority=1)


# 带记忆的聊天
@chat_record.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    # 若未开启私聊模式则检测到私聊就结束
    if isinstance(event, PrivateMessageEvent) and not plugin_config.xinghuo_enable_private_chat:
        chat_record.finish("对不起，私聊暂不支持此功能。")

    # 检测是否填写 API key
    if appid == "" or api_secret == "" or api_key == "":
        await chat_record.finish(MessageSegment.text("请先配置星火大模型API信息"), at_sender=True)

    # 提取提问内容
    content = msg.extract_plain_text()
    if content == "" or content is None:
        await chat_record.finish(MessageSegment.text("内容不能为空！"), at_sender=True)

    await chat_record.send(MessageSegment.text("星火大模型正在思考中......"))

    # 创建会话ID
    session_id = create_session_id(event)

    sid = generate_random_string(16)

    # 初始化保存空间
    if session_id not in session:
        session[session_id] = []

    # 开始请求
    try:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, getRes, session[session_id], content, sid)
    except Exception as error:
        await chat_record.finish(str(error), at_sender=True)
    await chat_record.finish(MessageSegment.text(res), at_sender=True)


# 不带记忆的对话
@chat_request.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent) and not plugin_config.xinghuo_enable_private_chat:
        chat_record.finish("对不起，私聊暂不支持此功能。")

    content = msg.extract_plain_text()
    if content == "" or content is None:
        await chat_request.finish(MessageSegment.text("内容不能为空！"))

    await chat_request.send(MessageSegment.text("星火大模型正在思考中......"))

    sid = generate_random_string(16)

    try:
        temp = []
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, getRes, temp, content, sid)
    except Exception as error:
        await chat_request.finish(str(error))
    await chat_request.finish(MessageSegment.text(res), at_sender=True)


@clear_request.handle()
async def _(event: MessageEvent):
    del session[create_session_id(event)]
    await clear_request.finish(MessageSegment.text("成功清除历史记录！"), at_sender=True)


# 生成随机字符串
def generate_random_string(length=16):
    # 生成数字和字母字符集
    characters = string.digits + string.ascii_letters
    # 生成随机字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# 根据消息类型创建会话id
def create_session_id(event):
    if isinstance(event, PrivateMessageEvent):
        session_id = f"Private_{event.user_id}"
    elif public:
        session_id = event.get_session_id().replace(f"{event.user_id}", "Public")
    else:
        session_id = event.get_session_id()
    return session_id


def getRes(history, content, sid):
    history = checklen(getText("user", content, history))
    SparkApi.answer[sid] = ""
    SparkApi.main(appid, api_key, api_secret, API_URL, domain, history, sid)
    getText("assistant", SparkApi.answer[sid], history)
    ans = SparkApi.answer[sid]
    del SparkApi.answer[sid]
    return ans


def getText(role, content, text):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

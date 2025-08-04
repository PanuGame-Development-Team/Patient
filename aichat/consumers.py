from jieba import lcut
from ollama import AsyncClient
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from record.models import Record
from core.constants import *
from core.models import Machine
from Patient.settings import OLLAMA_MODEL
from django.db.models import Q
from json import dumps
class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        if not OLLAMA_MODEL:
            await self.close(4000,"该服务器没有提供AI模型，无法启动。")
    async def disconnect(self,*args):
        ...
    async def receive(self,text_data):
        # check access
        collections = await self.search(text_data)
        await self.send("json-references: " + await self.gen_references(collections))
        prompt = await self.gen_prompt(collections,text_data)
        res = await AsyncClient().generate(OLLAMA_MODEL,prompt,stream=True)
        async for chunk in res:
            await self.send(chunk.response)
    @database_sync_to_async
    def search(self,text_data):
        keywords = lcut(text_data)
        try:
            q = Q()
            for keyword in keywords:
                q |= Q(errcode__contains=keyword)|Q(title__contains=keyword)|Q(machine__name__contains=keyword)|Q(detail__contains=keyword)
            result = Record.objects.filter(q).all()
            return result
        except:
            return []
    @database_sync_to_async
    def gen_prompt(self,collections,text_data):
        machines = map(lambda x:x.name,Machine.objects.all())
        prompt = f"这个是设备的精确名称，务必仔细区分，列表中的设备无相互关联：{machines}\n"
        prompt += "以下是在日志数据库中搜索的结果，错误代码与现象没有关联：\n"
        for i in range(len(collections)):
            prompt += f"""{i+1}.{collections[i].title} 错误代码：{collections[i].errcode} 关联设备：{collections[i].machine.name}
    问题描述：'''{collections[i].detail}'''
    解决方案：'''{collections[i].solution}'''

"""
        prompt += f"请根据以上材料，去除与问题无关的设备，只输出匹配度高的几条解决方案。问题为：{text_data}"
        return prompt
    @database_sync_to_async
    def gen_references(self,collections):
        ls = []
        for i in collections:
            ls.append(i.tojson())
        return dumps(ls)
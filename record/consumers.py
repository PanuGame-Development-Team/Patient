import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Record
from core.models import fetch
from core.constants import *
from user.models import check_access
from .lib import *

class RecordConsumer(AsyncWebsocketConsumer):
    type = None
    id = None
    dbobject = None
    filter = [None,None,None,None]
    async def connect(self):
        await self.accept()
    async def disconnect(self,*args):
        ...
    async def receive(self,text_data):
        data = json.loads(text_data)
        if data.get("type"):
            self.type = data.get("type")
            self.id = data.get("id")
            await self.loaddbobj()
        lowestid = data.get("lowestid",2147483647)
        if data.get("filter"):
            self.filter = data.get("filter",[None,None,None,None])
        user = self.scope['user']
        record = await self.search(user,lowestid)
        if record:
            await self.send(json.dumps({"status":200,"position":"down",**record}))
        else:
            await self.send(json.dumps({"status":403}))
    @database_sync_to_async
    def search(self,user,lowestid):
        if not check_access(user,**{self.type:self.dbobject}) & ACCESS["READ"]:
            return {"status":403}
        try:
            q = Record.objects.filter(id__lt=lowestid)
            q = place_filter(q,self.type,self.dbobject)
            q = search_filter(q,*self.filter)
            return q.order_by("-id").first().tojson()
        except:
            return {"status":404}
    @database_sync_to_async
    def loaddbobj(self):
        self.dbobject = fetch(self.type,self.id)
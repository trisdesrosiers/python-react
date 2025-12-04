import json
import asyncio
import psycopg2
import psycopg2.extensions
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from decouple import config


class DatabaseChangesConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer that sends database change notifications to clients."""
    
    async def connect(self):
        print(f"WebSocket: Connection attempt from {self.scope.get('client', 'unknown')}")
        self.group_name = "db_changes"
        
        try:
            await self.accept()
            print("WebSocket: Connection accepted")
            
            # Add to group after accepting
            if self.channel_layer:
                await self.channel_layer.group_add(
                    self.group_name,
                    self.channel_name
                )
                print("WebSocket: Added to group")
            
            # Send confirmation message
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'Connected to real-time updates'
            }))
            print("WebSocket: Confirmation sent")
            
        except Exception as e:
            print(f"WebSocket: Error in connect - {e}")
            import traceback
            traceback.print_exc()
    
    async def disconnect(self, close_code):
        print(f"WebSocket: Disconnected with code {close_code}")
        try:
            if self.channel_layer and hasattr(self, 'group_name'):
                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name
                )
        except Exception as e:
            print(f"WebSocket: Error in disconnect - {e}")
    
    async def receive(self, text_data):
        """Handle incoming messages from WebSocket."""
        try:
            data = json.loads(text_data)
            print(f"WebSocket: Received message - {data}")
            if data.get('type') == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
        except Exception as e:
            print(f"WebSocket: Error in receive - {e}")
    
    async def db_change(self, event):
        """Handle database change events and send to WebSocket."""
        try:
            await self.send(text_data=json.dumps({
                'type': 'db_change',
                'table': event.get('table'),
                'operation': event.get('operation'),
                'data': event.get('data')
            }))
        except Exception as e:
            print(f"WebSocket: Error in db_change - {e}")


class PostgreSQLListener:
    """
    Listens for PostgreSQL NOTIFY events and broadcasts to WebSocket clients.
    """
    
    def __init__(self):
        self.conn = None
        self.running = False
    
    def get_connection(self):
        """Create a new PostgreSQL connection for LISTEN."""
        conn = psycopg2.connect(
            host="postgres",
            user=config('PSQL_DB_USER'),
            password=config('PSQL_DB_PASSWORD'),
            database="project1"
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    
    async def start(self):
        """Start listening for PostgreSQL notifications."""
        self.running = True
        
        # Wait a bit for Django to fully initialize
        await asyncio.sleep(2)
        
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            print("PostgreSQL Listener: No channel layer available")
            return
        
        print("PostgreSQL Listener: Starting...")
        
        while self.running:
            try:
                self.conn = await sync_to_async(self.get_connection)()
                cursor = self.conn.cursor()
                await sync_to_async(cursor.execute)("LISTEN db_changes;")
                print("PostgreSQL Listener: Listening for db_changes")
                
                while self.running:
                    await sync_to_async(self._wait_for_notify)()
                    
                    while self.conn.notifies:
                        notify = self.conn.notifies.pop(0)
                        print(f"PostgreSQL Listener: Notification - {notify.payload[:100]}...")
                        
                        try:
                            payload = json.loads(notify.payload)
                            await channel_layer.group_send(
                                "db_changes",
                                {
                                    "type": "db_change",
                                    "table": payload.get("table"),
                                    "operation": payload.get("operation"),
                                    "data": payload.get("data")
                                }
                            )
                        except json.JSONDecodeError as e:
                            print(f"PostgreSQL Listener: Invalid JSON - {e}")
                            
            except Exception as e:
                print(f"PostgreSQL Listener: Error - {e}")
                if self.conn:
                    try:
                        self.conn.close()
                    except:
                        pass
                await asyncio.sleep(5)
    
    def _wait_for_notify(self):
        """Wait for notification with timeout."""
        import select
        if self.conn:
            select.select([self.conn], [], [], 1.0)
            self.conn.poll()
    
    def stop(self):
        """Stop the listener."""
        self.running = False
        if self.conn:
            try:
                self.conn.close()
            except:
                pass


pg_listener = PostgreSQLListener()


async def start_pg_listener():
    """Start the PostgreSQL listener as a background task."""
    try:
        await pg_listener.start()
    except Exception as e:
        print(f"PostgreSQL Listener: Failed to start - {e}")

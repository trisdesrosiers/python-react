from django.apps import AppConfig
import asyncio
import threading


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """Start the PostgreSQL listener when Django is ready."""
        import os
        
        # Only start listener in the main process (not in migrate/makemigrations)
        if os.environ.get('RUN_MAIN') == 'true' or os.environ.get('DAPHNE_RUNNING'):
            self._start_pg_listener()
    
    def _start_pg_listener(self):
        """Start PostgreSQL listener in a background thread with its own event loop."""
        def run_listener():
            from api.consumers import start_pg_listener
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(start_pg_listener())
            except Exception as e:
                print(f"PostgreSQL Listener thread error: {e}")
            finally:
                loop.close()
        
        listener_thread = threading.Thread(target=run_listener, daemon=True)
        listener_thread.start()

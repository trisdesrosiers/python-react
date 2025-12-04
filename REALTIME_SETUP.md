# Real-Time Updates Setup Guide

PostgreSQL LISTEN/NOTIFY + Django Channels implementation for real-time database change notifications.

---

## Architecture Overview

```
PostgreSQL (triggers) → Django (listener + websocket) → React (hook)
```

**How it works:** Database triggers detect changes → PostgreSQL sends notification → Django listener catches it → Broadcasts to all connected WebSocket clients → React updates UI instantly.

---

## Implementation Steps

### 1. Backend Dependencies
- Added `channels` and `daphne` packages to requirements.txt
- Channels handles WebSocket connections
- Daphne is the ASGI server (replaces runserver for WebSocket support)

### 2. Django Configuration
- Added `daphne` and `channels` to INSTALLED_APPS in settings.py
- Configured ASGI_APPLICATION and CHANNEL_LAYERS (using InMemoryChannelLayer)
- Updated asgi.py to route HTTP and WebSocket protocols separately

### 3. WebSocket Consumer
- Created `consumers.py` with DatabaseChangesConsumer class
- Handles WebSocket connect/disconnect/message events
- Groups all clients into "db_changes" broadcast group

### 4. PostgreSQL Listener
- Created PostgreSQLListener class that maintains persistent DB connection
- Executes `LISTEN db_changes` to subscribe to PostgreSQL notifications
- When notification received, broadcasts to all WebSocket clients
- Auto-reconnects on connection failure

### 5. Listener Startup
- Modified `apps.py` to start PostgreSQL listener when Django boots
- Runs in background thread with its own event loop
- Only starts in main process (not during migrations)

### 6. Database Triggers
- Created `notify_table_change()` PostgreSQL function
- Added triggers on profiles, registrations, roles tables
- Triggers fire on INSERT, UPDATE, DELETE operations
- Sends JSON payload with table name, operation type, and row data

### 7. WebSocket Routing
- Created `routing.py` with WebSocket URL pattern
- Endpoint: `/ws/changes/`

### 8. Frontend WebSocket Hook
- Created `useWebSocket.js` with two hooks:
  - `useWebSocket`: Generic WebSocket connection with auto-reconnect
  - `useTableChanges`: Filters messages by specific table names
- Uses refs for callbacks to prevent React re-render reconnection loops
- Exponential backoff for reconnection attempts

### 9. Docker Configuration
- Changed backend command from `runserver` to `daphne`
- Added `DAPHNE_RUNNING` environment variable

### 10. Nginx Configuration
- `/ws/` route proxies to backend for real-time WebSocket
- `/ws` route (exact match) proxies to frontend for React HMR
- Both require WebSocket upgrade headers

---

## Files Modified/Created

| Location | File | Purpose |
|----------|------|---------|
| Backend | `requirements.txt` | Added channels, daphne |
| Backend | `project1/settings.py` | Channels config |
| Backend | `project1/asgi.py` | Protocol routing |
| Backend | `api/consumers.py` | WebSocket + PG listener |
| Backend | `api/routing.py` | WebSocket URLs |
| Backend | `api/apps.py` | Listener startup |
| Database | `psql/scripts/01_init.sql` | Schema + trigger definitions |
| Database | `psql/scripts/02_triggers.sql` | Standalone trigger script |
| Frontend | `src/hooks/useWebSocket.js` | React WebSocket hooks |
| Root | `docker-compose.yml` | Daphne server config |
| Root | `nginx.conf` | WebSocket proxy routes |

---

## Adding Real-Time to New Tables

1. Add trigger in `01_init.sql` or run `02_triggers.sql`:
   - Create trigger on your table referencing `notify_table_change()` function

2. In React component:
   - Import `useTableChanges` hook
   - Call with table name and callback function

---

## Troubleshooting

### WebSocket connects then immediately disconnects
- **Cause:** React useEffect dependency loop causing reconnections
- **Fix:** Use refs for callback functions in useWebSocket hook to prevent re-renders from triggering reconnects

### WebSocket connection to `/ws` failed (React HMR)
- **Cause:** Nginx not proxying React dev server WebSocket
- **Fix:** Add exact match route in nginx.conf:
  ```
  location = /ws { proxy_pass http://frontend:3002/ws; ... }
  ```
- **Note:** This is separate from `/ws/` (our real-time) vs `/ws` (React HMR)

### EACCES permission denied for node_modules/.cache
- **Cause:** Docker user permissions mismatch
- **Fix:** Run as root to create directory:
  ```bash
  docker exec -u root <frontend-container> sh -c "mkdir -p /app/node_modules/.cache && chmod -R 777 /app/node_modules/.cache"
  ```

### PostgreSQL Listener not receiving notifications
- **Cause:** Triggers not applied to database
- **Fix:** Run the trigger script on existing database:
  ```bash
  docker exec -i project1-postgres psql -U postgres -d project1 < psql/scripts/02_triggers.sql
  ```

---

## Key Points

- **No Redis required** - Uses PostgreSQL's built-in pub/sub
- **Catches ALL changes** - Even from raw SQL, scripts, or external tools
- **Auto-reconnect** - Both backend listener and frontend WebSocket
- **Scalable** - Add triggers to any table as needed
- **Lightweight** - Minimal dependencies, no external message broker
- **HTTPS not required** - Works on HTTP for local development

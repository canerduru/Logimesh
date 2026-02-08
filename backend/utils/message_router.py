import os
import logging
import json
from typing import Callable, Dict, Any, List
from supabase import create_client, Client
from dotenv import load_dotenv

try:
    from backend.models.message import AgentMessage, MessageType
except ImportError:
    from models.message import AgentMessage, MessageType

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client if not in dry run
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if not DRY_RUN and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

# In-memory message bus for DRY_RUN mode
_local_subscribers: Dict[str, List[Callable]] = {}

def validate_message(message_data: Dict[str, Any]) -> AgentMessage:
    """Validates a message dictionary against the AgentMessage schema."""
    try:
        return AgentMessage(**message_data)
    except Exception as e:
        logger.error(f"Message validation failed: {e}")
        raise ValueError(f"Invalid message format: {e}")

async def send_message(message: AgentMessage) -> str:
    """
    Sends a message to the network.
    In DRY_RUN mode, simulates sending via local bus.
    In PRODUCTION mode, writes to Supabase 'agent_messages' table.
    """
    message_dict = message.model_dump()

    logger.info(f"[MESSAGE SENT] {message.sender_agent_type} -> {message.receiver_agent_type} | {message.message_type}")

    if DRY_RUN:
        # Simulate network latency or direct delivery
        logger.info(f"[DRY RUN] Message payload: {json.dumps(message_dict, indent=2)}")

        # Deliver to local subscribers
        receiver_type = message.receiver_agent_type
        if receiver_type in _local_subscribers:
            for callback in _local_subscribers[receiver_type]:
                try:
                    await callback(message_dict)
                except Exception as e:
                    logger.error(f"Error in local subscriber callback: {e}")

        # Also broadcast to "ALL" if applicable
        if "ALL" in _local_subscribers:
             for callback in _local_subscribers["ALL"]:
                try:
                    await callback(message_dict)
                except Exception as e:
                    logger.error(f"Error in global subscriber callback: {e}")

        return message.id

    # Production Mode: Write to Supabase
    if not supabase:
        logger.error("Supabase client not initialized. Cannot send message.")
        return None

    try:
        response = supabase.table("agent_messages").insert({
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "sender_agent_type": message.sender_agent_type,
            "receiver_agent_type": message.receiver_agent_type,
            "message_type": message.message_type,
            "payload_json": message.payload,
            "conversation_id": message.conversation_id,
            "timestamp": message.timestamp
        }).execute()
        return message.id
    except Exception as e:
        logger.error(f"Failed to write message to Supabase: {e}")
        return None

def subscribe_to_messages(agent_type: str, callback: Callable):
    """
    Subscribes an agent to messages addressed to it.
    Callback should be an async function taking a message dict.
    """
    if agent_type not in _local_subscribers:
        _local_subscribers[agent_type] = []
    _local_subscribers[agent_type].append(callback)
    logger.info(f"Agent '{agent_type}' subscribed to messages.")

    if not DRY_RUN and supabase:
        # TODO: Implement Supabase Realtime subscription here
        # This requires using the realtime-py client or similar which is integrated in supabase-py
        # For now, we rely on polling or external triggers in production,
        # as implementing full Realtime loop in this script is complex.
        pass

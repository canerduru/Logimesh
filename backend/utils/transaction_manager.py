import os
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

try:
    from backend.models.core import Transaction
    from backend.models.message import AgentMessage, MessageType
except ImportError:
    from models.core import Transaction
    from models.message import AgentMessage, MessageType

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize Supabase client if not in dry run
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not DRY_RUN and SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

async def create_transaction(load_id: str, fleet_id: str, final_price: float,
                           carrier_id: str, shipper_id: str) -> Optional[str]:
    """
    Creates a new transaction record for a matched load.
    """
    logger.info(f"Creating transaction: Load {load_id} -> Fleet {fleet_id} @ {final_price}")

    transaction = Transaction(
        load_id=load_id,
        fleet_id=fleet_id,
        amount=final_price,
        carrier_company_id=carrier_id,
        shipper_company_id=shipper_id,
        status="PENDING",
        created_at=datetime.now()
    )

    if DRY_RUN:
        logger.info(f"[DRY RUN] Transaction created: {transaction.id}")
        return transaction.id

    try:
        data = supabase.table("transactions").insert({
            "id": transaction.id,
            "load_id": transaction.load_id,
            "fleet_id": transaction.fleet_id,
            "carrier_company_id": transaction.carrier_company_id,
            "shipper_company_id": transaction.shipper_company_id,
            "final_price": transaction.amount,
            "status": "PENDING"
        }).execute()
        return transaction.id
    except Exception as e:
        logger.error(f"Failed to create transaction: {e}")
        return None

async def finalize_transaction(transaction_id: str, success: bool = True):
    """
    Updates transaction status and related entities (load, fleet).
    """
    status = "COMPLETED" if success else "FAILED"
    logger.info(f"Finalizing transaction {transaction_id} -> {status}")

    if DRY_RUN:
        logger.info(f"[DRY RUN] Transaction {transaction_id} marked as {status}")
        # Mock updating Load -> MATCHED
        logger.info(f"[DRY RUN] Load associated with {transaction_id} marked MATCHED")
        # Mock updating Fleet -> ASSIGNED
        logger.info(f"[DRY RUN] Fleet associated with {transaction_id} marked ASSIGNED")
        return

    try:
        # Update Transaction
        supabase.table("transactions").update({"status": status}).eq("id", transaction_id).execute()

        if success:
            # Fetch transaction to get load_id and fleet_id
            tx_data = supabase.table("transactions").select("*").eq("id", transaction_id).single().execute()
            if tx_data and tx_data.data:
                load_id = tx_data.data['load_id']
                fleet_id = tx_data.data['fleet_id']

                # Update Load
                supabase.table("loads").update({"status": "MATCHED"}).eq("id", load_id).execute()
                # Update Fleet
                supabase.table("fleets").update({"status": "ASSIGNED"}).eq("id", fleet_id).execute()

    except Exception as e:
        logger.error(f"Failed to finalize transaction: {e}")

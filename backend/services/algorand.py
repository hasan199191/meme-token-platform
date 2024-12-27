from algosdk import account, mnemonic
from algosdk.v2client import algod, indexer
import os
from collections import defaultdict
import logging
from datetime import datetime

class AlgorandService:
    def __init__(self):
        self.algod_address = "https://mainnet-api.algonode.cloud"
        self.indexer_address = "https://mainnet-idx.algonode.cloud"
        self.algod_token = ""
        self.indexer_token = ""
        
        try:
            self.algod_client = algod.AlgodClient(
                self.algod_token,
                self.algod_address
            )
            self.indexer_client = indexer.IndexerClient(
                self.indexer_token,
                self.indexer_address
            )
            status = self.algod_client.status()
            print(f"Algorand client başarıyla oluşturuldu. Node durumu: {status}")
        except Exception as e:
            print(f"Algorand client hatası: {str(e)}")

    async def get_token_holders(self, asset_id, limit=100):
        try:
            holders = defaultdict(int)
            next_token = ""
            total_supply = 0
            
            while True:
                response = self.indexer_client.search_transactions(
                    asset_id=asset_id,
                    txn_type="axfer",
                    limit=limit,
                    next_page=next_token
                )
                
                for txn in response.get("transactions", []):
                    if "asset-transfer-transaction" in txn:
                        transfer = txn["asset-transfer-transaction"]
                        receiver = transfer["receiver"]
                        amount = transfer["amount"]
                        sender = txn["sender"]
                        
                        holders[receiver] += amount
                        holders[sender] -= amount
                
                next_token = response.get("next-token")
                if not next_token:
                    break
            
            asset_info = self.algod_client.asset_info(asset_id)
            total_supply = asset_info["params"]["total"]
            
            holder_list = [
                {
                    "address": addr[:8] + "..." + addr[-4:],
                    "full_address": addr,
                    "amount": amt,
                    "percentage": (amt / total_supply) * 100 if total_supply > 0 else 0
                }
                for addr, amt in holders.items()
                if amt > 0
            ]
            
            holder_list.sort(key=lambda x: x["amount"], reverse=True)
            
            return {
                "holders": holder_list,
                "total_supply": total_supply,
                "holder_count": len(holder_list),
                "circulation": sum(h["amount"] for h in holder_list)
            }
            
        except Exception as e:
            print(f"Token sahipleri alınamadı: {str(e)}")
            return {
                "holders": [],
                "total_supply": 0,
                "holder_count": 0,
                "circulation": 0
            }
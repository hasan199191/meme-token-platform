from algosdk import account, transaction
from algosdk.v2client import algod
import time

class TokenService:
    def __init__(self, algorand_service=None):
        """TokenService sınıfı başlatıcı"""
        if algorand_service is None:
            raise ValueError("algorand_service parametresi gerekli")
        self.algorand = algorand_service

    async def check_balance(self, address):
        """Cüzdan bakiyesini kontrol et"""
        try:
            account_info = self.algorand.client.account_info(address)
            return account_info.get('amount', 0)
        except:
            return 0

    async def create_meme_token(self, creator_private_key, asset_name, unit_name, total):
        try:
            # Önce bakiye kontrolü yap
            sender = account.address_from_private_key(creator_private_key)
            balance = await self.check_balance(sender)
            
            if balance < 1000000:  # 1 Algo minimum gerekli
                return {"error": "Yetersiz bakiye. En az 1 Algo gerekli."}

            # Token oluştur
            params = self.algorand.client.suggested_params()
            txn = transaction.AssetConfigTxn(
                sender=sender,
                sp=params,
                total=total,
                default_frozen=False,
                unit_name=unit_name,
                asset_name=asset_name,
                manager=sender,
                reserve=sender,
                freeze=sender,
                clawback=sender,
                decimals=0)
            
            signed_txn = txn.sign(creator_private_key)
            print("Transaction gönderiliyor...")
            tx_id = self.algorand.client.send_transaction(signed_txn)
            print(f"Transaction ID: {tx_id}")
            
            print("İşlem onayı bekleniyor...")
            for i in range(10):
                try:
                    pending_txn = self.algorand.client.pending_transaction_info(tx_id)
                    if "asset-index" in pending_txn:
                        print(f"Token başarıyla oluşturuldu! Asset ID: {pending_txn['asset-index']}")
                        return {
                            "status": "success",
                            "asset_id": pending_txn["asset-index"],
                            "tx_id": tx_id
                        }
                except:
                    pass
                time.sleep(2)
            return {"error": "Token oluşturulamadı - zaman aşımı"}
                
        except Exception as e:
            print(f"Token oluşturma hatası: {str(e)}")
            return {"error": str(e)}

    async def opt_in_to_token(self, account_private_key, asset_id):
        try:
            sender = account.address_from_private_key(account_private_key)
            params = self.algorand.client.suggested_params()
            
            txn = transaction.AssetTransferTxn(
                sender=sender,
                sp=params,
                receiver=sender,
                amt=0,
                index=asset_id)
                
            signed_txn = txn.sign(account_private_key)
            print("Opt-in transaction gönderiliyor...")
            tx_id = self.algorand.client.send_transaction(signed_txn)
            
            print("Opt-in onayı bekleniyor...")
            for i in range(10):
                try:
                    pending_txn = self.algorand.client.pending_transaction_info(tx_id)
                    if pending_txn.get("confirmed-round", 0) > 0:
                        print("Opt-in başarılı!")
                        return {"status": "success", "tx_id": tx_id}
                except:
                    pass
                time.sleep(2)
            return {"error": "Opt-in zaman aşımı"}
            
        except Exception as e:
            print(f"Opt-in hatası: {str(e)}")
            return {"error": str(e)}

    async def transfer_token(self, sender_private_key, receiver_address, asset_id, amount):
        try:
            sender = account.address_from_private_key(sender_private_key)
            params = self.algorand.client.suggested_params()
            
            txn = transaction.AssetTransferTxn(
                sender=sender,
                sp=params,
                receiver=receiver_address,
                amt=amount,
                index=asset_id)
                
            signed_txn = txn.sign(sender_private_key)
            print(f"Transfer işlemi başlatılıyor... ({amount} token)")
            tx_id = self.algorand.client.send_transaction(signed_txn)
            
            print("Transfer onayı bekleniyor...")
            for i in range(10):
                try:
                    pending_txn = self.algorand.client.pending_transaction_info(tx_id)
                    if "asset-transfer-transaction" in pending_txn:
                        print(f"Transfer başarılı! TX ID: {tx_id}")
                        return {
                            "status": "success", 
                            "tx_id": tx_id,
                            "amount": amount,
                            "receiver": receiver_address
                        }
                except:
                    pass
                time.sleep(2)
            return {"error": "Transfer zaman aşımı"}
                
        except Exception as e:
            print(f"Transfer hatası: {str(e)}")
            return {"error": str(e)}

    async def get_token_info(self, asset_id):
        """Token bilgilerini görüntüle"""
        try:
            asset_info = self.algorand.client.asset_info(asset_id)
            return {
                "durum": "başarılı",
                "isim": asset_info["params"]["name"],
                "birim": asset_info["params"]["unit-name"],
                "toplam": asset_info["params"]["total"],
                "oluşturan": asset_info["params"]["creator"]
            }
        except Exception as e:
            return {"hata": f"Token bilgisi alınamadı: {str(e)}"}

    async def get_token_balance(self, address, asset_id):
        """Token bakiyesini kontrol et"""
        try:
            account_info = self.algorand.client.account_info(address)
            for asset in account_info.get("assets", []):
                if asset["asset-id"] == asset_id:
                    return {
                        "durum": "başarılı",
                        "bakiye": asset.get("amount", 0)
                    }
            return {"hata": "Token bulunamadı"}
        except Exception as e:
            return {"hata": f"Bakiye sorgulanamadı: {str(e)}"}
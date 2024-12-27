from backend.services.algorand import AlgorandService
from backend.services.token import TokenService
from backend.services.database import DatabaseService
import asyncio
from algosdk import account
import time
from datetime import datetime

async def main():
    try:
        # 1. Servisleri başlat
        algo_service = AlgorandService()
        token_service = TokenService(algo_service)
        db_service = DatabaseService()
        
        # 2. Gönderici cüzdan oluştur
        creator_private_key, creator_address = account.generate_account()
        print(f"\nGönderici Cüzdan Oluşturuldu:")
        print(f"Adres: {creator_address}")
        
        # 3. Cüzdanı fonla
        print("\nLütfen gönderici cüzdanı fonlayın:")
        print("1. https://bank.testnet.algorand.network/ adresine gidin")
        print(f"2. Bu adresi yapıştırın: {creator_address}")
        print("3. 'Submit' butonuna tıklayın ve ENTER'a basın")
        input()
        
        # 4. Token oluştur
        print("\nToken oluşturuluyor...")
        result = await token_service.create_meme_token(
            creator_private_key=creator_private_key,
            asset_name="TestMeme",
            unit_name="MEME",
            total=1000000
        )
        print("Token oluşturuldu:", result)

        if result.get("status") == "success":
            # 5. Alıcı cüzdan oluştur
            receiver_private_key, receiver_address = account.generate_account()
            print(f"\nAlıcı Cüzdan Oluşturuldu:")
            print(f"Adres: {receiver_address}")
            
            # 6. Alıcı cüzdanı fonla
            print("\nLütfen alıcı cüzdanı fonlayın:")
            print(f"Adres: {receiver_address}")
            input("Fonladıktan sonra ENTER'a basın...")

            # 7. Token'a katılım (opt-in)
            print("\nToken'a katılım yapılıyor...")
            await token_service.opt_in_to_token(
                receiver_private_key, 
                result["asset_id"]
            )

            # 8. Token transfer et
            print("\nToken transfer ediliyor...")
            transfer_result = await token_service.transfer_token(
                creator_private_key,
                receiver_address,
                result["asset_id"],
                100  # transfer miktarı
            )
            print("\nTransfer Sonucu:", transfer_result)
            
            # 9. Transfer sonrası bakiyeler
            receiver_balance = await token_service.get_token_balance(receiver_address, result["asset_id"])
            sender_balance = await token_service.get_token_balance(creator_address, result["asset_id"])
            
            print("\nTransfer Sonrası Bakiyeler:")
            print(f"Gönderici Bakiye: {sender_balance.get('bakiye', 0)} token")
            print(f"Alıcı Bakiye: {receiver_balance.get('bakiye', 0)} token")
            
            # 10. Token detayları ve kayıt
            token_info = await token_service.get_token_info(result["asset_id"])
            tx_history = {
                "timestamp": datetime.now().isoformat(),
                "token_id": result["asset_id"],
                "token_name": token_info.get("isim"),
                "total_supply": token_info.get("toplam"),
                "circulating_supply": token_info.get("toplam") - sender_balance.get("bakiye", 0),
                "creator": creator_address,
                "holders": [
                    {"address": creator_address, "balance": sender_balance.get("bakiye", 0)},
                    {"address": receiver_address, "balance": receiver_balance.get("bakiye", 0)}
                ]
            }
            
            await db_service.islem_kaydet(tx_history)
            
    except Exception as e:
        print(f"Hata: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
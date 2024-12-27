from backend.services.database import DatabaseService
import asyncio
from datetime import datetime

async def main():
    try:
        print("\nToken İşlem Görüntüleyici")
        print("-" * 50)
        
        db_service = DatabaseService()
        islemler = await db_service.islem_listele()
        
        if not islemler:
            print("Henüz kaydedilmiş işlem bulunmuyor.")
            return
            
        for islem in islemler:
            print(f"\nİşlem Detayları:")
            print(f"Tarih: {datetime.fromisoformat(islem['islem_zamani']).strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"Token ID: {islem['token_id']}")
            print(f"Token Adı: {islem['token_adi']}")
            print(f"Toplam Arz: {islem['toplam_arz']:,}")
            print(f"Dolaşımdaki Token: {islem['dolasim_arzi']:,}")
            print("\nCüzdan Dağılımı:")
            for cuzdan in islem['cuzdan_listesi']:
                print(f"- Adres: {cuzdan['address'][:10]}...{cuzdan['address'][-5:]}")
                print(f"  Bakiye: {cuzdan['balance']:,} token")
            print("-" * 50)
            
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
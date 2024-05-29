import os
import glob
import time

# Silme işlemini yapan fonksiyon
def delete_old_files(folder_path, max_size_gb):
    try:
        # Klasördeki dosyaları zamana göre listele ve sırala
        files = sorted(glob.glob(os.path.join(folder_path, "*")), key=os.path.getmtime)

        # Dosya boyutunu ve kullanılan alanı hesapla
        total_size_gb = round(sum(os.path.getsize(file) / (1024**3) for file in files), 2)
        print(f"\nCurrent size: {total_size_gb} GB")

        # Eğer kullanılan alan maksimum boyutu aşıyorsa, en eski dosyaları sil
        while total_size_gb > max_size_gb:
            print("\nDosya boyutu sınırı aşıldı. Silme işlemi yapılıyor.")
            # En eski dosyayı silme işlemi
            if files:
                deleted_file = files[0]  # En eski dosya

                timestamp = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
                
                # Log çıktısı olarak, tarih||toplam alan||dosya silindikten sonraki alan||silinen dosya adı
                with open('../Logs/deleter.log', 'a') as log_file:
                    log_file.write(f"{timestamp}||{round(total_size_gb, 2)} GB||{round(total_size_gb - os.path.getsize(deleted_file) / (1024**3), 2)} GB||{os.path.basename(deleted_file)}\n")
                
                # Dosyayı sil
                os.remove(deleted_file)
                # Silinen dosyanın adını ekrana yazdır
                print(f"Removed file: {deleted_file}")
                files.pop(0)  # Silinen dosyayı listeden çıkar
                # Dosya boyutunu güncelle
                total_size_gb = round(sum(os.path.getsize(file) / (1024**3) for file in files), 2)
            else:
                break
        
        # Eğer toplamı max_size_gb altındaysa, ekrana yazdır
        if total_size_gb <= max_size_gb:
            print(f"\nDosya boyutu {max_size_gb} GB altında.")
    except Exception as e:
        print(f"Hata: {e}")
        with open('../Logs/deleter.log', 'a') as log_file:
            timestamp = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
            log_file.write(f"{timestamp}||ERROR: {e}\n")

if __name__ == "__main__":
    folder_path = '../Downloads'  # Downloads klasörünün yolu
    max_size_gb = 20  # Toplam alan sınırı (örneğin 20 GB)

    delete_old_files(folder_path, max_size_gb)

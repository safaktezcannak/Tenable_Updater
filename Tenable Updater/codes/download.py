import os
import requests
import time

# Proxy ayarlarını almak için fonksiyon
def get_proxy_from_file():
    # proxy.txt dosyasından proxy bilgilerini okuma
    # eğer dosya boşsa proxy kullanılmaz
    try:
        if os.stat('../Settings/proxy.txt').st_size > 0:
            with open('../Settings/proxy.txt', 'r') as proxy_file:
                proxy = proxy_file.read().strip()
        else:
            proxy = None
    except Exception as e:
        print(f"Proxy ayarları okunurken hata oluştu: {e}")
        proxy = None

    return proxy  # Proxy değerini döndür

# Dosya indirme fonksiyonu
def download(url, download_folder, dosya_turu, proxy):
    try:
        response = requests.get(url, allow_redirects=True, proxies={"http": proxy, "https": proxy} if proxy else None)
        if response.status_code == 200:
            # Dosyayı indirme tarihi ile isimlendirme
            # Time modülü ile tarih ve saat bilgisi alınır
            date_time = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
            
            # Dosya ismi oluşturma (tarih-dosya_turu.tar.gz)
            file_name = f"{date_time}-{dosya_turu}.tar.gz" # Örnek isim: 2021-08-25-15-30-00-feed.tar.gz

            # Dosyayı kaydetme
            with open(os.path.join(download_folder, file_name), 'wb') as download_file:
                download_file.write(response.content)
            
            # Log dosyasına yazma
            log_message = f"{date_time}||{file_name}||SUCCESSFULLY DOWNLOADED\n"

            # Terminal çıktısı
            print(f"{file_name} başarıyla indirildi.")
            with open('../Logs/download.log', 'a') as log_file:
                log_file.write(log_message)

        # Eğer response değeri 200 değilse, dosya indirilemediyse
        else:
            date_time = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
            log_message = f"{date_time}||{dosya_turu} FAIL RESPONSE CODE: {response.status_code}\n"
            with open('../Logs/download.log', 'a') as log_file:
                log_file.write(log_message)
            print(f"Hata {dosya_turu}: {response.status_code} - Dosya indirilemedi.")
    
    # Eğer bir hata oluşursa
    except Exception as e:
        date_time = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
        log_message = f"{date_time}||{dosya_turu}||FAIL DOWNLOAD: {e}\n"
        with open('../Logs/download.log', 'a') as log_file:
            log_file.write(log_message)
        print(f"Hata: {e}")

def main():
    # Proxy ayarlarını al
    proxy = get_proxy_from_file()  # Proxy ayarlarını al

    # urls.txt dosyasından linkleri okuma
    urls = []

    try:
        with open('../Settings/urls.txt', 'r') as urls_file:
            for line in urls_file:
                parts = line.strip().split("'")
                if len(parts) > 1:
                    urls.append(parts[1])
    except Exception as e:
        print(f"URL'ler okunurken hata oluştu: {e}")

    # İndirme klasörünün yerini veriyoruz
    download_folder = '../Downloads'

    # Her bir URL için dosya indirme işlemi
    for i, url in enumerate(urls):
        dosya_turu = "feed" if i == 0 else "plugin"  # İlk link "feed", ikinci link "plugin" olarak işlenir
        download(url, download_folder, dosya_turu, proxy)

if __name__ == "__main__":
    print()
    main()
    print()

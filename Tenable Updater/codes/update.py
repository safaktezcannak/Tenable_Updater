from tenable.sc import TenableSC
import time
import os
import sys
import warnings

# AuthenticationWarning'leri devre dışı bırak
warnings.filterwarnings("ignore")

# Log mesajı oluştur
def log_message(target_ip, status, message):
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
    log_message = f"{timestamp}||{target_ip}||{status} {message}\n"
    return log_message

# Güncelleme işlemini gerçekleştir
def update(target_ip, feed_file, plugin_file, access_key, secret_key):
    # İlk başta feed sonra plugin,
    # feed tarafında giriş işlemi yapıldıktan sonra tekrar yapılmaya gerek duyulmamıştır.
    try:  # Feed Kısmı
        # TenableSC bağlantısını oluştur
        sc = TenableSC(target_ip)  # IP adresi burada belirtilmeli
        sc.login(access_key=access_key, secret_key=secret_key)  # API anahtarları ile giriş yap

        # Feed dosyasını yükleme
        with open(feed_file, 'rb') as feedfile:
            sc.feeds.process('sc', feedfile)

        # Başarılı feed log mesajı
        log_success = log_message(target_ip, "FEED FILE SUBMITTED", "")
        with open('../Logs/update.log', 'a') as log_file:
            log_file.write(log_success)

        # Terminal çıktısı
        print(f"{target_ip} için FEED dosyası gönderildi.\n")

    except Exception as e:
        # Hata oluştuğunda log mesajı oluştur
        log_fail = log_message(target_ip, "FEED COULD NOT BE SUBMITTED", str(e))
        with open('../Logs/update.log', 'a') as log_file:
            log_file.write(log_fail)

        # Terminal çıktısı
        print(f"{target_ip} için FEED dosyası gönderilirken hata oluştu: {e}")

    try:  # Plugin kısmı
        with open(plugin_file, 'rb') as pluginfile:
            sc.feeds.process('active', pluginfile)

        log_success = log_message(target_ip, "PLUGIN FILE SUBMITTED", "")
        with open('../Logs/update.log', 'a') as log_file:
            log_file.write(log_success)

        print(f"{target_ip} için PLUGIN dosyası gönderildi.\n")

    except Exception as e:
        log_fail = log_message(target_ip, "PLUGIN COULD NOT BE SUBMITTED", str(e))
        with open('../Logs/update.log', 'a') as log_file:
            log_file.write(log_fail)

        print(f"{target_ip} için PLUGIN dosyası gönderilirken hata oluştu: {e}")

    finally:
        # Son olarak çıkış yap
        sc.logout()

def main():
    # main.py'de update.py target_ip inputu ile çalıştırılıyor. Burada bunun kontrolü yapılıyor.
    if len(sys.argv) != 4:
        print("Hata: Hedef IP adresi eksik!")
        return

    # Hedef IP adresini al, terminal inputu olarak alıyor.
    target_ip = sys.argv[1]
    access_key = sys.argv[2]
    secret_key = sys.argv[3]

    # Downloads klasörü içindeki feed ve plugin dosyalarını bulma
    download_folder = '../Downloads'
    feed_files = [f for f in os.listdir(download_folder) if f.endswith('-feed.tar.gz')]
    plugin_files = [f for f in os.listdir(download_folder) if f.endswith('-plugin.tar.gz')]

    # Eğer feed veya plugin dosyaları bulunamazsa hata ver
    if not feed_files or not plugin_files:
        print("Hata: Feed veya plugin dosyaları bulunamadı!")
        return

    # En son feed ve plugin dosyalarını al
    latest_feed_file = max(feed_files, key=os.path.getctime)
    latest_plugin_file = max(plugin_files, key=os.path.getctime)

    # Dosya yollarını oluştur ve bunları belirle
    feed_file = os.path.join(download_folder, latest_feed_file)
    plugin_file = os.path.join(download_folder, latest_plugin_file)

    # Son olarak güncelleme işlemini ip, feed ve plugin dosyaları ile başlat
    update(target_ip, feed_file, plugin_file, access_key, secret_key)

if __name__ == "__main__":
    main()

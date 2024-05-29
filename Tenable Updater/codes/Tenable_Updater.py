from datetime import datetime
import time
import subprocess

# log üretmek için fonksiyon
def log_message(message, target_ip=None):
    now = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
    with open('../Logs/main.log', 'a') as log_file:
        log_file.write(f"{now}||{target_ip}||{message}\n")

# Dosyadan satırları okumak için fonksiyon ip'ler ve Schedule'lar için
def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines

# subprocess.run işlemlerinde hata yakalamak için yardımcı fonksiyon
def run_subprocess(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")
        log_message(f"ERROR: {e}")

# update işlemi
def update_process(target_ip, access_key, secret_key):
    print(f"Güncelleme işlemi başlatılıyor {target_ip}...")
    run_subprocess(['python', 'update.py', target_ip, access_key, secret_key])

# Bildirim işlemi
def notification_process(notification_time, target_ip, access_key, secret_key):
    print(f"\nBildirimler kontrol ediliyor {target_ip}...")
    run_subprocess(['python', 'notificationChecker.py', notification_time, target_ip, access_key, secret_key])

# Fazlalık dosyaları silen işlem
def deleter_process():
    print(f"\nFazlalık dosyalar kontrol ediliyor...")
    run_subprocess(['python', 'downloadsDeleter.py'])

def main():
    # Dosya yolları
    target_ips_file = '../Settings/ipScheduled.txt' # Takvimleme txt
    schedule_file = '../Settings/scheduleList.txt' # Hedef Ip'ler txt

    # Sonsuz Döngüye sokuyoruz
    while True:
        # Dosyaları satır okuma fonskiyonuna sokuyoruz
        target_ips = read_file_lines(target_ips_file)
        schedule_list = read_file_lines(schedule_file)

        # Eşleşen IP'leri saklamak için bir liste, her döngüde sıfırlanacak
        matched_ips = []

        # Şu anki GÜN-SAAT:DAKİKA bilgisini alıyoruz
        now = datetime.now()
        current_day_time = now.strftime("%A-%H:%M")
        print(f"\nŞu an ki gün-saat: {current_day_time}")

        # Her bir ip için ve her bir schedule satırı için kontrol yap
        for idx, schedule in enumerate(schedule_list):
            # Eğer ki şu an ki gün-saat:dakika schedule'da varsa
            if current_day_time in schedule:
                # ilgili satırı pipe ile split ediyoruz
                target_ip, access_key, secret_key = target_ips[idx].split("||")
                # Terminale bunun bilgisini veriyoruz
                print(f"Eşleşme bulundu: {target_ip} ve {current_day_time}!\n")
                # Main loglaması (Sadece eşleşme bulundu şeklinde)
                log_message(f"MATCH FOUND", target_ip)
                # Eşleşen ip'yi ve keyleri listeye (ARRAY) ekliyoruz. (Schedule Listesinde hangi satırda eşleşme varsa o satırın index'indeki ip'yi ekliyoruz.)
                matched_ips.append((target_ip, access_key, secret_key))
        
        # Eğer ki eşleşen ip'ler varsa (Array boş değilse)
        if matched_ips:
            print("\nİndirme işlemi...")
            # download.py dosyasını çalıştırıyoruz
            run_subprocess(['python', 'download.py'])

            # Sonrasında denk gelen index ip'leri ve keyleri sırasıyla update ediyoruz
            for ip, key, secret in matched_ips:
                notification_time = int(time.time())
                update_process(ip, key, secret)
                notification_process(str(notification_time), ip, key, secret)

            # tüm update işlemleri bittikten sonra fazlalık dosyaları silen işlemi başlatıyoruz    
            deleter_process()
        
        # Eğer ki eşleşen ip yoksa
        if not any(current_day_time in schedule for schedule in schedule_list):
            # Terminale bunun bilgisini veriyoruz
            # İsteğe bağlı loglanabilir ama çok fazla log çıkarabilir
            print("Bu gün ve saat için eşleşme bulunamadı!\n")
        
        # Döngüyü 60 saniye bekletiyoruz, her dakika bekletiyoruz.
        time.sleep(60)

if __name__ == "__main__":
    print("\nmain.py çalışmaya başladı...")
    main()

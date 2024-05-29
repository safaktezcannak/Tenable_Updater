import time
import subprocess

# Loglama işlemi
def log_message(message, target_ip=None):
    now = time.strftime("%Y-%m-%d-%H-%M-%S-GMT%z", time.localtime())
    with open('../Logs/main2.log', 'a') as log_file:
        log_file.write(f"{now}||{target_ip}||{message}\n")

# Dosyadan satır satır okuma işlemi
def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines

# subprocess.run işlemlerinde hata yakalamak için yardımcı fonksiyon
def run_subprocess(command, target_ip=None):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        error_message = f"ERROR: {e}"
        print(error_message)
        log_message(error_message, target_ip)

# İndirme işlemi
def download_process():
    print(f"\nİndirme işlemi başlatılıyor...")
    run_subprocess(['python', 'download.py'])

# Güncelleme işlemi
def update_process(target_ip, access_key, secret_key):
    print(f"\nGüncelleme işlemi başlatılıyor {target_ip}...")
    run_subprocess(['python', 'update.py', target_ip, access_key, secret_key], target_ip)

# Bildirim işlemi
def notification_process(notification_time, target_ip, access_key, secret_key):
    print(f"\nBildirimler kontrol ediliyor {target_ip}...")
    run_subprocess(['python', 'notificationChecker.py', notification_time, target_ip, access_key, secret_key], target_ip)

# Fazlalık dosyaları silen işlem
def deleter_process():
    print(f"\nFazlalık dosyalar kontrol ediliyor...")
    run_subprocess(['python', 'downloadsDeleter.py'])

# Ana fonksiyon
def main():
    # Hedef IP'lerin bulunduğu dosya
    target_ips_file = '../Settings/ipSuddenly.txt'

    # ilk başta hedef için aynı dosylaar kullanılacağı için indirme işlemini yapıyoruz.
    download_process()

    # Hedef IP'leri oku
    target_ips = read_file_lines(target_ips_file)

    # her bir ip için döngü başlat
    for line in target_ips:
        target_ip, access_key, secret_key = line.split("||")

        log_message(f"SUDDENLY PROCESS STARTED", target_ip)

        notification_time = int(time.time())
        
        # Güncelleme işlemi
        update_process(target_ip, access_key, secret_key)
        
        # Bildirim işlemi
        notification_process(str(notification_time), target_ip, access_key, secret_key)

    # En son olarak gereksiz dosyaları sil
    deleter_process()

if __name__ == "__main__":
    print("\nmain2.py çalışmaya başladı...")
    main()
    print()

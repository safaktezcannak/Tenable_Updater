import requests
import urllib3
import time
import sys

# Terminaldeki SSL uyarılarını kapat 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Loglama işlemi
log_path = '../Logs/update.log'
def log_message(human_readable_time, target_ip, message):
    log_message = f"{human_readable_time}||{target_ip}||{message.strip()}\n"
    with open(log_path, 'a') as log_file:
        log_file.write(log_message)

# Parametrelerin alınmasında hata oluşması durumunda exit
if len(sys.argv) != 5:
    print("Hata: Eksik parametre!")
    sys.exit()

# Parametrelerin alınması
start_time = int(sys.argv[1])
target_ip = sys.argv[2]
accesskey = sys.argv[3]
secretkey = sys.argv[4]

# Tenable api adresi
api = f'https://{target_ip}/rest/notification'

# Parametreler ve headerlar
params = {
    "fields": "id,time,text",
    "timeframe": "24h"
}

headers = {
    'x-apikey': f'accesskey={accesskey}; secretkey={secretkey}'
}

# Bildirimler için liste ve id tekrarını engellemek için set
notifications_list = []
notification_ids = set()

# Hata sayacı
error_count = 0
max_errors = 2

# İki bildirimi alana kadar döngü
while len(notifications_list) < 2:
    if error_count >= max_errors:
        print("Maximum hata sayısına ulaşıldı. İşlem sonlandırılıyor.")
        break

    try:
        # Tenable API'ye istek yap
        response = requests.get(api, headers=headers, params=params, verify=False, timeout=10)

        # Eğer cevap 200 ise bildirimleri al
        if response.status_code == 200:
            notifications = response.json()["response"]

            # Bildirimlerin içinde dolaş
            for notification in notifications:
                unix_timestamp = int(notification['time'])
                
                # Belirtilen zamandan sonraki olan bildirimleri al
                if unix_timestamp >= start_time and notification['id'] not in notification_ids:
                    notifications_list.append(notification)
                    notification_ids.add(notification['id'])
                    
                    # İki bildirimi alınca döngüden çık
                    if len(notifications_list) >= 2:
                        break

        # Eğer cevap 200 değilse hata mesajı yaz
        else:
            error_message = f"ERROR: {response.status_code} - {response.text}"
            human_readable_time = time.strftime('%Y-%m-%d-%H-%M-%S-GMT%z', time.localtime())
            log_message(human_readable_time, target_ip, error_message)
            print(f"HATA: {response.status_code} - {response.text}")
            error_count += 1

    except requests.exceptions.ConnectTimeout:
        error_message = "ERROR: Connection timed out."
        human_readable_time = time.strftime('%Y-%m-%d-%H-%M-%S-GMT%z', time.localtime())
        log_message(human_readable_time, target_ip, error_message)
        print(error_message)
        error_count += 1
        time.sleep(5)  # Bağlantı zaman aşımından sonra 5 saniye bekle ve tekrar dene

    except requests.exceptions.RequestException as e:
        error_message = f"ERROR: {e}"
        human_readable_time = time.strftime('%Y-%m-%d-%H-%M-%S-GMT%z', time.localtime())
        log_message(human_readable_time, target_ip, error_message)
        print(error_message)
        error_count += 1
        break  # Diğer türde bir hata oluştuğunda döngüyü kır

# Bildirimleri zamana göre sırala
if len(notifications_list) > 0:
    sorted_notifications = sorted(notifications_list, key=lambda x: int(x['time']))

    # Bildirimleri ekrana yaz ve logla
    print("Belirtilen zamandan sonraki son 2 bildirim:")
    for notification in sorted_notifications:
        # Bildirimlerin bilgilerini al
        notification_text = notification['text']
        unix_timestamp = int(notification['time'])
        # Unix zamanını okunabilir zaman haline getir
        human_readable_time = time.strftime('%Y-%m-%d-%H-%M-%S-GMT%z', time.localtime(unix_timestamp))
        # Bildirimleri termial ekrana yaz
        print(f"ID: {notification['id']}")
        print(f"Time: {human_readable_time}")
        print(f"Text: {notification_text}")
        print("---------------------")
        # Bildirimleri log dosyasına yaz
        log_message(human_readable_time, target_ip, notification_text)
    print("Bildirimler loglandı.")
else:
    print("Bildirim alınamadı. İşlem sonlandırıldı.")

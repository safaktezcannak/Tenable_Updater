# Tenable_Updater
Offline tenable SC plugiin and feed updater.
# Tenable_Updater
Offline tenable SC plugiin and feed updater.

#### FOR ENGLISH VERSION, PLEASE SCROLL DOWN

#------------------TURKISH VERSION------------------#

<<<'tenableUpdate Script Project'>>>
Bu proje, belirli IP adreslerine ve zaman dilimlerine göre otomatik olarak dosya indirme, güncelleme ve dosya boyutu kontrolü yapma işlemlerini gerçekleştirir.

## Gereksinimler
- Python 3.x
- TenableSC
- requests kütüphanesi
- pytenable kütüphanesi

## Kurulum
1. Python 3.x`i yükleyin.
2. Gerekli kütüphaneleri yüklemek için terminal veya komut istemcisinde şu komutu çalıştırın:

>>> "pip install -r requirements.txt"

3. 'Settings' klasörü altında yer alan dosyaları düzenleyin:
- `proxy.txt`: Proxy ayarlarını burada belirtin (isteğe bağlı).
- `urls.txt`: İndirilecek dosyaların URL`lerini burada belirtin.
- `ipScheduled.txt`: Takvimleme için IP adreslerini ve zaman dilimlerini belirtin. main.py için bunu düzenleyin. ACCESSKEY ve SECRETKEY burada belirtiniz.
- `ipSuddenly.txt`: Ani güncellemeler için IP adreslerini burada belirtin. main2.py için bunu düzenleyin. ACCESSKEY ve SECRETKEY burada belirtiniz.
- `scheduleList.txt`: Zaman dilimlerini burada belirtin. main.py için bunu düzenleyin.

## Kullanım
1. `main.py`: Otomatik güncelleme ve dosya kontrolü için kullanılır. Ana programdır.
2. `main2.py`: Ani güncellemeler için kullanılır. Belirtilen IP adreslerini hızlıca günceller.
3. `download.py`: Dosya indirme işlemlerini gerçekleştirir.
4. `update.py`: TenableSC üzerinde güncelleme işlemlerini gerçekleştirir.
5. `downloadsDeleter.py`: Dosya boyutunu kontrol eder ve gereksiz dosyaları siler.
6. `notificationChecker.py`: TenableSC apileri ile sistem bildirimlerinden update bildirimlerini kontrol eder.

## Notlar
- Güncelleme işlemi bir hedef için yaklaşık 10 dakika sürer. Schedule listesini buna göre ayarlayın.
- 'Logs' klasöründe işlem günlükleri bulunur.
- 'Downloads' klasörü indirilen dosyaları içerir.
- 'codes' klasörü altında çalışan Python betikleri yer alır.


#---------ENGLISH VERSION---------#

<<<'tenableUpdate Script Project'>>>

This project automates the processes of downloading files, updating, and checking file sizes automatically based on specific IP addresses and timeframes.

## Requirements
-Python 3.x
-TenableSC
-requests library
-pytenable library

## Installation
1. Install Python 3.x.
2. In the terminal or command prompt, run the following command to install required libraries:

>>> "pip install -r requirements.txt"

3. Edit the files under the 'Settings' folder:
- proxy.txt: Specify proxy settings here (optional).
- urls.txt: Specify the URLs of the files to be downloaded here.
- ipScheduled.txt: Specify IP addresses and timeframes for scheduling. Edit this for main.py. Specify ACCESSKEY and SECRETKEY here.
- ipSuddenly.txt: Specify IP addresses for sudden updates. Edit this for main2.py. Specify ACCESSKEY and SECRETKEY here.
- scheduleList.txt: Specify timeframes here. Edit this for main.py.

## Usage
1. main.py: Used for automatic updates and file checks. This is the main program.
2. main2.py: Used for sudden updates. Quickly updates specified IP addresses.
3. download.py: Performs file download operations.
4. update.py: Performs update operations on TenableSC.
5. downloadsDeleter.py: Checks file size and deletes unnecessary files.
6. notificationChecker.py: Checks update notifications from system notifications with TenableSC APIs.

## Notes
- Update operations take approximately 10 minutes per target. Adjust the schedule list accordingly.
- Process logs are stored in the 'Logs' folder.
- Downloaded files are stored in the 'Downloads' folder.
- Python scripts that run are located under the 'codes' folder.

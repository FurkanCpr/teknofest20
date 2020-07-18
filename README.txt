Docker Commands

Docker komutlarını sudo kullanmadan çalıştırmak için aşağıdaki komut yazılır.
sudo usermod -a -G docker $USER
Değişiklerin gerçekleşmesi için log out yapılıp tekrar giriş yapılması gerekir.


Docker görüntüsünü yüklemek için aşağıdaki komut çalıştırılır.
docker load -i suruiha_2020_final_v2.tar

Yüklenen docker görüntüsünü kullanarak konteyneri çalıştırmak için aşağıdaki komut çalıştırılır."suruiha_docker" konteynerin ismidir, yarışmacı isterse değiştirmekte serbesttir.
docker run -it --name suruiha_docker --net=host suruiha_2020_final_v2

Gazebo'nun model dosyalarını doğru şekilde çalıştırabilmesi için aşağıdaki komut çalıştırılır.

docker cp suruiha_docker:/opt/suruiha_2020/src/suruiha_2019/suruiha_gazebo_model/gazebo_models/. ~/.gazebo/models

RabbitMQ sunusucu docker içerisinde bulunmaktadır. Docker başlatıldıktan sonra docker içersinde aşağıdaki komut çalıştırılarak sunucu ayağa kaldırılır.
service rabbitmq-server start

Çalışan Docker konteyneri içerisinde yeni bir bash açmak için aşağıdaki komut çalıştırılır.
docker exec -it suruiha_docker bash


Sistemin çalışması için 2 adet konteyner bash'ine ihtiyaç vardır. Bash dizinleri açıldıktan sonra aşağıdaki komutlar sırası ile çalıştırılmalıdır.
	Aşağıdaki komut ile simulasyon ortamı çalıştırılır.
	1. Konteyner Bash: roslaunch suruiha_gazebo demo_world.launch
	
	Aşağıdaki komut ile GUI çalıştırılır ve simülasyon ortamı ile bağlantı sağlanır. Arayüz tamamiyle çalıştırıldıktan sonra diğer komutlar çalıştırılmalıdır. (Paylaşılan videoda görülebilir.)
	Ubuntu Bash: gzclient --verbose

	İlk çalışma sırasında, simülasyon ortamının hemen açılmaması normaldir. Eksik olan grafik modellerin internetten indirlmesi biraz vakit alacaktır. Bu durum bir defaya masustur.
	
	Aşağıdaki komut ile İHA kontrolcüleri ayağa kalkmış olur. 
	2. Konteyner Bash: rosrun suruiha_controller SuruihaContestManager.py 0 0


Not: Simülasyon ortamında bulunan İHA'ların kontrol edilebilmesi için klasör içerisinde bulunan sample_team klasörü incelenmelidir.


rabbitmqctl add_user teknofest teknofest
rabbitmqctl set_user_tags teknofest administrator
rabbitmqctl set_permissions -p / teknofest "." "." ".*"

------ LOCAL PCDEKİ RABBİTMQ KAPATMA KOMUTU => sudo rabbitmqctl shutdown (çalışan node'u kapatıyor)----

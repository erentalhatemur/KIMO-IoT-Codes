![image](https://github.com/erentalhatemur/KIMO-IoT-Codes/assets/165311868/7e44f502-b6ea-4168-b437-b29a5892528f)

Merhaba,
Öncelikle projemi incelediğiniz için teşekkür ederim.Bu kısımda sizlere projemin nasıl ortaya çıktığını,üretim aşamasında nelerden yararlandığımı,araştırmalarımı
ve sunduğum çözümleri anlatacağım.

2019 yılında başlattığımız KimO! Ev Güvenliği Sistemleri Projesi, ülkemizde bulunan diğer güvenlik sistemlerine oranla daha düşük bütçelerde bir ürün üretmek için yola çıktı.9-11 Mart 2020 tarihlerinde düzenlenen TÜBİTAK Liselerarası Yarışmasında İstanbul ikinciliği ödülü aldıktan sonra Eylül 2020’den itibaren Başakşehir Living Lab tarafından desteklenen projeler kapsamına alındı.
2019 yılı ve sonrasında popülerleşen IoT teknolojisi kullanarak tasarladığım bu proje ev,dükkan,ofis vb. mülklerde düşük bütçe ve alandan tasarruf ederek maksimum güvenlik sağlamayı amaçladı.

ÇALIŞMA PRENSİBİ:
(ANA BİLGİSAYAR:Raspberry Pi,SINIR:Ultrasonik Mesafe Sensörü uyarılma sınırı)
- Kapının dış kısmında bulunan korumalı kalıp içerisinde mesafe sensörü bulunur. Mesafe sensörü sürekli ölçüm yaparken ürün kullanıcısının belirlediği sınır içerisinde bir hareket algıladığında ana bilgisayara bildirim gönderir
-Ana bilgisayar tarafından ürün kullanıcısına mail iletisi ile harekete dair haber verilir aynı anda kapıda bulunan gizli kamera ile elde ettiği görüntüleri Dropbox bulut depolama klasöründe depolar. Gönderdiği mail iletisinin içeriğinde bu klasöre ulaşabilmek için bir bağlantı bulunur ve kullanıcı bu görüntülere internet bağlantısına sahip olduğu her yerde ulaşabilir.

ÇALIŞMA PRENSİBİNİN 3D GÖRÜNTÜSÜ
![Ekran görüntüsü 2024-06-30 111255](https://github.com/erentalhatemur/KIMO-IoT-Codes/assets/165311868/01348646-ccd7-4d8a-89d1-8014d867088a)

Gönderilen e-mail'den bir örnek






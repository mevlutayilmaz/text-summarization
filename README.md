# Proje Başlığı: Metin Özetleme ve Görselleştirme

Bu projede verilen bir dokümandaki cümleler, graf yapısına dönüştürülmüş ve bu graf modeli görselleştirilmiştir. Sonrasında, graf üzerindeki düğümler ile özet oluşturan bir algoritma geliştirilmiştir. Proje, veri yapıları bilgisini pekiştirmek ve problem çözme becerisini geliştirmek amacıyla gerçekleştirilmiştir.


## İçindekiler

- [Özellikler](#özellikler)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Kullanılan Algoritmalar](#kullanılan-algoritmalar)
- [Proje Adımları](#proje-adımları)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Ekran Görüntüleri](#ekran-görüntüleri)

## Özellikler

- **Belge Yükleme:** Bir DOCX dosyasını yükleyin ve metin ile beklenen özeti çıkarın
- **Metin Ön İşleme:** Metni özetleme için hazırlamak üzere tokenizasyon, temizlik ve işleme işlemleri yapar.
- **Özet Üretme:** Metin analizine ve puanlama kriterlerine dayalı olarak özetler oluşturur.
- **Görselleştirme:** Metindeki kelime ilişkilerini içeren grafikleri oluşturur ve görüntüler.

## Kullanılan Teknolojiler

- **Programlama Dili:** Python
- **Geliştirme Ortamı:** PyCharm
- **GUI Araçları:** Qt Designer
- **Kütüphaneler:**
  - `nltk` - Doğal Dil İşleme Kitaplığı (NLTK), metin ön işleme için kullanılır; bu, tokenizasyon, kök bulma ve durak kelimelerin kaldırılmasını içerir.
  - `PyQt5` - Uygulama arayüzünü oluşturmak için kullanılan GUI çerçevesi sağlar.
  - `networkx` - Grafikler oluşturmak ve görselleştirmek için kullanılır. Bu, kelime ilişkilerini ve cümle benzerliklerini görselleştirmeyi sağlar.
  - `matplotlib` - NetworkX ile oluşturulan grafiklerin görselleştirilmesi için grafik çizim yetenekleri sağlar.
  - `sklearn` - Makine öğrenimi araçlarını sağlar, CountVectorizer metin vektörizasyonu ve cosine similarity cümle benzerliğini ölçmek için kullanılır.
  - `docx` - DOCX dosyalarını okumak ve işlemek için kullanılır.
  - `rouge` - Özetlerin kalitesini değerlendirmek için ROUGE (Recall-Oriented Understudy for Gisting Evaluation) metriklerini kullanır.

## Kullanılan Algoritmalar

### 1. Metin Ön İşleme

Metin ön işleme aşamasında, aşağıdaki adımlar uygulanır:

- **Noktalama İşaretlerini Kaldırma:** Metindeki tüm noktalama işaretlerini kaldırarak sadece kelimeleri analiz ederiz.
- **Küçük Harfe Çevirme:** Metni küçük harfe çeviririz, böylece büyük-küçük harf farklılıklarını ortadan kaldırırız.
- **Durak Kelimeleri Çıkarma:** Anlam taşımayan ve sıklıkla kullanılan kelimeleri (örneğin, "ve", "bu") metinden çıkarırız.
- **Kök Bulma (Stemming):** Kelimeleri köklerine indirgeriz. Örneğin, "yazıyor", "yazdı" kelimeleri kök "yaz" olarak işlenir.

### 2. Cümle Benzerliği Hesaplama

Cümleler arasındaki benzerliği hesaplamak için kullanılan teknikler:

- **CountVectorizer:** Cümleleri vektörlere dönüştürür. Bu, metindeki kelimeleri sayarak her bir cümleyi bir kelime frekansı vektörü olarak temsil eder.
- **Kosinüs Benzerliği:** İki cümlenin vektörleri arasındaki açıyı hesaplayarak benzerliklerini ölçer. Kosinüs benzerliği, iki vektör arasındaki açının kosinüsünü kullanarak benzerliği değerlendirir.
  
### 3. TF-IDF (Terim Frekansı - Ters Belge Frekansı)

TF-IDF, metindeki kelimelerin önemini değerlendirmek için kullanılır:

- **TF (Term Frequency):** Bir kelimenin bir cümledeki frekansıdır. Bir kelimenin ne kadar sık kullanıldığını ölçer.
- **IDF (Inverse Document Frequency):** Bir kelimenin tüm belgelerdeki önemini ölçer. Kelimenin ne kadar yaygın olduğunu belirler, yaygın kelimeler düşük IDF puanına sahipken nadir kelimeler yüksek IDF puanına sahiptir.
- **TF-IDF:** TF ve IDF değerlerinin çarpımıdır. Bu, bir kelimenin belirli bir cümledeki önemini değerlendirir.

### 4. Cümle Puanlama

Cümlelerin puanlanması için çeşitli faktörler göz önünde bulundurulur:

- **Başlıktaki Kelimeler:** Cümlede başlıktaki kelimelerin bulunup bulunmadığını kontrol ederiz.
- **Numerik Veri:** Cümledeki sayısal verileri sayarız. Genellikle bilgi açısından önemli olabilir.
- **Benzerlik:** Cümlenin diğer cümlelerle olan benzerliğine bakarız. Yüksek benzerlik gösteren cümleler daha fazla önem taşır.
- **İsimler:** Cümledeki özel isimleri (örneğin, yer adları, kişi isimleri) sayarız.
- **TF-IDF Temelli Kelimeler:** Cümlede TF-IDF değeri yüksek kelimelerin sayısını ölçeriz.

### 5. Özetleme ve ROUGE Puanı

Özetleme işlemi, puanlama sonuçlarına dayanarak önemli cümleleri seçer. Bu seçilen cümleler, metnin özetini oluşturur. ROUGE puanı, oluşturulan özet ile beklenen özet arasındaki benzerliği ölçer. ROUGE, genellikle özetlerin kalitesini değerlendirmek için kullanılır.


## Proje Adımları

1. **Doküman Yükleme:** Kullanıcıdan doküman yüklemesi sağlanmıştır.
2. **Graf Oluşturma:** Dokümandaki cümleler graf yapısına dönüştürülmüştür. Her cümle bir düğüm olarak temsil edilmiştir.
3. **Graf Görselleştirme:** Oluşturulan graf, kullanıcı arayüzünde görselleştirilmiştir.
4. **Cümle Skorlama:** Cümleler arasındaki anlamsal ilişkiler skorlanmış ve özet çıkarma algoritması geliştirilmiştir.
5. **Özetleme:** Önemli cümleler seçilerek özet çıkarılmıştır.
6. **ROUGE Skoru Hesaplama:** Çıkarılan özet ile gerçek özet arasındaki benzerlik ROUGE skoru ile ölçülmüştür.

## Kurulum

1. **Gerekli Kütüphaneleri Yükleyin:**
   Gerekli Python kütüphanelerini yüklemek için aşağıdaki komutu çalıştırın:
   ```bash
   pip install nltk pyqt5 networkx matplotlib scikit-learn python-docx rouge

2. **Proje Dosyalarını İndirin:**
   Proje dosyalarını GitHub'dan klonlayın veya indirin:
   ```bash
   git clone https://github.com/mevlutayilmaz/text-summarization.git

3. **Uygulamayı Çalıştırın:**
   Proje dizininde `main.py` dosyasını çalıştırarak uygulamayı başlatın:
   ```python
   python main.py

4. **GUI'yi Dönüştürün:**
   Qt Designer ile oluşturulmuş `.ui` dosyasını Python koduna dönüştürün:
   ```python
   pyuic5 -o convertGui.py untitled.ui
   ```

   Bu adım, Qt Designer'da oluşturduğunuz grafik arayüzün Python koduna dönüştürülmesini sağlar. `convertGui.py` dosyasını proje dizininde bulabilirsiniz.

5. **Proje Yapılandırmasını Kontrol Edin:**
   `main.py`, `convertGui.py`, ve `Gui.py` dosyalarının doğru yapılandırıldığından emin olun. Her dosya, uygulamanızın doğru çalışması için gerekli olan kodu içermelidir.

6. **Test ve Geliştirme:**
   Uygulamanızı test edin ve gerekli geliştirmeleri yapın. Uygulama işleyişi ve kullanıcı arayüzü ile ilgili her türlü değişiklik bu aşamada yapılmalıdır.

## Kullanım

1. Dokümanı yüklemek için arayüzdeki ilgili alanı kullanın.
2. "Visualize Doc." butonuna tıklayarak dokümanı graf yapısında görselleştirin.
3. "Summary" butonuna basarak özet çıkarın ve cümle skorlarını görselleştirin.
4. Özetin gerçek özet ile benzerliğini ROUGE skoru ile ölçün.

## Ekran Görüntüleri

<table style="border-spacing: 0; border-collapse: collapse; width: 100%;">
  <tr>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/368c1c2e-3f34-46b7-abc0-f112fc2e009f" width="400" />
    </td>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/8041cece-b065-4322-9196-3b8fbfa05c3e" width="400" />
      <p style="text-align: center;">Doküman Graf Yapısı</p>
    </td>
  </tr>
  <tr>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/bdc16433-03fc-460f-95a2-9aecaa074ab9" width="400" />
      <p style="text-align: center;">Özet 1</p>
    </td>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/c6a1e8e1-efff-4cac-bb76-0e20ee0b2982" width="400" />
      <p style="text-align: center;">Özet.1 Cümle Puanları</p>
    </td>
  </tr>
  <tr>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/36d2a858-c450-4a3d-b883-6f9ac62f9ee2" width="400" />
      <p style="text-align: center;">Özet 2</p>
    </td>
    <td style="padding: 0; vertical-align: middle; text-align: center;">
      <img src="https://github.com/user-attachments/assets/c20ab694-1918-4414-81cc-f74091a8558d" width="400" />
      <p style="text-align: center;">Özet.2 Cümle Puanları</p>
    </td>
  </tr>
</table>



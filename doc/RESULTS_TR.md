# Deneysel Sonuçlar (Image Quality Inspector)

## Veri Seti
Bu çalışmada farklı kalite seviyelerine sahip **229** adet görüntü kullanılmıştır. Görüntüler; bulanıklık, gürültü, düşük aydınlatma, düşük kontrast ve pozlama hataları gibi gerçek dünya bozulmalarını içerecek şekilde seçilmiştir.

## Karar Dağılımı
Sistem her görüntü için kalite skorunu (0–100) hesaplamış ve **kabul/ret** kararı üretmiştir.

- **ACCEPT (Kabul):** 91
- **REJECT (Ret):** 138

Bu dağılım, sistemin “her şeyi kabul eden” veya “her şeyi reddeden” bir yapı olmadığını; düşük kaliteli girdileri filtreleyen bir **quality gate** olarak çalıştığını göstermektedir.

## Çıktı Dosyaları
Çalıştırma sonucunda aşağıdaki dosyalar üretilmiştir:
- `quality_out/results.csv` → tablo/rapor için sonuçlar
- `quality_out/results.jsonl` → sistem log’u (makine okunur çıktı)

## Grafikler
Aşağıdaki grafikler kalite skorlarının dağılımını göstermektedir:

- Accept/Reject skor dağılımı: `assets/hist_accept_reject.png`
- Tüm skor histogramı: `assets/hist_all.png`
- Skorların sıralı eğrisi: `assets/scores_sorted_curve.png`

## Temsilî Örnekler (Kanıt)

Aşağıdaki görseller, sistemin yüksek kalite görüntülere yüksek skor verdiğini ve düşük kaliteli görüntüleri doğru şekilde reddettiğini göstermektedir:

- ACCEPT örnekleri: `assets/model_sonuclarimiz/accept/`
- REJECT örnekleri: `assets/model_sonuclarimiz/reject/`


## Kısa Yorum
Görüntü kalitesindeki bozulmaların (özellikle bulanıklık, düşük ışık ve sensör gürültüsü) çoğu zaman birlikte oluştuğu gözlemlenmiştir. Bu durum, gerçek dünya kamera koşullarında model performansının neden kararsızlaştığını açıklamaktadır. Önerilen kalite denetim sistemi, düşük kaliteli girdileri model öncesinde eleyerek downstream CV modelleri için daha stabil bir giriş sağlamayı amaçlar.

from app.normalizers.sr.strategy import SerbianNormalizerStrategy
from app.normalizers.en.strategy import EnglishNormalizerStrategy
from app.normalizers.de.strategy import GermanNormalizerStrategy

def main() -> None:
    german_examples = [
        "Mein BMW kostet €25.000 und verbraucht 7,5 l/100km bei einer Temperatur von 25°C.",
        "Tesla Model S hat 670 kW Leistung und beschleunigt 0-100 km/h in 2,1 Sekunden.",
        "Wir kauften ein Haus am 12.05.2023. für $150.000 mit 120 m² Fläche.",
        "Neues iPhone kostet €1.200 und hat 6,1 Zoll Bildschirm mit 2556×1179 Pixel Auflösung.",
        "Computer läuft mit 3,2 GHz mit 16 GB RAM und verbraucht 65 W Energie.",
        "Mercedes AMG GT kostet €180.000 und hat 4,0 l Motor mit 630 PS Leistung.",
        "Formel I Wagen fährt 350 km/h und beschleunigt 0-100 km/h in 2,6 s mit 1000 kg Gewicht.",
        "Wohnung mit 85 m² kostet €2.500/m² was insgesamt €212.500 für Jahr 2024 ist.",
        "Porsche neunhundertelf verbraucht 9,5 l/100km und hat 64 l Tank für Preis €120.000.",
        "Wir kauften Fernseher mit 65 Zoll für $1.500 der 150 W verbraucht und 4K Auflösung hat.",
        "Laptop kostet €1.200 und hat 512 GB SSD mit Geschwindigkeit von 3.500 MB/s.",
        "Flugzeug fliegt in Höhe von 11.000 m mit Geschwindigkeit 900 km/h mit 180 Passagieren.",
        "Telefon hat 4.500 mAh Akku und verbraucht 12 W beim Laden von 0-100%.",
        "Volkswagen Golf kostet €35.000 und hat 1,4 l Motor mit 150 PS Leistung.",
        "Haus hat 150 m² mit 15 kW Heizung für Temperatur von 22°C im Winter.",
        "Ferrari F acht kostet €280.000 und fährt 0-100 km/h in 2,9 s mit 3,9 l Motor.",
        "Monitor mit 27 Zoll kostet $400 und verbraucht 25 W mit 2560×1440 Auflösung.",
        "Audi A acht kostet €95.000 und verbraucht 8,2 l/100km mit 73 l Tank.",
        "Prozessor läuft mit 4,5 GHz und verbraucht 95 W mit 8 Kernen und 16 Threads.",
        "Heimkino kostet €2.200 und hat Lautsprecher 5×100 W mit 200 W Subwoofer."
    ]

    english_examples = [
        "My BMW costs 25.000 € and consumes 7,5 l/100km at a temperature of 25°C.",
        "Tesla Model S has power of 670 kW and accelerates 0-100 km/h in 2,1 seconds.",
        "We bought a house 12.05.2023. for 150.000 $ which has 120 m² area.",
        "New iPhone costs €1.200 and has a 6,1 inch screen with resolution 2556×1179 pixels.",
        "Computer runs at 3,2 GHz with 16 GB of RAM and consumes 65 W of energy.",
        "Mercedes AMG GT costs 180.000 € and has a 4,0 l engine with power of 630 horsepower.",
        "Formula 1 car goes 350 km/h and accelerates 0-100 km/h in 2,6 s with 1000 kg weight.",
        "Apartment of 85 m² costs 2.500 €/m² which is total 212.500 € for 2024 year.",
        "Porsche 911 consumes 9,5 l/100km and has a tank of 64 l for price of €120.000.",
        "We bought a TV of 65 inch for $1.500 that consumes 150 W and has 4K resolution.",
        "Laptop costs 1.200 € and has a 512 GB SSD with speed of 3.500 MB/s.",
        "Airplane flies at an altitude of 11.000 m with speed of 900 km/h with 180 passengers.",
        "Phone has a battery of 4.500 mAh and consumes 12 W when charging from 0-100%.",
        "Volkswagen Golf costs 35.000 € and has a 1,4 l engine with power of 150 HP.",
        "House has 150 m² with 15 kW heating for temperature of 22°C in winter.",
        "Ferrari F8 costs €280.000 and goes 0-100 km/h in 2,9 s with a 3,9 l engine.",
        "Monitor of 27 inch costs $400 and consumes 25 W with resolution 2560×1440.",
        "Audi A8 costs 95.000 € and consumes 8,2 l/100km with a tank of 73 l.",
        "Processor runs at 4,5 GHz and consumes 95 W with 8 cores and 16 threads.",
        "Home theater costs 2.200 € and has speakers of 5×100 W with a 200 W subwoofer."
    ]

    serbian_examples = [
        "Dacia 1000$ a meni rodjus 25.06.1996. pa ti vidi a ide 1457km posle",
        "Tesla model S ima snagu od 670 kW i ubrzava 0-100 km/h za 2,1 sekunde.",
        "Kupili smo kuću 12.05.2023. za 150.000 $ koja ima 120 m² površine.",
        "Novi iPhone košta €1.200 i ima ekran od 6,1 inch sa rezolucijom 2556×1179 piksela.",
        "Računar radi na 3,2 GHz sa 16 GB RAM-a i troši 65 W energije.",
        "Mercedes AMG GT košta 180.000 € i ima motor od 4,0 l sa snagom od 630 konja.",
        "Formula 1 bolid ide 350 km/h i ubrzava 0-100 km/h za 2,6 s sa 1000 kg težine.",
        "Apartman od 85 m² košta 2.500 €/m² što je ukupno 212.500 € za 2024. godinu.",
        "Porsche 911 troši 9,5 l/100km i ima rezervoar od 64 l za cenu od €120.000.",
        "Kupili smo TV od 65 inch za $1.500 koji troši 150 W i ima 4K rezoluciju.",
        "Laptop košta 1.200 € i ima SSD od 512 GB sa brzinom od 3.500 MB/s.",
        "Avion leti na visini od 11.000 m brzinom od 900 km/h sa 180 putnika.",
        "Telefon ima bateriju od 4.500 mAh i troši 12 W pri punjenju od 0-100%.",
        "Volkswagen Golf košta 35.000 € i ima motor od 1,4 l sa snagom od 150 HP.",
        "Kuća ima 150 m² sa grejanjem od 15 kW za temperaturu od 22°C zimi.",
        "Ferrari F8 košta €280.000 i ide 0-100 km/h za 2,9 s sa motorom od 3,9 l.",
        "Monitor od 27 inch košta $400 i troši 25 W sa rezolucijom 2560×1440.",
        "Audi A8 košta 95.000 € i troši 8,2 l/100km sa rezervoarom od 73 l.",
        "Procesor radi na 4,5 GHz i troši 95 W sa 8 jezgara i 16 threadova.",
        "Kućni bioskop košta 2.200 € i ima zvučnike od 5×100 W sa subwooferom od 200 W."
    ]

    sr_normalizer = SerbianNormalizerStrategy()
    en_normalizer = EnglishNormalizerStrategy()
    de_normalizer = GermanNormalizerStrategy()

    for example in english_examples:
        normalized = en_normalizer.normalize(example)
        print(f"{example} -> {normalized}")

    for example in german_examples:
        normalized = de_normalizer.normalize(example)
        print(f"{example} -> {normalized}")

    for example in serbian_examples:
        normalized = sr_normalizer.normalize(example)
        print(f"{example} -> {normalized}")

if __name__ == "__main__":
    main()

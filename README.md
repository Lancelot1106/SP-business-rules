# SP-business-rules


De code zelf is te vinden in de Relation_functions.py en Relation_Creation.py. De R_Creation.py is speciaal gemaakt om snel en makkelijk alle functies uit te kunnen voeren zonder veel extra moeite. Hierin hoeven enkel de lijsten en regel aan te worden gepast. 

_idsToUse_ is nu even voor het gemak en voorbeeld, maar in principe zou je door de volledige database kunnen loopen om de functies voor ieder item uit te voeren om zo de volledige recommendationstabel voor te bereiden.

_rule_ wordt gebruikt om aan te duiden of je met content of collaboration werkt. De tabel wordt dat ook met de rule aangemaakt en ingevuld

_itemsToGet_ is een lijst van gegevens die je uit de database zou willen halen. Hier is het enkel het merk, de category, doelgroep en prijs, maar in principe zou hier nog veel meer aan toe kunnen worden gevoegd


In de R_functions.py staan alle gebruikte functies. Hierover een korte uitleg (er staat binnen comments in de functies ook uitleg)

__getProduct__ haalt aan de hand van de huidige id gegevens op die matchen met de kolomnamen

__getSimilars__ haalt aan de hand van gegeven items de id's op van matchende producten

__whereClause__ maakt de regel voor de 'WHERE' statement aan

__createTable__ gooit zo mogelijk de tabel voor de geselecteerde regel weg en maakt deze zo mogelijk aan

__insertdata__ voegt de data in de gekozen tabel, dit zijn (voor nu) de eerste 4 producten in de id lijst (minus het originele product mocht dat ertussen staan)


hieronder een voorbeeld van de database met de gebruikte ID's in de meest linker kolom en daarnaast de 4 recommendations (en de nieuwe geboorte van "Venus" aangezien ik nog weinig ervaring heb met 2 schermen gebruiken)
![image](https://user-images.githubusercontent.com/70372427/111656552-ec461b00-880a-11eb-875b-069e755967b3.png)

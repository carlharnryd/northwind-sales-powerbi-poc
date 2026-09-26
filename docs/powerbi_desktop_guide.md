# Power BI Desktop - steg för steg

Den här guiden beskriver exakt hur du bygger och sparar Power BI-rapporten för
projektet, från en tom rapport till en sparad `.pbix`-fil i repot.

## Om ditt Power BI Desktop är inställt på svenska

Guiden nedan är skriven med Power BI Desktop:s engelska menynamn (File, Home,
Get data, Save As, med mera). Om ditt program visar svenska menyer (Fil,
Start, Infoga, Modellering, Visa, Optimera, Hjälp) påverkar det två helt
olika saker: dels vad knapparna heter, dels hur talvärden i CSV-filerna
tolkas. Det andra är viktigare och kan ge fel resultat utan att du märker
det direkt.

### Viktigast: decimaltal kan tolkas 100 gånger för stora

CSV-filerna i `data/powerbi` är skapade av Python och använder punkt `.` som
decimaltecken, till exempel `6.87` för en valutakurs. Det är internationell/
amerikansk standard. Svensk regioninställning använder istället komma `,` som
decimaltecken och punkt som tusentalsavgränsare.

Om Power BI Desktop, med svensk regioninställning, tolkar filens tal enligt
svensk standard kan det läsa `6.87` som talet `687` (punkten tolkas som
tusentalsavgränsare, inte decimaltecken) - alltså 100 gånger för stort, helt
utan felmeddelande.

Detta kan i värsta fall drabba dessa kolumner:

- `fact_sales`: `unit_price`, `discount`, `line_amount`,
  `exchange_rate_to_sek`, `line_amount_sek`
- `dim_product`: `list_unit_price`

**Kontrollera direkt efter att du läst in filerna, innan du går vidare:**

1. Gå till **Table view** (Tabellvy) i vänstermenyn.
2. Välj tabellen `fact_sales`.
3. Titta på kolumnen `exchange_rate_to_sek`. De tre unika värdena ska vara
   ungefär `6.87`, `7.87` och `8.065` (jämför med
   [docs/data_profile.md](data_profile.md)).
4. Om du istället ser heltal utan decimaler, till exempel `687`, `787`,
   `8065`, har talen tolkats fel och behöver rättas enligt nedan.

**Så här rättar du det om det har blivit fel:**

1. Klicka på tabellen `fact_sales` i fältpanelen, klicka sedan på
   **Transform data** (Transformera data) i fliken **Home** (Start). Detta
   öppnar Power Query-redigeraren.
2. Högerklicka på kolumnrubriken för den felaktiga kolumnen, till exempel
   `exchange_rate_to_sek`.
3. Välj **Change Type** (Ändra typ) > **Using Locale...** (Med hjälp av
   språkinställning...). Om texten skiljer sig något i din version, leta
   efter ett alternativ som nämner "språkinställning" eller "locale".
4. Sätt **Data Type** (Datatyp) till `Decimal Number` (Decimaltal) och
   **Locale** (Språkinställning) till `English (United States)`.
5. Klicka **OK**.
6. Upprepa för övriga drabbade kolumner i listan ovan.
7. Klicka **Close & Apply** (Stäng och tillämpa) för att ladda om datat med
   rätt tolkning.

Datumkolumnerna (`order_date`, `date`) är inte känsliga för detta, eftersom
de är skrivna i det entydiga formatet `ÅÅÅÅ-MM-DD`, vilket tolkas likadant
oavsett regioninställning.

### DAX-formlerna i den här guiden påverkas inte

Funktionsnamnen `SUM`, `DISTINCTCOUNT` och `DIVIDE` skrivs och fungerar exakt
likadant oavsett vilket visningsspråk Power BI Desktop har. Måttnamnen i den
här guiden (`Total Sales SEK`, `Order Count`, `Average Order Value SEK`)
skrivs precis som i guiden. Det enda formlerna gör är att referera till
kolumner och andra mått, så inga hårdkodade decimaltal skrivs in i
formelfältet, och därför uppstår ingen decimaltecken-konflikt där.

### Så hittar du rätt knapp när menyerna är på svenska

De sju huvudflikarna högst upp i Power BI Desktop heter, i ordning:
**Fil**, **Start**, **Infoga**, **Modellering**, **Visa**, **Optimera**,
**Hjälp**. Guiden nedan använder de engelska namnen (File, Home, Insert,
Modeling, View, Optimize, Help) - använd tabellen nedan för att hitta rätt
flik och knapp på svenska.

| Engelskt namn i guiden | Svenskt namn i Power BI Desktop |
| --- | --- |
| File (flik) | Fil |
| Home (flik) | Start |
| Insert (flik) | Infoga |
| Modeling (flik) | Modellering |
| View (flik) | Visa |
| Optimize (flik) | Optimera |
| Help (flik) | Hjälp |
| Get data | Hämta data |
| Load | Läs in |
| Transform Data | Transformera data |
| Save As | Spara som |
| This PC / Browse this device | Den här enheten / Bläddra på den här enheten |
| Table view | Tabellvy |
| Model view | Modellvy |
| Report view | Rapportvy |
| Data type (dropdown på Start-fliken i Tabellvy) | Datatyp |
| New measure (knapp på Modellering- eller Start-fliken) | Nytt mått |
| Cardinality | Kardinalitet |
| Many to one (*:1) | Många till en (*:1) |
| Cross filter direction / Single | Korsfiltreringsriktning / Enkelriktad |
| Visualizations | Visualiseringar |
| Fields | Fält |
| Filters | Filter |
| Card | Kort |
| Clustered bar/column chart | Grupperat stapel-/kolumndiagram |
| Line chart | Linjediagram |
| Slicer | Skiva |
| Table (visual) | Tabell |
| Sort by | Sortera efter |
| Top N filter | Övre N-filter |
| Format | Format |
| Currency | Valuta |
| Decimal Number | Decimaltal |
| Whole Number | Heltal |
| Date | Datum |
| Options and settings | Alternativ och inställningar |
| Options | Alternativ |
| GLOBAL | GLOBALT |
| CURRENT FILE | AKTUELL FIL |
| Regional Settings | Regioninställningar |
| Locale | Språkinställning / Lokal |
| Delete from model | Ta bort från modellen |
| Change Type | Ändra typ |
| Using Locale... | Med hjälp av språkinställning... |
| Column quality / distribution / profile | Kolumnkvalitet / kolumnfördelning / kolumnprofil |
| Close & Apply | Stäng och tillämpa |

Exakta ordval kan skilja sig något mellan Power BI-versioner. Om du inte
hittar en knapp, leta efter en med liknande betydelse i samma flik.

**Viktigt att skilja på:** att byta visningsspråk (Fil > Alternativ och
inställningar > Alternativ > Globalt > Språk) ändrar bara vad knapparna
heter, till exempel Fil istället för File. Det löser **inte**
decimaltalsproblemet ovan, eftersom det styrs av en helt annan inställning
(Regional Settings/Locale, se nästa avsnitt). Byt bara visningsspråk om du
vill att menytexterna exakt ska matcha guiden, inte som en lösning på
decimalproblemet.

### Rekommenderad genväg: fixa decimaltalen med en enda inställning, innan import

Om du inte redan har importerat filerna, eller vill börja om för att slippa
manuellt rätta kolumner en efter en, gör så här. Det här är den snabbaste
vägen och kräver noll manuellt arbete per kolumn efteråt:

Steg med svenska menynamn (det som faktiskt visas i ditt Power BI Desktop):

1. Om du redan har läst in de fem CSV-filerna: högerklicka på varje tabell i
   fältpanelen (`fact_sales`, `dim_customer`, `dim_product`, `dim_category`,
   `dim_date`) och välj **Ta bort från modellen**. Om du hellre vill starta
   helt om, stäng filen utan att spara och öppna en ny tom rapport.
2. Klicka på fliken **Fil** högst upp till vänster.
3. Klicka på **Alternativ och inställningar**.
4. Klicka på **Alternativ**.
5. I dialogrutan som öppnas, klicka på **AKTUELL FIL** i vänsterlistan.
6. Under **AKTUELL FIL**, klicka på **Regioninställningar**.
7. Sätt rullistan **Språkinställning** (kan även visas som **Lokal**) till
   `English (United States)`.
8. Klicka **OK**.
9. Klicka på **Hämta data**.
10. Välj **Text/CSV** (samma namn på svenska).
11. Bläddra till mappen `data/powerbi` och öppna en av de fem filerna.
12. Klicka **Läs in**.
13. Upprepa steg 9-12 för alla fem filerna.
14. Gör en snabb koll: klicka på **Tabellvy** i vänstermenyn, välj
    `fact_sales`, kontrollera att `exchange_rate_to_sek` visar
    `6.87`/`7.87`/`8.065` och att `discount` visar decimaltal som
    `0.05`/`0.1`/`0.15`. Om det ser rätt ut direkt behöver du inte röra
    något mer i avsnitt 3 nedan.

Om något enstaka värde ändå ser fel ut efter detta (ovanligt, men kan hända
beroende på Power BI-version): använd **Strategi B** i avsnitt 3.4, som
rättar flera kolumner samtidigt på under en minut, i stället för att börja
om igen.

## 0. Vilken miljö du ska vara i

Power BI Desktop är ett fristående Windows-program. Det är **inte** kopplat
till projektets Python-miljö (`.venv`). Du behöver **inte** öppna en terminal
och **inte** aktivera något virtuellt environment för de här stegen. Du
behöver bara ha Power BI Desktop öppet som ett vanligt Windows-program.

Om du inte vet om Power BI Desktop är installerat: tryck på Windows-tangenten,
skriv `Power BI Desktop` och se om appen visas i listan. Om den inte finns,
ladda ner den gratis från Microsoft Store (sök `Power BI Desktop`) eller via
powerbi.microsoft.com.

## 1. Öppna Power BI Desktop

1. Starta appen **Power BI Desktop**.
2. Om en startskärm visas med senaste filer, klicka bort den eller välj
   **Blank report** (Tom rapport).
3. Du ska nu se en tom rapportyta, med paneler för **Fields** (Fält),
   **Visualizations** (Visualiseringar) och **Filters** (Filter) till höger.

## 2. Läs in de fem CSV-filerna

Filerna ligger klara i mappen:

```text
C:\Users\cahr\source\northwind-sales-powerbi-poc\data\powerbi
```

Du gör följande fem gånger, en gång per fil:

1. Klicka på **Home** i det övre menyfältet.
2. Klicka på **Get data**.
3. Välj **Text/CSV** i listan. Om den inte syns direkt, klicka **More...** och
   sök efter `Text/CSV`.
4. Bläddra till mappen ovan.
5. Välj en av filerna nedan och klicka **Open**:
   - `fact_sales.csv`
   - `dim_customer.csv`
   - `dim_product.csv`
   - `dim_category.csv`
   - `dim_date.csv`
6. Ett förhandsgranskningsfönster visas. Klicka direkt på **Load** (Läs in),
   inte på "Transform Data".
7. Upprepa steg 2-6 tills alla fem filer är inlästa.

När du är klar ska **Fields**-panelen till höger visa fem tabeller:
`fact_sales`, `dim_customer`, `dim_product`, `dim_category`, `dim_date`.

## 3. Kontrollera datatyper

### 3.1 Snabb koll i Table view

1. Klicka på ikonen **Table view** i vänstermenyn (ser ut som ett litet
   rutnät).
2. Välj tabellen `fact_sales`.
3. Kontrollera kolumnerna:
   - `order_date` ska vara typen **Date**. Om det står **Text**, klicka på
     kolumnen så den är markerad, gå till fliken **Start** och leta efter
     rullistan som visar den nuvarande datatypen (**Datatyp**), byt den till
     `Date`.
   - `line_amount`, `line_amount_sek`, `unit_price`, `exchange_rate_to_sek`
     ska vara **Decimal Number**.
   - `quantity` ska vara **Whole Number**.
4. Gå till tabellen `dim_date`. Kontrollera att kolumnen `date` är **Date**,
   och att `year`, `quarter`, `month_number` är **Whole Number**.
5. Gå till `dim_customer`, `dim_product`, `dim_category`. Kontrollera att
   id-kolumnerna (`customer_id`, `product_id`, `category_id`) har samma
   datatyp som motsvarande kolumn i `fact_sales`, annars fungerar inte
   relationerna i nästa steg.

### 3.2 Fullständig checklista per tabell - vad som är rimliga värden

Använd tabellerna nedan för att avgöra om ett fält faktiskt är fel, inte bara
vilken datatyp det har. Det här är särskilt viktigt om Power BI är inställt
på svenska, se avsnittet om detta högre upp i den här filen.

**`fact_sales`** (2 155 rader)

| Kolumn | Förväntad typ | Rimligt värde | Tecken på fel |
| --- | --- | --- | --- |
| `order_detail_id` | Text | t.ex. `10248-11` | - |
| `order_id` | Whole Number | ca 10248-11077 | - |
| `customer_id` | Text | 5 bokstäver, t.ex. `VINET` | - |
| `product_id` | Whole Number | 1-77 | - |
| `category_id` | Whole Number | 1-8 | - |
| `order_date` | Date | 1996-07-04 till 1998-05-06 | Visas som text, inte datum |
| `order_year` | Whole Number | 1996, 1997 eller 1998 | - |
| `ship_country` / `ship_city` | Text | t.ex. `France`, `Reims` | - |
| `unit_price` | Decimal Number | ca 2 till 264 | Värden 100 gånger för stora, t.ex. `1400` istället för `14.00` |
| `quantity` | Whole Number | 1 till 130 | - |
| `discount` | Decimal Number | `0`, `0.05`, `0.1`, `0.15`, `0.2` eller `0.25` | **Bästa tidiga varningstecknet**: heltal som `5`, `10`, `15`, `20`, `25` istället för decimaltal |
| `line_amount` | Decimal Number | varierar, upp till några tusen | Onaturligt stora heltal |
| `exchange_rate_to_sek` | Decimal Number | `6.87`, `7.87` eller `8.065` | Visas som `687`, `787`, `8065` |
| `line_amount_sek` | Decimal Number | summa totalt 9 839 628,90 SEK, snitt ca 4 566 SEK/rad | Onaturligt stora tal per rad |

**`dim_customer`** (91 rader): `customer_id` text (5 bokstäver), `company_name`/
`contact_name`/`city`/`country` text, `region` text där många rader helt
korrekt är tomma (null).

**`dim_product`** (77 rader): `product_id` Whole Number 1-77, `category_id`
Whole Number 1-8, `list_unit_price` Decimal Number i samma intervall som
`unit_price` ovan (kontrollera på samma sätt), `quantity_per_unit` text
(t.ex. `10 boxes x 20 bags`), `discontinued` antingen Whole Number (0/1)
eller True/False, båda fungerar, kontrollera bara att den inte blivit Text.

**`dim_category`** (8 rader): `category_id` Whole Number 1-8, `category_name`
text (t.ex. `Beverages`), `description` längre text.

**`dim_date`** (672 rader): `date` Date, `year` Whole Number 1996-1998,
`quarter` Whole Number 1-4, `month_number` Whole Number 1-12, `month_name`
text med engelska månadsnamn (t.ex. `July`, inte `juli`, eftersom filen
genererades av Python oavsett vilket språk Windows/Power BI har),
`year_month` text (t.ex. `1996-07`).

### 3.3 Snabbaste sättet att hitta alla felaktiga kolumner på en gång

Att leta rad för rad i en tabell med 2 155 rader är långsamt. Använd i
stället Power Querys inbyggda kolumnprofilering:

1. Klicka på tabellen i fältpanelen, klicka sedan **Transform data**
   (Transformera data) i fliken **Home** (Start). Det öppnar
   Power Query-redigeraren i ett eget fönster.
2. Klicka på fliken **View** (Visa) högst upp i Power Query-redigerarens
   eget menyfält (inte i huvudfönstret).
3. Bocka i kryssrutorna **Column quality**, **Column distribution** och
   **Column profile** (Kolumnkvalitet, Kolumnfördelning, Kolumnprofil).
4. Klicka på kolumnrubriken för t.ex. `exchange_rate_to_sek`. Under
   förhandsgranskningen visas nu statistik, bland annat **Min** och **Max**.
5. Jämför Min/Max mot tabellen i avsnitt 3.2. Om värdena är 100 gånger för
   stora, eller helt saknar decimaler där decimaler förväntas, är kolumnen
   felimporterad.
6. Upprepa för varje tabell. Det tar totalt bara någon minut och du slipper
   leta rad för rad.

### 3.4 Strategier för att rätta felaktiga kolumner

**Strategi A - Rätta en kolumn i taget (säkrast, tydligast att följa)**

1. Öppna Power Query-redigeraren enligt 3.3, steg 1.
2. Högerklicka på kolumnrubriken för den felaktiga kolumnen.
3. Välj **Change Type** (Ändra typ) > **Using Locale...** (Med hjälp av
   språkinställning...).
4. Sätt **Data Type** (Datatyp) till `Decimal Number` (Decimaltal) och
   **Locale** (Språkinställning) till `English (United States)`.
5. Klicka **OK**.
6. Upprepa för varje felaktig kolumn, en i taget.
7. Klicka **Close & Apply** (Stäng och tillämpa) när alla kolumner i alla
   tabeller är rättade.

**Strategi B - Rätta flera kolumner samtidigt (snabbare för `fact_sales`,
som kan ha upp till fem drabbade kolumner)**

1. Öppna Power Query-redigeraren enligt 3.3, steg 1.
2. Håll ner **Ctrl** och klicka på kolumnrubrikerna för alla drabbade
   kolumner samtidigt, t.ex. `unit_price`, `discount`, `line_amount`,
   `exchange_rate_to_sek`, `line_amount_sek`.
3. Högerklicka på valfri av de markerade kolumnrubrikerna.
4. Välj **Change Type** > **Using Locale...**, sätt `Decimal Number` och
   `English (United States)`, klicka **OK**. Alla markerade kolumner rättas
   i samma steg.
5. Klicka **Close & Apply** när alla tabeller är klara.

**Strategi C - Börja om med en tabell om det blivit rörigt**

Om du klickat runt och det känns oklart vilka steg som redan är gjorda för
en viss tabell:

1. I Power Query-redigerarens vänsterpanel (**Queries**), högerklicka på
   tabellens namn, till exempel `fact_sales`, och välj **Delete**.
2. Läs in filen på nytt enligt avsnitt 2 ovan.
3. Applicera Strategi B direkt, innan du gör något annat med tabellen.

**Strategi D - Ändra själva CSV-filernas format (valfritt, kräver
kodändring i projektet)**

Ett alternativ är att jag ändrar Python-exporten i
[src/build_warehouse.py](../src/build_warehouse.py) så att CSV-filerna
istället skrivs med semikolon som fältavgränsare och komma som
decimaltecken, det vill säga svensk CSV-konvention. Då tolkas filerna
korrekt direkt vid import, utan att du behöver göra något i Power Query.

Nackdelen är att filerna då blir mindre universella om något annat verktyg
eller en granskare förväntar sig standardformatet med punkt och komma. Jag
gör inte den här ändringen automatiskt, säg till om du vill att jag justerar
exporten på det sättet istället för att rätta i Power BI Desktop.

**Oavsett vilken strategi du väljer:** kontrollera efteråt att relationerna
i **Model view** fortfarande finns kvar (nästa avsnitt), eftersom en ändrad
datatyp ibland kan ta bort en tidigare skapad relation om typerna på ömse
sidor inte längre matchar.

## 4. Skapa relationer mellan tabellerna

1. Klicka på ikonen **Model view** i vänstermenyn (ser ut som flera kopplade
   rutor).
2. Du ser nu fem tabeller som lådor, med linjer mellan sig om Power BI redan
   gissat relationer. Kontrollera dem noga mot listan nedan. Om en relation
   saknas, skapar du den manuellt genom att dra med musen från en kolumn i en
   tabell till motsvarande kolumn i en annan tabell och släppa.
3. Skapa exakt dessa fyra relationer:

   | Från kolumn | Till kolumn |
   |---|---|
   | `fact_sales[customer_id]` | `dim_customer[customer_id]` |
   | `fact_sales[product_id]` | `dim_product[product_id]` |
   | `fact_sales[category_id]` | `dim_category[category_id]` |
   | `fact_sales[order_date]` | `dim_date[date]` |

4. I dialogrutan som visas för varje relation, kontrollera att:
   - **Cardinality** är `Many to one (*:1)`, med dimensionstabellen
     (`dim_...`) som "one"-sidan.
   - **Cross filter direction** är `Single`.
5. Klicka **OK** för varje relation.

## 5. Skapa DAX-mått

1. Gå tillbaka till **Report view** (första ikonen i vänstermenyn).
2. Klicka på tabellen `fact_sales` i fältpanelen så att den är markerad.
3. Klicka på fliken **Modeling** (Modellering) i menyfältet högst upp, klicka
   sedan på knappen **New measure** (Nytt mått).
4. En formel-rad öppnas högst upp. Skriv in exakt:

   ```DAX
   Total Sales SEK = SUM(fact_sales[line_amount_sek])
   ```

5. Tryck Enter.
6. Klicka **New measure** igen och skriv:

   ```DAX
   Order Count = DISTINCTCOUNT(fact_sales[order_id])
   ```

7. Tryck Enter.
8. Klicka **New measure** en tredje gång och skriv:

   ```DAX
   Average Order Value SEK = DIVIDE([Total Sales SEK], [Order Count])
   ```

9. Tryck Enter. Alla tre måtten ligger nu under `fact_sales` i fältpanelen.
10. Valfritt: högerklicka på `Total Sales SEK` och `Average Order Value SEK`,
    välj **Format**, sätt till **Currency** eller **Decimal number** med två
    decimaler.

## 6. Bygg rapportsida 1 - Försäljningsöversikt

1. Dubbelklicka på fliken `Page 1` längst ner och byt namn till
   `Försäljningsöversikt`.
2. Lägg till tre KPI-kort:
   - Klicka på tom yta på sidan.
   - Välj visualiseringstypen **Card** i **Visualizations**-panelen.
   - Dra fältet `Total Sales SEK` till kortet.
   - Upprepa två gånger till för `Order Count` och `Average Order Value SEK`.
     Placera de tre korten bredvid varandra högst upp på sidan.
3. Lägg till ett stapeldiagram för kategori:
   - Klicka på tom yta.
   - Välj **Clustered bar chart** (eller **Clustered column chart**).
   - Dra `dim_category[category_name]` till fältet **Y-axis** (eller
     **X-axis** om du valde kolumndiagram).
   - Dra `Total Sales SEK` till fältet **Values**.
4. Lägg till ett linjediagram för tid:
   - Klicka på tom yta.
   - Välj **Line chart**.
   - Dra `dim_date[year_month]` till **X-axis**.
   - Dra `Total Sales SEK` till **Y-axis**.
   - Lägg till en textruta ovanför diagrammet med texten:
     `Observera: 1998 är inte ett komplett kalenderår` (eftersom data slutar
     1998-05-06).
5. Lägg till en slicer:
   - Klicka på tom yta.
   - Välj visualiseringstypen **Slicer**.
   - Dra `fact_sales[ship_country]` till fältet.
   - Placera slicern så den syns tydligt, till exempel längst upp eller till
     vänster på sidan.

## 7. Bygg rapportsida 2 - Kunder och marknader

1. Klicka på **+** längst ner för en ny sida.
2. Dubbelklicka på den nya fliken och byt namn till `Kunder och marknader`.
3. Lägg till en tabell över topp 10 kunder:
   - Välj visualiseringstypen **Table**.
   - Dra `dim_customer[company_name]`, `dim_customer[country]` och
     `Total Sales SEK` till fältet **Columns**.
   - Klicka på de tre punkterna `...` uppe till höger på visualiseringen,
     välj **Sort by** och välj `Total Sales SEK`, fallande ordning.
   - Klicka på visualiseringen, öppna **Filters**-panelen, lägg till ett
     **Top N**-filter på 10 för `company_name`, baserat på `Total Sales SEK`.
4. Lägg till ett diagram över länder:
   - Välj **Clustered bar chart** (eller **Map** om du hellre vill visa en
     karta).
   - Dra `fact_sales[ship_country]` till axeln.
   - Dra `Total Sales SEK` till fältet **Values**.

## 8. Spara filen som `.pbix` - detaljerad genomgång

Om filen inte redan finns på disk blir det här en helt ny fil, inte en
uppdatering.

1. Klicka på **File** högst upp till vänster i Power BI Desktop.
2. Klicka på **Save As**.
3. Om Power BI frågar var du vill spara (OneDrive eller This PC), välj alltid
   **This PC** / **Browse this device**. Välj aldrig OneDrive, för att undvika
   synk-konflikter med Git-repot.
4. En vanlig Utforskaren-dialog öppnas. Klistra in denna sökväg i
   adressfältet och tryck Enter:

   ```text
   C:\Users\cahr\source\northwind-sales-powerbi-poc\powerbi
   ```

5. I fältet **File name**, skriv:

   ```text
   northwind_sales_report
   ```

6. Kontrollera att **Save as type** står till `Power BI files (*.pbix)` (det
   är standardvärdet).
7. Klicka på knappen **Save**.

Efter detta ligger filen exakt här:

```text
C:\Users\cahr\source\northwind-sales-powerbi-poc\powerbi\northwind_sales_report.pbix
```

**Om en fil med namnet `~$northwind_sales_report.pbix` dyker upp i samma
mapp:** det är en tillfällig låsfil som Power BI skapar medan filen är öppen.
Den är redan listad i projektets `.gitignore` och ska inte sparas i Git. Den
försvinner automatiskt när du stänger Power BI Desktop.

## 9. Spara löpande under arbetet

Tryck `Ctrl+S` med jämna mellanrum medan du arbetar, särskilt efter att du
lagt till en relation, ett mått eller en ny sida. Efter den första
**Save As** frågar Power BI inte om plats igen, `Ctrl+S` sparar direkt till
samma fil och plats.

## 10. Lägg till filen i Git efter att du är klar

När rapporten är sparad och du är nöjd med den, öppna en terminal i
projektmappen och kör dessa tre kommandon, ett i taget:

```powershell
git add powerbi/northwind_sales_report.pbix
```

```powershell
git commit -m "Add Power BI report"
```

```powershell
git push
```

# Mottagarguide: Northwind Sales Power BI POC

Den här guiden är för dig som har fått länken till GitHub-repot och vill öppna,
presentera eller själv återskapa lösningen på en Windows-dator.

## Börja här: välj vad du vill göra

Det finns två olika sätt att använda leveransen:

1. **Bara öppna och presentera rapporten.** Ladda ner `.pbix`-filen och öppna
   den i Power BI Desktop. Du behöver inte installera Python eller köra koden.
2. **Återskapa dataflödet.** Klona hela repot, installera Python-paketen och
   kör pipelinen. Den hämtar data från API:erna, bygger DuckDB och skriver om
   Power BI-CSV-filerna.

Om du bara ska granska rapporten kan du börja med del 1. Om du också vill
verifiera hur datat skapas går du vidare till del 2.

## 1. Öppna och presentera rapporten

### 1.1 Öppna GitHub-repot

Öppna länken:

[Northwind Sales Power BI POC på GitHub](https://github.com/carlharnryd/northwind-sales-powerbi-poc)

På repo-sidan visas `README.md`, som sammanfattar projektet. Kontrollera att
repo-sidan visar märket **Public** om du ska öppna länken utan GitHub-konto.
Om repot är privat måste ägaren ge dig åtkomst först.

### 1.2 Hämta Power BI-filen

1. Öppna mappen `powerbi` i repot.
2. Klicka på `northwind_sales_report.pbix`.
3. Klicka på **Download raw file** eller nedladdningsknappen.
4. Vänta tills filen har laddats ner. Webbläsaren placerar den vanligtvis i
   mappen **Hämtade filer**.

GitHub kan inte köra eller visa en PBIX-rapport interaktivt på webbsidan. PBIX
är en Power BI Desktop-fil som behöver laddas ner och öppnas i Power BI Desktop.

### 1.3 Öppna filen i Power BI Desktop

1. Starta **Power BI Desktop** från Windows Start-menyn.
2. Klicka på **Fil** längst upp till vänster.
3. Välj **Öppna rapport** eller **Öppna**.
4. Välj **Bläddra** om Power BI frågar var filen finns.
5. Öppna mappen **Hämtade filer**.
6. Markera `northwind_sales_report.pbix` och klicka på **Öppna**.

Om dubbelklick på filen i Utforskaren redan öppnar Power BI Desktop kan du
använda det sättet i stället.

Rapporten innehåller en importerad datamodell. Du behöver därför inte köra
Python bara för att öppna och visa den. Rapporten har två sidor:

- **Försäljningsöversikt**
- **Kunder och marknader**

Sidorna väljs med flikarna längst ned i Power BI-fönstret. För att kontrollera
rapporten kan du ändra land- eller årsfilter och se om kort och diagram
uppdateras.

### 1.4 Förstå knappen Uppdatera

Att öppna rapporten och att uppdatera rapportens data är två olika saker.

- **Öppna rapporten:** visar den importerade data som sparats i PBIX-filen. Det
  kräver inte Python.
- **Klicka på Uppdatera:** Power BI försöker läsa CSV-filer från filvägar som
  anges av Power Query-parametern `DataFolder`. Om parametern pekar på en annan
  mapp än den lokala klonen kan uppdateringen misslyckas även om rapporten går
  att öppna.

CSV-filerna finns i repot under `data/powerbi/`. Rapportens fem frågor använder
samma `DataFolder`-parameter och lägger själva till respektive CSV-filnamn.
Efter en kloning till en ny dator behöver mottagaren därför ändra en enda
parameter, inte fem separata sökvägar.

För en presentation där du bara ska visa den levererade rapporten behöver du
inte klicka på **Uppdatera**.

### 1.5 Ange sökvägen efter kloning

Gör detta om du vill uppdatera rapporten från CSV-filerna i din egen klonade
repo-mapp, eller om **Uppdatera** säger att en CSV-fil inte hittas.

1. Öppna den lokala rapportfilen `powerbi/northwind_sales_report.pbix` från
   den klonade projektmappen i Power BI Desktop.
2. I Utforskaren öppnar du projektmappen och går till `data\powerbi`.
3. Klicka i Utforskarens adressfält högst upp. Det ska visa hela sökvägen till
   CSV-mappen. Kopiera sökvägen med `Ctrl+C`. Den ska sluta med
   `northwind-sales-powerbi-poc\data\powerbi` och inte innehålla ett CSV-filnamn.
4. Gå tillbaka till Power BI Desktop. Klicka på **Start > Transformera data**
   för att öppna Power Query-redigeraren.
5. I Power Query-redigeraren klickar du på fliken **Start** och väljer
   **Hantera parametrar > Redigera parametrar**.
6. Välj parametern `DataFolder`.
7. I fältet för aktuellt värde markerar du den gamla mappsökvägen och klistrar
   in den nya sökvägen med `Ctrl+V`. Klistra in enbart mappen `data\powerbi`,
   inte ett filnamn som `fact_sales.csv` och inte citattecken.
8. Klicka **OK**. Ändra inte de fem frågornas formler eller övriga steg.
9. Klicka på **Stäng och tillämpa** och vänta tills Power BI har laddat frågorna.
10. I huvudfönstret klickar du på **Start > Uppdatera** och väntar tills
    uppdateringen är klar.
11. Kontrollera att rapporten inte visar fel och att värdena är rimliga:
    cirka 9 839 629 SEK i total försäljning, 830 ordrar och cirka 11 855 SEK
    i genomsnittligt ordervärde.
12. Tryck `Ctrl+S` för att spara rapporten med mappsökvägen för din dator.

Du behöver ändra `DataFolder` en gång per lokal klon. När Python-pipelinen
körs skriver den om CSV-filerna i den mappen; därefter kan Power BI läsa dem
med **Uppdatera** utan att du ändrar de fem frågorna igen.

## 2. Klona repot och återskapa pipelinen

Den här delen hämtar projektets källkod till datorn och kör hela dataflödet.

### 2.1 Program som behövs

Installera följande program om de inte redan finns:

- **Git for Windows**: behövs för att klona repot.
- **Python**: behövs för att köra pipelinen. Installationen ska innehålla
  Python Launcher-kommandot `py`.
- **Visual Studio Code**: rekommenderas för att öppna projektet och terminalen.
- **Power BI Desktop**: behövs för att öppna och presentera `.pbix`-rapporten.

Python-, Git- och VS Code-installationer behöver inte vara kopplade till något
AZDO-projekt. Detta är ett fristående GitHub-repo.

Kontrollera Git och Python så här:

1. Öppna PowerShell eller VS Code-terminalen.
2. Kör `git --version`. Git ska svara med ett versionsnummer.
3. Kör `py --version`. Python ska svara med ett versionsnummer.

Om något kommando inte känns igen behöver motsvarande program installeras
innan du fortsätter.

### 2.2 Klona med Visual Studio Code

1. Starta Visual Studio Code.
2. Tryck `Ctrl+Shift+P` för att öppna **Kommandopaletten**.
3. Skriv `Git: Clone`.
4. Välj kommandot **Git: Clone** i listan.
5. När VS Code frågar efter repo-URL, klistra in:

   ```text
   https://github.com/carlharnryd/northwind-sales-powerbi-poc.git
   ```

6. När VS Code frågar var repot ska sparas väljer du en plats där du har
   skrivbehörighet, till exempel din användarmapp. Välj den överordnade
   mappen, inte en redan skapad `northwind-sales-powerbi-poc`-mapp; VS Code
   skapar projektmappen själv.
7. Vänta tills kloningen är färdig.
8. Klicka på **Öppna** när VS Code erbjuder att öppna repot.
9. Om VS Code visar frågan **Vill du lita på författarna till filerna i den
   här mappen?**, välj **Ja, jag litar på författarna** för att använda
   projektet.

Du behöver inte välja eller skapa en branch. Kloningen öppnar den aktuella
standardversionen, `main`.

### 2.3 Kontrollera att rätt mapp är öppen

I VS Codes vänstra **Utforskaren** ska rotmappen heta
`northwind-sales-powerbi-poc`. Där ska bland annat följande synas:

```text
README.md
requirements.txt
src/
data/
docs/
powerbi/
```

Öppna `README.md` om du vill ha projektöversikten. I VS Codes vänstra
**Utforskaren** klickar du på pilen bredvid `data` och sedan på pilen bredvid
`powerbi`. Där visas CSV-filerna. De finns redan efter kloningen, så du
behöver inte ladda ner dem en och en. PBIX-filen finns i mappen `powerbi/`.

### 2.4 Skapa Python-miljön och installera paket

1. I VS Code-menyn klickar du på **Terminal**.
2. Välj **Ny terminal**.
3. Kontrollera att PowerShells aktuella sökväg slutar med
   `northwind-sales-powerbi-poc`. Om terminalen står någon annanstans, gå till
   projektmappen med `cd` följt av den sökväg där du klonade repot.
4. Skapa projektets isolerade Python-miljö:

   ```powershell
   py -m venv .venv
   ```

5. Uppdatera pip i just den miljön:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   ```

6. Installera projektets beroenden:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

En virtuell miljö håller projektets Python-paket åtskilda från andra projekt.
Du behöver inte aktivera den med `Activate.ps1`; kommandona ovan använder
miljöns Python direkt.

### 2.5 Kör hela datapipelinen

Kontrollera att terminalen fortfarande står i projektmappens rot och kör:

```powershell
.\.venv\Scripts\python.exe -m src.build_warehouse
```

Kommandot kör följande faser i ordning:

1. **Hämta:** hämtar Customers, Orders, Order_Details, Products och
   Categories från Northwind OData API. Pagination följs tills alla sidor är
   hämtade. Hämtar även Riksbankens årsvisa växelkurser för 1996, 1997 och
   1998.
2. **Spara rådata:** sparar API-svaren som JSON under `data/raw/`.
3. **Transformera:** läser JSON till tabeller, kopplar orderrader till order,
   produkt, kategori och årskurs, räknar försäljningsbelopp och skapar
   faktatabell och dimensioner.
4. **Kontrollera och lagra:** kör kvalitetskontroller och skriver tabellerna
   till `data/warehouse/northwind.duckdb`.
5. **Exportera:** skriver om de fem Power BI-CSV-filerna i `data/powerbi/`.

En lyckad körning ska bland annat visa ungefär:

```text
OK fact_sales rows: 2155
OK distinct orders: 830
OK total sales SEK: 9,839,628.90
```

Sista raderna anger var DuckDB-filen och CSV-filerna skrevs. De fem CSV-filerna
behåller samma filnamn; körningen skriver över dem med de nya resultaten.
Rå JSON och DuckDB skapas lokalt och versionshanteras inte. CSV-filerna är
versionshanterade i Git, men lokala ändringar hamnar inte på GitHub förrän de
committas och pushas.

Om körningen stannar med ett fel ska du läsa terminalens sista felmeddelande.
Vanliga orsaker är att internet/API:erna inte är tillgängliga eller att
paketinstallationen inte blev klar.

### 2.6 Vilka datafiler finns i Git och vilka byggs lokalt?

De fem CSV-filer som rapporten använder är versionshanterade. De finns redan
efter kloningen i projektmappen `data\powerbi`:

```text
data/powerbi/fact_sales.csv
data/powerbi/dim_customer.csv
data/powerbi/dim_product.csv
data/powerbi/dim_category.csv
data/powerbi/dim_date.csv
```

Praktiskt innebär det:

1. Efter kloning finns filerna redan i `data\powerbi`.
2. Python-pipelinen skriver om CSV-filerna med samma fem filnamn. Ta inte bort
   dem innan körningen och skapa inte egna kopior med andra namn.
3. Power BI använder mappen som anges av parametern `DataFolder`.
4. Öppna eller redigera inte CSV-filerna manuellt för att visa rapporten.
   Öppna PBIX-filen i Power BI Desktop.

Rå JSON i `data/raw/` och DuckDB-databasen i `data/warehouse/` skapas lokalt
och versionshanteras inte. CSV-filerna är versionshanterade. Om en körning
ändrar dem lokalt syns ändringarna inte automatiskt på GitHub; de behöver
committas och pushas med Git.

Northwind-beloppen antas vara USD och räknas om till SEK med Riksbankens sista
tillgängliga årsvisa USD/SEK-kurs. Se [antagandena](assumptions.md) och
[dataprofilen](data_profile.md) för detaljer och kontrollvärden.

## 3. Köra om och uppdatera Power BI

Gör detta när CSV-filerna finns i den klonade projektmappens `data\powerbi`.
Om du har klonat repot till en ny plats eller dator ställer du först in
`DataFolder` enligt avsnitt 1.5. Det behöver göras en gång per lokal klon.

1. Öppna den lokala rapportfilen `powerbi/northwind_sales_report.pbix` i
   Power BI Desktop. Öppna filen från den klonade projektmappen, inte från en
   gammal kopia i **Hämtade filer**.
2. Kontrollera att `DataFolder` pekar på den klonade mappens `data\powerbi`.
   Om inte, ändra parametern enligt avsnitt 1.5.
3. Klicka på fliken **Start** i Power BI Desktop.
4. Klicka på **Uppdatera** och vänta tills den är klar.
5. Kontrollera att inga fel visas och att huvudvärdena är rimliga: cirka
   9 839 629 SEK, 830 ordrar och cirka 11 855 SEK i genomsnittligt
   ordervärde.
6. Tryck `Ctrl+S` för att spara PBIX-filen om du ändrade `DataFolder`.

Om **Uppdatera** säger att en fil inte hittas ska du kontrollera att CSV-filen
finns i den lokala `data\powerbi`-mappen och sedan kontrollera parametern
`DataFolder` enligt avsnitt 1.5. Ändra inte frågornas formler, importera inte
tabellerna på nytt och bygg inte om visualiseringarna.

## 4. Vad som ingår i leveransen

- `src/`: Python-kod för extraktion, transformering, kvalitetskontroller och
  byggande av warehouse.
- `data/powerbi/`: fem CSV-filer som Power BI-modellen läser.
- `powerbi/northwind_sales_report.pbix`: färdig Power BI-rapport.
- `docs/`: arkitektur, datamodell, antaganden, dataprofil, AI-användning och
  instruktioner för Power BI Desktop.

GitHub kan visa koden, README, Markdown-dokument och CSV-filer. GitHub kör inte
Python och visar inte PBIX-rapporten interaktivt. För att se rapporten visuellt
behövs Power BI Desktop; för att köra datapipelinen behövs Python och
internetåtkomst till käll-API:erna.

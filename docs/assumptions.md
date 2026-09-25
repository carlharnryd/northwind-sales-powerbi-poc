# Assumptions

- Northwind monetary values are treated as USD for the purpose of converting to SEK.
- Riksbank exchange rates are mapped by order year.
- For each year, the last available observation in the requested date interval is used.
- The USD/SEK Riksbank series is identified as `SEKUSDPMI`.
- Northwind OData pagination is followed even though the case text lists one URL per entity; otherwise the API only returns the first page for several entities.
- The report follows the two explicitly named report pages in the case text.
- Sales over time is included on the sales overview page to satisfy the business request.

# Feed Aggregator
Feed aggregator platform.

## Sample data for uploading
**XML**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
   <element>
      <ecomm_id>1</ecomm_id>
      <ecomm_portal>Amazon</ecomm_portal>
      <ecomm_url>http://amazon.in/</ecomm_url>
      <last_updated>2016-04-11T15:23:15</last_updated>
      <price>22000</price>
      <product_id>10</product_id>
      <product_name>htc one</product_name>
   </element>
</root>
```

**JSON**
```json
[
{
	"product_name": "htc one",
	"product_id": 10,
	"ecomm_id": 1,
	"ecomm_portal": "Amazon",
	"ecomm_url": "http://amazon.in/",
	"price": 22000,
	"last_updated": "2016-04-11T15:23:15"
}
]
```

**CSV**
```csv
product_name,product_id,ecomm_id,ecomm_portal,ecomm_url,price,last_updated
htc one,10,1,Amazon,http://amazon.in/,22000,2016-04-10T15:23:15
```

> Aforementioned key must be present in each type of file.
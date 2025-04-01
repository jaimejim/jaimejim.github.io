###Object definition	
| Name|Object ID|Instances|Mandatory|Object URN| 
|:-:|:-:|:-:|:-:|:-:|
|LWM2M Security|0|Multiple|Mandatory|urn:oma:lwm2m:oma:0|

###Resource definitions	|ID|Name|Operations|Instances|Mandatory|Type|Range or Enumeration|Units|Description|
|:--|:--|:-:|:-:|:-:|:-:|:-:|:-:|--:||0|LWM2M Server URI||Single|Mandatory|String|0-255 bytes||Description omitted||1|Bootstrap Server||Single|Mandatory|Boolean|||Description omitted||2|Security Mode||Single|Mandatory|Integer|0-3||Description omitted||3|Public Key or Identity||Single|Mandatory|Opaque|||Description omitted||4|Server Public Key||Single|Mandatory|Opaque|||Description omitted||5|Secret Key||Single|Mandatory|Opaque|||Description omitted||6|SMS Security Mode||Single|Optional|Integer|0-255||Description omitted|
|7|SMS Binding Key Parameters||Single|Optional|Opaque|6 bytes||Description omitted|
|8|SMS Binding Secret Key(s)||Single|Optional|Opaque|16-32-48 bytes||Description omitted||9|LWM2M Server SMS Number||Single|Optional|String|||Description omitted||10|Short Server ID||Single|Optional|Integer|1-65535||Description omitted||11|Client Hold Off Time||Single|Optional|Integer||s|Description omitted||12|Bootstrap Server Account Timeout||Single|Optional|Integer||s|Description omitted|	
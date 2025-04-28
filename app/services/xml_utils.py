import json
from lxml import etree
import io

def transform_xml(xml_string, xslt_path):
    xml = etree.parse(io.BytesIO(xml_string.encode('utf-8')))
    xslt = etree.parse(xslt_path)
    transform = etree.XSLT(xslt)
    result = transform(xml)

    
    try:
        json_data = json.loads(str(result))
        return json_data
    except json.JSONDecodeError as e:
        print("❌ Error parsing transformed XML to JSON:", e)
        return None

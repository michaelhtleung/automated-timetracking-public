from datetime import datetime
import dateutil.parser

# ISO parsing:
today = datetime.today().isoformat()
print(today)
today = dateutil.parser.isoparse(str(today)) # RFC 3339 format
print(today)

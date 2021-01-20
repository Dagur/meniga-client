from meniga_client import Meniga
import json

m = Meniga('your email', 'your password')
res = m.get_accounts()

print(json.dumps(res, sort_keys=True, indent=4))

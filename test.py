from dotenv import load_dotenv
import os
load_dotenv()

import json
cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
cred = json.loads(cred_path.replace("\n", "\\n"))
print(type(cred))


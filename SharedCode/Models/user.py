
from dataclasses import dataclass
from typing import List, Optional
from typing import Any
from dataclasses import dataclass
import json
from dataclasses import asdict
from SharedCode.Utils.constants import Constants

@dataclass
class User:
    id: str
    user_id: str
    name: str
    email: Optional[str] = None
    kv_secret_name: Optional[str] = None
    fyers_user_name: Optional[str] = None

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

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        _user_id = str(obj.get("UserId"))
        _id = _user_id
        _name = str(obj.get("name", None))
        _email = str(obj.get("email", None))
        _kv_secret_name = str(obj.get(Constants.kv_secret_name, None))
        _fyers_user_name = str(obj.get(Constants.fyers_user_name, None))
        return User(_id, _user_id, _name, _email, _kv_secret_name, _fyers_user_name)
    
    
    def to_dict(self) -> dict:
        user_dict = asdict(self)
        user_dict["UserId"] = user_dict.pop("user_id")
        user_dict["id"] = user_dict["UserId"]
        return user_dict

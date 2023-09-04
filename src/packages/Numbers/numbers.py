from ...views.classes.alerts import Alert
from util import _abc, _SPECIALS

def validar_telefone(tel : str) -> bool|None:
    if tel == '': return False
    elif len(tel) < 9 or len(tel) > 9:
        Alert().valores_invalidos(arg='número')
        return None
    elif tel[0] != '9' or (int(tel[1]) > 5 and int(tel[1]) < 9) or tel[1] == '0':
        Alert().valores_invalidos(arg='número')
        return None
    else:
        _abc.extend(_SPECIALS)
        for char in _abc:
            if char in tel.lower():
                Alert().valores_invalidos()
                return None
    return True
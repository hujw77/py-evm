from ..homestead import HomesteadVM

from .vm_state import SpuriousDragonVMState

SpuriousDragonVM = HomesteadVM.configure(
    __name__='SpuriousDragonVM',
    # classes
    _state_class=SpuriousDragonVMState,
)

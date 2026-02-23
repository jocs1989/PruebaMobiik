from abc import ABC, abstractmethod
from core.enum_core.nodes_enum import Node
import logging
from typing import Dict, Any, List, Optional, TypedDict
class BaseNode(ABC):
    def __init__(self,nodo:Node):
        self.nodo=nodo
        self.name =nodo.value
        self.logger=logging.getLogger("uvicorn.error")

    def _prepare_memory(self,state:Dict[str,any])-> Dict[str,Any]:
        state.setdefault("prev_nodo",None) # atras
        state.setdefault("current_nodo",None) # actual
        state.setdefault("next_nodo",None) # siguiente
        


        
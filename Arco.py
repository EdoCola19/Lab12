from dataclasses import dataclass

from Retailer import Retailer


@dataclass
class Arco:
    Retailer1: Retailer
    Retailer2: Retailer
    peso: int
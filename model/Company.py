from dataclasses import dataclass, field

from model.Section import Section

@dataclass
class Company:
    sections: list[Section] = field(default_factory=list)
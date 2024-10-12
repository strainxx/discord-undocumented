import abc

class Packet(abc.ABC):
    @abc.abstractmethod
    def decode(self, data: dict) -> None:
        """Fill current packet class fields from dict data"""

    @abc.abstractmethod
    def encode(self) -> str:
        """Encode current packet to json string"""

    def assert_op(self, op):
        if self.op != op:
            raise AssertionError(f"Tryed to use {type(self).__name__} with op {op}")
from string import Template


def validate_packet(input_packet: dict):
    if not isinstance(input_packet, dict):
        raise TypeError(
            Template("Invalid packet: $p").substitute(p=input_packet)
        )

    for key, value in input_packet.items():
        if isinstance(value, dict):
            validate_packet(value)
        else:
            if not isinstance(key, str):
                raise TypeError(
                    Template("Invalid key in packet: $k. Packet = $p").substitute(
                        k=key, p=input_packet)
                )

            if not isinstance(value, (dict, float, int, str)):
                raise TypeError(
                    Template("Invalid value in packet: $v. Packet = $p").substitute(
                        v=value,
                        p=input_packet)
                )

# could be staticmethods on PacketManger class, but we want to be able to invoke
# flattened = flatten_packet(packet) and print(flattened)  per prompt


def flatten_packet(input_packet: dict, delimiter: str = "."):
    validate_packet(input_packet)
    flattened = FlattenedPacket()
    stack = [{"dict": input_packet, "prefix": ""}]

    # Push nested dicts onto stack until we have flattened keys
    while stack:
        current_dict, prefix = stack.pop().values()

        for key, value in current_dict.items():
            flat_key = (
                Template("$p$d$k").substitute(p=prefix, d=delimiter, k=key)
                if (prefix)
                else key
            )

            if isinstance(value, dict):
                stack.append({"dict": value, prefix: flat_key})
            else:
                flattened[flat_key] = value
    return flattened


def flatten_packet_recursive(
        input_packet: dict, prefix: str = "", delimiter: str = ".", validated_packet: bool = False
):
    if not validated_packet:
        validate_packet(input_packet)

    flattened = FlattenedPacket()

    for key, value in input_packet.items():
        flat_key = (
            Template("$p$d$k").substitute(p=prefix, d=delimiter, k=key)
            if (prefix)
            else key
        )
        if isinstance(value, dict):
            flattened = {
                **flattened,
                **flatten_packet_recursive(value, flat_key, delimiter, True),
            }
        else:
            flattened[flat_key] = value

    return flattened


class FlattenedPacket(dict):
    # Python dict ordering is arbitrary but we want to print consistently by
    # sorting keys
    def __repr__(self):
        # Can replace with return dict.__repr__(self) to fail tests
        res = "{"
        for i, key in enumerate(sorted(self.keys())):
            res += (
                Template("'$k': $v, ").substitute(k=key, v=self[key])
                if (i < len(self.keys()) - 1)
                else Template("'$k': $v").substitute(k=key, v=self[key])
            )
        res += "}"
        return res


class PacketManager:
    def __init__(self, delimiter: str = "."):
        self.data = []
        self.delimiter = delimiter

    def add(self, input_packet: dict):
        validate_packet(input_packet)
        flattened = flatten_packet(input_packet, self.delimiter)
        self.data.append(flattened)

    def __repr__(self):
        res = ""
        for packet in self.data:
            res += repr(packet)
        return res

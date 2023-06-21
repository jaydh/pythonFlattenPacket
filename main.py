from string import Template

class FlattenedPacket(dict):

    # Python dict ordering arbitrary but we want to print consistently by sorting keys
    def __repr__(self):
        res = "{"
        for i, key in enumerate(sorted(self.keys())):
            res += Template("'$k': $v, ").substitute(k=key, v=self[key]) if (i < len(self.keys()) - 1) else Template("'$k': $v").substitute(k=key, v=self[key])
        res += "}"
        return res

class PacketManager:
    def __init__(self, delimiter = '.'):
        self.data = []
        self.delimiter = delimiter


    def add(self, input_packet):
        validate_packet(input_packet)
        flattened = flatten_packet(input_packet, self.delimiter)
        self.data.append(flattened)

    def __repr__(self):
        res = ''
        for packet in self.data:
            res += repr(packet)
        return res



def validate_packet(input_packet):
    if not isinstance(input_packet, (dict, float, int, str)):
        raise TypeError(Template('Invalid packet: $p').substitute(p=input_packet))

def flatten_packet(input_packet, delimiter = '.'):
    validate_packet(input_packet)
    flattened = FlattenedPacket()
    stack = [{ 'obj': input_packet, 'prefix' : '' }]

    # Push nested objects onto stack until we have flattened keys
    while stack:
        current_obj, prefix = stack.pop().values()

        for key, value in current_obj.items() :
            flat_key = Template('$p$d$k').substitute(p=prefix, d=delimiter, k=key) if (prefix) else key

            if isinstance(value, dict):
                stack.append({ 'obj': value, prefix: flat_key  })
            else:
                flattened[flat_key] =  value
    return flattened

def flatten_packet_recursive(input_packet, prefix = '', delimiter = '.', validated_packet = False):
    if not validated_packet:
        validate_packet(input_packet)

    flattened = FlattenedPacket()

    for key, value in input_packet.items() :
        flat_key = Template('$p$d$k').substitute(p=prefix, d=delimiter, k=key) if (prefix) else key
        if isinstance(value, dict):
            flattened = { **flattened, **flatten_packet_recursive(value, flat_key, delimiter, True) }
        else:
            flattened[flat_key] =  value

    return flattened
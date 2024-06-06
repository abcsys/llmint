import abc

"""Expert-defined functions."""


class EDF(abc.ABC):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def schema(self) -> dict:
        pass

    @abc.abstractmethod
    def function(self, *args, **kwargs) -> any:
        pass


"""Color Conversion."""


class HSB2RGB(EDF):
    def __init__(self):
        self._schema = {
            "type": "function",
            "function": {
                "name": "hsb2rgb",
                "description": "Converts HSB color to RGB color.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "h": {
                            "type": "number",
                            "description": "Hue value",
                        },
                        "s": {
                            "type": "number",
                            "description": "Saturation value",
                        },
                        "b": {
                            "type": "number",
                            "description": "Brightness value",
                        },
                    },
                    "required": ["h", "s", "b"],
                },
            },
        }
        super().__init__()

    def schema(self):
        return self._schema

    def function(self, h, s, b):
        h = float(h) / 360.0
        s = float(s) / 100.0
        b = float(b) / 100.0

        if s == 0:
            r = g = b = b
        else:
            if h == 1:
                h = 0
            h *= 6
            i = int(h)
            f = h - i
            p = b * (1 - s)
            q = b * (1 - s * f)
            t = b * (1 - s * (1 - f))

            if i == 0:
                r, g, b = b, t, p
            elif i == 1:
                r, g, b = q, b, p
            elif i == 2:
                r, g, b = p, b, t
            elif i == 3:
                r, g, b = p, q, b
            elif i == 4:
                r, g, b = t, p, b
            elif i == 5:
                r, g, b = b, p, q

        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return (r, g, b)

# input format
TRANSITION_WAVENUMBER = 'T'
UNCERTAINTY = 'U'
BRANCH = 'B'
V1_UPPER = '1'
V2_UPPER = '2'
V3_UPPER = '3'
P_UPPER = 'P'
L_UPPER = 'L'
N_UPPER = 'N'
E_UPPER = 'E'  # e/f
J_UPPER = 'J'
V1_LOWER = 'a'
V2_LOWER = 'b'
V3_LOWER = 'c'
P_LOWER = 'p'
L_LOWER = 'l'
N_LOWER = 'n'
E_LOWER = 'e'  # e/f
J_LOWER = 'j'
TAG = 't'
USELESS = 'u'

NO_COLUMNS = 13  # number of columns


# to use this formatter, provide it with the input string and the format of the input string
# for example, you can have
# input_str = "1003e-0000e  P   1  7701.68960    -0.21   546          "
# input_format = "12L3Euablce B j T U u"


class Formatter:
    default_format_dict: dict = {
        TRANSITION_WAVENUMBER : "",
        UNCERTAINTY : "",
        BRANCH: "",
        V1_UPPER : "",
        V2_UPPER : "",
        V3_UPPER : "",
        V1_LOWER : "",
        V2_LOWER : "",
        V3_LOWER : "",
        P_UPPER : "", 
        L_UPPER : "", 
        N_UPPER : "", 
        E_UPPER : "", 
        J_UPPER : "", 
        P_LOWER : "", 
        L_LOWER : "", 
        N_LOWER : "", 
        E_LOWER : "", 
        J_LOWER : "", 
        TAG : "",
        USELESS: "",
    }
    output_format: str = r"T U P L N E J p l n e j t"

    def __init__(self, input_format: str, tag: str) -> None:
        self.reset(input_format, tag)

    def reset(self, input_format: str, tag: str) -> None:
        self.input_format: list[str] = input_format.strip().split()
        self.tag = tag

    def format(self, input_str: str) -> str:
        input_items: list[str] = input_str.strip().split()
        assert len(self.input_format) == len(input_items), "There is something wrong, either with the format, or with the input string."

        format_dict = Formatter.default_format_dict.copy()
        format_dict[TAG] = self.tag

        for (item_format, item) in zip(self.input_format, input_items):
            if len(item_format) == 1:
                format_dict[item_format] = item
            else:
                assert len(item_format) == len(item), "The format of quantum numbers is wrong!"
                for (qn, value) in zip(list(item_format), list(item)):
                    format_dict[qn] = value

        if not format_dict[P_UPPER]:
            v1_upper = int(format_dict[V1_UPPER])
            v2_upper = int(format_dict[V2_UPPER])
            v3_upper = int(format_dict[V3_UPPER])
            format_dict[P_UPPER] = str(2 * v1_upper + v2_upper + 4 * v3_upper)
        if not format_dict[P_LOWER]:
            v1_lower = int(format_dict[V1_LOWER])
            v2_lower = int(format_dict[V2_LOWER])
            v3_lower = int(format_dict[V3_LOWER])
            format_dict[P_LOWER] = str(2 * v1_lower + v2_lower + 4 * v3_lower)

        if not format_dict[J_UPPER] or not format_dict[J_LOWER]:
            assert format_dict[BRANCH], "The branch is not given!"
            branch = format_dict[BRANCH].upper()
            assert branch in ('P', 'R'), "The branch must be either P or R!"
            if not format_dict[J_UPPER]:
                j_lower = int(format_dict[J_LOWER])
                if branch == 'P':
                    format_dict[J_UPPER] = str(j_lower - 1)
                else:
                    format_dict[J_UPPER] = str(j_lower + 1)
            if not format_dict[J_LOWER]:
                j_upper = int(format_dict[J_UPPER])
                if branch == 'P':
                    format_dict[J_LOWER] = str(j_upper - 1)
                else:
                    format_dict[J_LOWER] = str(j_upper + 1)
        
        if not format_dict[N_UPPER] or not format_dict[N_LOWER]:
            pass

        output: str = " ".join([format_dict[item] for item in Formatter.output_format.split()])
        return output


def test() -> None:
    input_format = "12L3Euablce B j T U u"
    input_str = "1003e-0000e  P   1  7701.68960    -0.21   546          "
    formatter = Formatter(input_format, tag="tag")
    output = formatter.format(input_str)
    print(output)


if __name__ == "__main__":
    test()

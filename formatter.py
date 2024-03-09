from get_n import *

# input format
TRANSITION_WAVENUMBER = "T"
UNCERTAINTY = "U"
BRANCH = "B"
V1_UPPER = "1"
V2_UPPER = "2"
V3_UPPER = "3"
P_UPPER = "P"
L_UPPER = "L"
N_UPPER = "N"
E_UPPER = "E"  # e/f
J_UPPER = "J"
V1_LOWER = "a"
V2_LOWER = "b"
V3_LOWER = "c"
P_LOWER = "p"
L_LOWER = "l"
N_LOWER = "n"
E_LOWER = "e"  # e/f
J_LOWER = "j"
TAG = "t"
USELESS = "u"
OVER = "O"

DEFAULT_UNCERTAINTY = "0.01"


# to use this formatter, provide it with the input string and the format of the input string
# for example, you can have
# input_str = "1003e-0000e  P   1  7701.68960    -0.21   546          "
# input_format = "12L3Euablce B j T U u"


def is_valid(input_str: str) -> bool:
    for char in input_str:
        if char in ("h"):
            return False
        if not char.isalnum():
            if char not in ("-", " ", ".", "(", ")"):
                return False
    return True


class Formatter:
    default_format_dict: dict = {
        TRANSITION_WAVENUMBER: "",
        UNCERTAINTY: "",
        BRANCH: "",
        V1_UPPER: "",
        V2_UPPER: "",
        V3_UPPER: "",
        V1_LOWER: "",
        V2_LOWER: "",
        V3_LOWER: "",
        P_UPPER: "",
        L_UPPER: "",
        N_UPPER: "",
        E_UPPER: "",
        J_UPPER: "",
        P_LOWER: "",
        L_LOWER: "",
        N_LOWER: "",
        E_LOWER: "",
        J_LOWER: "",
        TAG: "",
        USELESS: "",
    }
    output_format: str = r"T U P L N E J p l n e j t"

    def __init__(self, input_format: str, tag: str) -> None:
        self.reset(input_format, tag)

    def reset(self, input_format: str, tag: str) -> None:
        self.input_format: list[str] = input_format.strip().split()
        if OVER in self.input_format:
            self.input_format.pop()
        self.tag = tag

    def format(self, input_str: str) -> str:
        input_items: list[str] = [
            item for item in input_str.strip().split() if is_valid(item)
        ][: len(self.input_format)]
        # try:
        #     assert len(self.input_format) == len(input_items), "There is something wrong, either with the format, or with the input string."
        # except AssertionError:
        #     print(len(self.input_format), len(input_items))
        #     print(self.input_format, input_items)
        #     raise AssertionError()
        assert len(self.input_format) == len(
            input_items
        ), "There is something wrong, either with the format, or with the input string."

        format_dict = Formatter.default_format_dict.copy()
        format_dict[TAG] = self.tag

        for item_format, item in zip(self.input_format, input_items):
            print(item_format, item)
            if len(item_format) == 1:
                format_dict[item_format] = item
            else:
                # assert len(item_format) == len(item), "The format of quantum numbers is wrong!"
                # for (qn, value) in zip(list(item_format), list(item)):
                #     format_dict[qn] = value
                if item_format[0] == BRANCH:
                    format_dict[BRANCH] = item[0]
                    format_dict[item_format[1]] = str(int(item[1:]))
                else:
                    i = 0
                    j = 0
                    while i < len(item_format):
                        if item[j] not in ("(", ")"):
                            format_dict[item_format[i]] = item[j]
                        elif item[j] == "(":
                            starting_pos = j + 1
                            while item[j] != ")":
                                j += 1
                            ending_pos = j
                            format_dict[item_format[i]] = item[starting_pos:ending_pos]
                        i += 1
                        j += 1
        print(format_dict)

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
            assert branch in ("P", "R", "Q"), "The branch must be either P, Q or R!"
            if not format_dict[J_UPPER]:
                j_lower = int(format_dict[J_LOWER])
                if branch == "P":
                    # j_upper = str(j_lower - 1)
                    # if j_upper == '0':
                    #     j_upper = max(format_dict[L_UPPER], '1')
                    # format_dict[J_UPPER] = j_upper
                    format_dict[J_UPPER] = str(j_lower - 1)
                elif branch == "R":
                    format_dict[J_UPPER] = str(j_lower + 1)
                else:
                    format_dict[J_UPPER] = str(j_lower)
            if not format_dict[J_LOWER]:
                j_upper = int(format_dict[J_UPPER])
                if branch == "P":
                    format_dict[J_LOWER] = str(j_upper + 1)
                elif branch == "R":
                    format_dict[J_LOWER] = str(j_upper - 1)
                else:
                    format_dict[J_LOWER] = str(j_upper)

        # if not format_dict[N_UPPER] or not format_dict[N_LOWER]:
        #     upper_v = tuple([format_dict[key] for key in [V1_UPPER, V2_UPPER, V3_UPPER]])
        #     assert "" not in upper_v
        #     lower_v = tuple([format_dict[key] for key in [V1_LOWER, V2_LOWER, V3_LOWER]])
        #     assert "" not in lower_v
        #     upper_jp = tuple([format_dict[key] for key in [J_UPPER, P_UPPER]])
        #     assert "" not in upper_jp
        #     lower_jp = tuple([format_dict[key] for key in [J_LOWER, P_LOWER]])
        #     assert "" not in upper_jp
        #     upper_e = format_dict[E_UPPER]
        #     lower_e = format_dict[E_LOWER]
        #     upper_n, lower_n = get_n(
        #         upper_v,
        #         lower_v,
        #         upper_jp,
        #         lower_jp,
        #         upper_e,
        #         lower_e,
        #     )
        #     format_dict[N_UPPER] = upper_n
        #     format_dict[N_LOWER] = lower_n

        # if not format_dict[N_UPPER] or not format_dict[N_LOWER]:
        #     upper_v = tuple([format_dict[key] for key in [V1_UPPER, V2_UPPER, V3_UPPER]])
        #     assert "" not in upper_v
        #     lower_v = tuple([format_dict[key] for key in [V1_LOWER, V2_LOWER, V3_LOWER]])
        #     assert "" not in lower_v
        #     upper_j = format_dict[J_UPPER]
        #     lower_j = format_dict[J_LOWER]
        #     upper_e = format_dict[E_UPPER]
        #     lower_e = format_dict[E_LOWER]
        #     upper_n, lower_n, upper_p, lower_p = get_np(
        #         upper_v,
        #         lower_v,
        #         upper_j,
        #         lower_j,
        #         upper_e,
        #         lower_e,
        #     )
        #     format_dict[N_UPPER] = upper_n
        #     format_dict[N_LOWER] = lower_n
        #     format_dict[P_UPPER] = upper_p
        #     format_dict[P_LOWER] = lower_p

        # if not format_dict[N_UPPER] or not format_dict[N_LOWER]:
        #     upper_v = tuple([format_dict[key] for key in [V1_UPPER, V2_UPPER, V3_UPPER]])
        #     assert "" not in upper_v
        #     lower_v = tuple([format_dict[key] for key in [V1_LOWER, V2_LOWER, V3_LOWER]])
        #     assert "" not in lower_v
        #     upper_e = format_dict[E_UPPER]
        #     lower_e = format_dict[E_LOWER]
        #     format_dict[N_LOWER] = '1'
        #     lower_n = format_dict[N_LOWER]
        #     upper_n, upper_p, lower_p = get_np_from_lower_n(
        #         upper_v,
        #         lower_v,
        #         upper_e,
        #         lower_e,
        #         lower_n,
        #     )
        #     format_dict[N_UPPER] = upper_n
        #     format_dict[P_UPPER] = upper_p
        #     format_dict[P_LOWER] = lower_p

        if format_dict[E_UPPER] == "1":
            format_dict[E_UPPER] = "e"
        elif format_dict[E_UPPER] == "2":
            format_dict[E_UPPER] = "f"
        else:
            raise ValueError("E_LOWER has to be 'e' or 'f'!")
        if format_dict[E_LOWER] == "1":
            format_dict[E_LOWER] = "e"
        elif format_dict[E_LOWER] == "2":
            format_dict[E_LOWER] = "f"
        else:
            raise ValueError("E_UPPER has to be 'e' or 'f'!")

        if not format_dict[N_LOWER]:
            if format_dict[E_LOWER] == "e":
                format_dict[N_LOWER] = "1"
            else:
                format_dict[N_LOWER] = "2"
            if not format_dict[N_UPPER]:
                format_dict[N_UPPER] = r"{}"

        if not format_dict[UNCERTAINTY]:
            format_dict[UNCERTAINTY] = DEFAULT_UNCERTAINTY

        output: str = " ".join(
            [format_dict[item] for item in Formatter.output_format.split()]
        )
        return output


def test() -> None:
    input_format = "12L3Euablce B j T U O"
    input_str = "1003e-0000e  P   1  7701.68960    -0.21  546          "
    formatter = Formatter(input_format, tag="tag")
    output = formatter.format(input_str)
    print(output)


if __name__ == "__main__":
    test()

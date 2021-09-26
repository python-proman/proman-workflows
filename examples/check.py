from textwrap import dedent


def get_values(var: str) -> None:
    print(var)


get_values(
    dedent(
        """\
        abc
        def
        ghi
        """
    )
)

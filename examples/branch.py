import re

pattern = r"""
    ^(?P<type>dev|feat|fix|rc|release)
    (?:
        [/_-]?
        (?P<name>[A-Za-z]\w+)
    )
    (?:
        [/_-]?
        (?P<id>\d+)
    )?$
"""
search = re.compile(pattern, re.VERBOSE | re.IGNORECASE)


def check_branch(branch: str) -> None:
    result = re.search(search, branch)

    if result:
        print(result.groups())
        print(result.group('type'), result.group('name'), result.group('id'))


check_branch('feat-check-123')
check_branch('feat/check-123')
check_branch('feat_123')

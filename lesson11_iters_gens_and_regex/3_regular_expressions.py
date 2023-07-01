import re

user_email = "user@gmail.com"


def validate_email(email_str):
    """ Way to validate email without regular expressions"""
    if "@" not in email_str:
        raise Exception(f"@ not in {email_str}")

    parts = email_str.split("@")
    assert len(parts) == 2, "More that one @"

    left, right = parts
    if "." not in right:
        raise Exception()

    right_parts = right.split(".")
    left1, right1 = right_parts
    if len(right1) not in (2, 3):
        raise Exception()

    # and a lot of another checks ...


# pattern for regular expression should be the "raw" string (prefix r before quotes)
regex_email_pattern = r"[a-zA-Z\d]+@[a-z]+.[a-z]{2,3}"
# it's better to compile regular expression once and then use it
regex_email = re.compile(regex_email_pattern)

# Check that email address is valid
result = regex_email.fullmatch(user_email)

if result:  # if email is fully matched with the pattern: result is re.Match object
    matched = result.group()  # returns the matched string
    assert matched == user_email
else:       # if email is NOT fully matched with the pattern: result is None
    print(f"{user_email} is NOT matched!")

# search the substring in source string using regex pattern:
re_search_result = re.search(r'@[a-z]+.', user_email)  # NOTE: search is stopped upon a first occurrence of matched substring
assert result is not None
print(re_search_result.group())


# findall: returns list of found substrings
m_count = re.findall('m', user_email)
assert len(m_count) == 2
u_count = re.findall('u', user_email)
assert len(u_count) == 1
r_count = re.findall('r', user_email)
assert len(r_count) == 1
ampersand_count = re.findall("&", user_email)
assert not ampersand_count  # equivalent to: len(ampersand_count) == 0

result = re.findall(r"[a-zA-Z]", user_email)
assert result == list(user_email.replace('@', '').replace('.', ''))
print(result)


# sub: replace the substring matched with pattern with specified string value
print(re.sub('user', 'resu', user_email))
# In real life for the case above it's better to use:
# print(user_email.replace('user', 'resu'))

assert re.sub(regex_email_pattern, '12345', user_email) == '12345'
assert re.sub(r'[a-z]', '0', user_email) == '0000@00000.000'

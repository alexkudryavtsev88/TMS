import re

regex_email_pattern = r"[a-zA-Z\d]+@[a-z]+.[a-z]{2,3}"
regex_email = re.compile(regex_email_pattern)

user_email = "user@gmail.com"
result = regex_email.fullmatch(user_email)
if result:
    print(result.group())

print(re.search(r'@', user_email).group())  # поиск до 1-го вхождения
print(re.findall(r'm', user_email))
print(re.sub('@', '-', user_email))



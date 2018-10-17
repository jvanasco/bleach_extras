import bleach
import bleach_extras

dangerous = """foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");</script>2</div>.bar"""

print(bleach.clean(dangerous, tags=['div', ], strip=False))
# foo.<div>1&lt;script&gt;alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg");&lt;/script&gt;2</div>.bar

print(bleach.clean(dangerous, tags=['div', ], strip=True))
# foo.<div>1alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");2</div>.bar

print(bleach_extras.clean_strip_content(dangerous, tags=['div'], ))
# foo.<div>12</div>.bar

cleaner = bleach_extras.cleaner_factory__strip_content(tags=['div'],)
print(cleaner.clean(dangerous))
# foo.<div>12</div>.bar

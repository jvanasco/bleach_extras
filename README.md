`bleach_extras` is a package of utilities paired for use with the `bleach` library.

The first utility is `TagTreeFilter` which is utilized by `clean_strip_content` and `cleaner_factory__strip_content`.

# `TagTreeFilter`, `clean_strip_content`, `cleaner_factory__strip_content`

`clean_strip_content` is paired to `bleach.clean`, and the only intended difference
is to support the concept of stripping the content of tags, and not just the
tag itself.  `cleaner_factory__strip_content` is a factory function used to create
configured `bleach.Cleaner` instances.

`bleach` has a `strip` flag that toggles the behavior of "unsafe" tags:

`strip = False` will render the tags as escaped HTML encodings, such as this replacement

	- foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");</script>2</div>.bar
	+ foo.<div>1&lt;script&gt;alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");&lt;/script&gt;2</div>.bar
	
`strip = True` will strip the tags, but leave the HTML within as plaintext:

	- foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");</script>2</div>.bar
	+ foo.<div>1alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");2</div>.bar

Many users of `bleach` want to remove both the tag and contents of unsafe tags for
a variety of reasons, such as:

* escaping the tags make the text safe, but unreadable
* leaving the tags' content without the tags negatively affects readability and comprehension
* leaving the tags' content allows a malicious user to still have some sort of fallback payload which is displayed

`clean_strip_content` is a function that mimics `bleach.clean` with a key difference:

* tags destined for content stripping are fed into a `Cleaner` instance as allowed
* the tags are stripped during the filter process via `TagTreeFilter`

An expected transformation is such:

	- foo.<div>1<script>alert("ur komputer hs VIRUS! Giv me ur BITCOIN in 24 hours! Wallet is: abdefg!");</script>2</div>.bar
	+ foo.12.bar

Look at that! all the evil payload is gone, including the bitcoin wallet address that f---- spammers tried to slip through.

## Why do this filtering with `bleach` and not something else ?

Parsing/Tokenzing HTML is not very efficient. Performing this outside of `bleach` would require performing these operations on the HTML fragments at least twice.

`bleach`'s design implementation encodes/strips 'unsafe' tags during the parsing/tokening process - before the plugin filtering process starts. In order to filter the tags out correctly, they must be allowed during the generation of the dom tree, then removed during the filter step. This trips a lot of people up; offering this in a public library with tests that can grow is ideal.


Example::

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

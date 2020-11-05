import find

class TestFind:
	
	def test_get_word(self):
	    assert find.get_word("test", "test/09][],..,-*/") == "test"

	def test_get_get_soundex_code(self):
		assert find.get_soundex_code("test") == "T234"
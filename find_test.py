import find

class TestFind:
	
	def test_get_get_soundex_code(self):
		assert find.get_soundex_code("test") == "T230"
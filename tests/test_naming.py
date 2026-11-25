from renamer import naming


def test_is_number():
    assert naming.is_number('12')
    assert not naming.is_number('a1')
    assert not naming.is_number('')


def test_parse_int():
    assert naming.parse_int('5', 1) == 5
    assert naming.parse_int('x', 1) == 1
    assert naming.parse_int('-2', 0, minimum=0) == 0
    assert naming.parse_int('-2', 0) == -2


def test_short_name():
    assert naming.short_name('|grp|geo') == 'geo'
    assert naming.short_name('geo') == 'geo'


def test_remove_first_last_keep_one_char():
    assert naming.remove_first('abcd', 2) == 'cd'
    assert naming.remove_last('abcd', 2) == 'ab'
    assert naming.remove_first('abc', 3) == 'abc'
    assert naming.remove_last('abc', 0) == 'abc'


def test_affixes():
    assert naming.add_prefix('a', 'pre') == 'pre_a'
    assert naming.add_prefix('a', '12') == 'a'
    assert naming.add_suffix('a', 'suf') == 'a_suf'
    assert naming.add_suffix('a', '') == 'a'


def test_padding():
    assert naming.add_padding('a', 3, 4) == 'a_0003'
    assert naming.add_padding('a', 12345, 4) == 'a_12345'
    assert naming.add_padding('a', 3, 0) == 'a_3'


def test_parse_int_whitespace_and_empty():
    assert naming.parse_int(' 7 ', 1) == 7
    assert naming.parse_int('', 9) == 9

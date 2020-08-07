from utils import normalize_path

# обязательно должно начинаться с test
def test_normalized_path():

    norm_data = ["/", "hello", "hello/", ]
    expected_data = ["/", "hello/", "hello/", ]

    for i in range(3):
        t = norm_data[i]
        e = expected_data[i]
        got = normalize_path(t)
        assert got == e, f"path '{t}', normalized to '{got}', while '{e}' expected"




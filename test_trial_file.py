import trial_file

def test_increase():
    assert trial_file.increase(5) == 6

def test_title():
    assert trial_file.title() == 'Hello Word !'
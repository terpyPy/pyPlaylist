import  playlistV2  # The code to test

def test_increment():
    assert playlistV2.UI.buttonFunction('help')

def test_decrement():
    assert playlistV2.decrement(3) == 4
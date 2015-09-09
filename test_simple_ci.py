from PIL.Image import Image

import simple_ci


def test_draw_badge():
    '''Test to ensure drawing an image works as expected'''
    assert isinstance(simple_ci.draw_pin('Hi!'), Image)


def test_pin():
    '''Test to ensure pin transformer works as expected'''
    assert isinstance(simple_ci.pin(True), Image)
    assert isinstance(simple_ci.pin(False), Image)
    assert isinstance(simple_ci.pin(simple_ci.NOT_FOUND), Image)
    assert isinstance(simple_ci.pin(None), Image)

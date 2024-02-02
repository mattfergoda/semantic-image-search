from image_utils import scrape_exif

def test_scrape_exif():
    """Test getting exif data from an image with exif data."""

    with open("tests/images/Fujifilm_FinePix_E500.jpg", "rb") as image:
        exif = scrape_exif(image)

    assert exif == {
            'ResolutionUnit': 2,
            'ExifOffset': 266, 
            'Make': 'FUJIFILM', 
            'Model': 'FinePix E500   ', 
            'Software': 'GIMP 2.4.5', 
            'Orientation': 1, 
            'DateTime': '2008:07:31 16:49:10', 
            'YCbCrPositioning': 2, 
            'Copyright': '    ', 
            'XResolution': 96.0, 
            'YResolution': 96.0
    }

def test_scrape_exif_no_exif():
    """Test getting exif data from an image without exif data."""

    with open("tests/images/pexels-mikhail-nilov-8297845.jpg", "rb") as image:
        exif = scrape_exif(image)

    assert exif == {}
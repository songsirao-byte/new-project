from travel_pack_tool import TravelProfile, build_pack_list, clothing_count


def test_clothing_count_short_trip():
    counts = clothing_count(3)
    assert counts["Tops"] == 4
    assert counts["Bottoms"] == 2
    assert counts["Sleepwear"] == 1


def test_clothing_count_long_trip_caps_values():
    counts = clothing_count(20)
    assert counts["Tops"] == 10
    assert counts["Underwear"] == 12
    assert counts["Socks"] == 12
    assert counts["Sleepwear"] == 2


def test_build_pack_list_includes_activity_and_weather():
    profile = TravelProfile(
        destination="Tokyo",
        days=5,
        climate="rainy",
        trip_type="business",
        activities=["photography", "gym", "photography"],
    )

    pack = build_pack_list(profile)

    assert "Waterproof jacket" in pack["weather_specific"]
    assert "Laptop + charger" in pack["trip_specific"]
    assert "Camera" in pack["activity_specific"]
    assert pack["activity_specific"].count("Camera") == 1

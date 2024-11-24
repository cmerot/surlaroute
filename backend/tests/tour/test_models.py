from app.tour import models


def test_tour_model() -> None:
    tour = models.Tour()
    event = models.Event(tour=tour)
    print(event)
    assert 1 == 2

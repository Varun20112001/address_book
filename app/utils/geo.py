"""Geospatial utility helpers."""

from geopy.distance import geodesic


def is_within_distance(
    origin_lat: float,
    origin_lng: float,
    target_lat: float,
    target_lng: float,
    max_distance_km: float,
) -> bool:
    """Return whether target coordinates are within max_distance_km of origin."""
    distance = geodesic((origin_lat, origin_lng), (target_lat, target_lng)).kilometers
    return distance <= max_distance_km

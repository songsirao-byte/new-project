#!/usr/bin/env python3
"""AI-inspired travel packing list generator (offline heuristic)."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TravelProfile:
    destination: str
    days: int
    climate: str
    trip_type: str
    activities: List[str]


BASE_ITEMS: Dict[str, List[str]] = {
    "documents": [
        "Passport/ID",
        "Visa (if required)",
        "Travel insurance card",
        "Flight/train tickets",
        "Hotel booking confirmations",
        "Credit/debit cards + small cash",
    ],
    "electronics": [
        "Phone + charger",
        "Power bank",
        "Universal travel adapter",
        "Headphones",
    ],
    "toiletries": [
        "Toothbrush + toothpaste",
        "Shampoo / body wash (travel size)",
        "Skincare basics",
        "Prescription medications",
    ],
}

CLIMATE_ITEMS: Dict[str, List[str]] = {
    "cold": ["Down jacket", "Thermal base layer", "Gloves", "Scarf", "Beanie"],
    "temperate": ["Light jacket", "Long sleeve tops", "Comfortable pants"],
    "hot": ["Breathable T-shirts", "Shorts", "Sun hat", "Sunglasses", "Sunscreen"],
    "rainy": ["Waterproof jacket", "Compact umbrella", "Quick-dry socks", "Water-resistant shoes"],
}

TRIP_TYPE_ITEMS: Dict[str, List[str]] = {
    "business": ["Business attire", "Laptop + charger", "Portable mouse", "Notebook + pen"],
    "leisure": ["Casual outfits", "Comfortable walking shoes", "Daypack"],
    "adventure": ["Hiking shoes", "Quick-dry clothing", "Reusable water bottle", "First-aid kit"],
}

ACTIVITY_ITEMS: Dict[str, List[str]] = {
    "beach": ["Swimwear", "Flip-flops", "After-sun lotion"],
    "hiking": ["Trekking poles", "Trail snacks", "Blister pads"],
    "formal_dinner": ["Formal outfit", "Dress shoes"],
    "gym": ["Workout clothes", "Training shoes"],
    "photography": ["Camera", "Extra memory card", "Camera batteries"],
}


def clothing_count(days: int) -> Dict[str, int]:
    tops = min(days + 1, 10)
    bottoms = max(2, (days + 2) // 3)
    underwear = min(days + 1, 12)
    socks = min(days + 1, 12)
    sleepwear = 1 if days <= 4 else 2
    return {
        "Tops": tops,
        "Bottoms": bottoms,
        "Underwear": underwear,
        "Socks": socks,
        "Sleepwear": sleepwear,
    }


def build_pack_list(profile: TravelProfile) -> Dict[str, List[str]]:
    result = {key: items.copy() for key, items in BASE_ITEMS.items()}

    result["clothing_core"] = [f"{k}: {v}" for k, v in clothing_count(profile.days).items()]

    result["weather_specific"] = CLIMATE_ITEMS.get(profile.climate, []).copy()
    result["trip_specific"] = TRIP_TYPE_ITEMS.get(profile.trip_type, []).copy()

    activity_items: List[str] = []
    for activity in profile.activities:
        activity_items.extend(ACTIVITY_ITEMS.get(activity, []))

    if activity_items:
        # preserve order while removing duplicates
        seen = set()
        deduped = []
        for item in activity_items:
            if item not in seen:
                deduped.append(item)
                seen.add(item)
        result["activity_specific"] = deduped

    result["smart_tips"] = [
        f"Destination: {profile.destination}",
        "Roll clothes to save space.",
        "Keep one emergency outfit in carry-on.",
        "Pack liquids in a clear zip bag.",
    ]

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI travel pack list tool")
    parser.add_argument("--destination", required=True, help="Trip destination")
    parser.add_argument("--days", required=True, type=int, help="Trip duration in days")
    parser.add_argument(
        "--climate",
        required=True,
        choices=sorted(CLIMATE_ITEMS.keys()),
        help="Expected climate",
    )
    parser.add_argument(
        "--trip-type",
        required=True,
        choices=sorted(TRIP_TYPE_ITEMS.keys()),
        help="Type of trip",
    )
    parser.add_argument(
        "--activities",
        default="",
        help="Comma-separated activities from: " + ", ".join(sorted(ACTIVITY_ITEMS.keys())),
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "json"],
        help="Output format",
    )
    return parser.parse_args()


def format_markdown(pack_list: Dict[str, List[str]]) -> str:
    lines = ["# AI Travel Pack List", ""]
    for category, items in pack_list.items():
        lines.append(f"## {category.replace('_', ' ').title()}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    args = parse_args()
    activities = [a.strip() for a in args.activities.split(",") if a.strip()]

    profile = TravelProfile(
        destination=args.destination,
        days=args.days,
        climate=args.climate,
        trip_type=args.trip_type,
        activities=activities,
    )

    pack_list = build_pack_list(profile)
    if args.format == "json":
        print(json.dumps(pack_list, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(pack_list), end="")


if __name__ == "__main__":
    main()

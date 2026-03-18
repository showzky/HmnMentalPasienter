#!/usr/bin/env python3
"""
Simple script to sync clicker achievements from JSON to database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Achievement, GAME_ACHIEVEMENTS

def sync_achievements():
    with app.app_context():
        print("Syncing clicker achievements...")
        added = 0
        
        for ach in GAME_ACHIEVEMENTS:
            ach_id = ach["id"]
            exists = Achievement.query.get(ach_id)
            if not exists:
                new_ach = Achievement(
                    id=ach_id,
                    name=ach.get("name", ach_id),
                    description=ach.get("desc", ""),
                    icon=ach.get("icon", ""),
                    rarity=ach.get("rarity", "common"),
                    glow_color=ach.get("glow_color", "#fff"),
                    condition_type="clicker",
                    condition_value=ach.get("value", 0)
                )
                db.session.add(new_ach)
                added += 1
                print(f"  Adding: {ach_id}")
            else:
                print(f"  Already exists: {ach_id}")
        
        db.session.commit()
        print(f"✅ Done! Added {added} new achievements.")

if __name__ == "__main__":
    sync_achievements() 
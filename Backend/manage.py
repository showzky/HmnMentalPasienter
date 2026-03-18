from app import app, db, Achievement, GAME_ACHIEVEMENTS
import click
from flask.cli import with_appcontext

@app.cli.command("sync-clicker-achievements")
@with_appcontext
def sync_clicker_achievements():
    """Sync clicker achievements from JSON to the database."""
    added = 0
    for ach in GAME_ACHIEVEMENTS:
        ach_id = ach["id"]
        exists = Achievement.query.get(ach_id)
        if not exists:
            new_ach = Achievement(
                id=ach_id,
                name=ach.get("title", ach_id),
                description=ach.get("description", ""),
                icon=ach.get("icon", ""),
                rarity=ach.get("rarity", "common"),
                glow_color=ach.get("glow_color", "#fff"),
                condition_type="clicker",
                condition_value=ach.get("value", 0)
            )
            db.session.add(new_ach)
            added += 1
    db.session.commit()
    click.echo(f"✅ Synced! {added} new clicker achievements added to the database.")

@app.cli.command("cleanup-clicker-achievements")
@with_appcontext
def cleanup_clicker_achievements():
    """Remove clicker achievements from DB that are no longer in the JSON."""
    json_ids = {ach["id"] for ach in GAME_ACHIEVEMENTS}
    db_achievements = Achievement.query.filter_by(condition_type="clicker").all()
    removed = 0
    for ach in db_achievements:
        if ach.id not in json_ids:
            db.session.delete(ach)
            removed += 1
    db.session.commit()
    click.echo(f"🗑️ Removed {removed} clicker achievements from the database that are not in the JSON.")
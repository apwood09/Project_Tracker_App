from datetime import datetime, timezone

from .extensions import db


class Item(db.Model):
    """Placeholder model. Rename or replace to suit your domain."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Item {self.id} {self.name!r}>"

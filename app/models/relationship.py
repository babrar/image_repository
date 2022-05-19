from ..db import db

# Represents a junction table to represent the
# many-to-many relationship between image and tags
image_tags = db.Table(
    "image_tags",
    db.Column("image_id", db.ForeignKey("images.id")),
    db.Column("tag_id", db.ForeignKey("tags.id")),
    db.PrimaryKeyConstraint("image_id", "tag_id"),
)

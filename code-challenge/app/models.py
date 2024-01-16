from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    super_name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')

    def __repr__(self):
        return f"Hero('{self.name}')"


class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"
    serialize_rules = ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("description")
    def validate_description(self, key, description):
        assert len(
            description) >= 20, "Description must be at least 20 characters long"
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey(
        "powers.id"), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)

    power = db.relationship("Power", backref="hero_powers")

    @validates("strength")
    def validate_strength(self, key, strength):
        assert strength in ["Strong", "Weak",
                            "Average"], "Invalid strength value"
        return strength

    def __repr__(self):
        return f"HeroPower(hero_id={self.hero_id}, power_id={self.power_id}, strength={self.strength})"

from sqlalchemy import Column, Integer, String, Enum, DateTime
from bot.database.db import Base
import enum
from datetime import datetime, timedelta

# Enum для статусу підписки
class SubscriptionStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.INACTIVE)
    expiration_date = Column(DateTime, nullable=True)
    invite_link = Column(String, nullable=True)  # Додаємо поле для запрошення

    def activate(self):
        self.status = SubscriptionStatus.ACTIVE
        self.expiration_date = datetime.utcnow() + timedelta(days=1)  # Підписка діє 1 день

    def deactivate(self):
        self.status = SubscriptionStatus.INACTIVE
        self.expiration_date = None
        self.invite_link = None

    def is_active(self):
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.expiration_date and self.expiration_date < datetime.utcnow():
            self.deactivate()  # Якщо термін дії минув, деактивуємо підписку
            return False
        return True

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, status={self.status.value}, expiration={self.expiration_date}, invite_link={self.invite_link})>"
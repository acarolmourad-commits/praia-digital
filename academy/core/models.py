from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from academy.core.database import Base
import enum

class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"
    support = "support"

class EnrollmentStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    refunded = "refunded"
    cancelled = "cancelled"

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class OrderStatus(str, enum.Enum):
    open = "open"
    paid = "paid"
    cancelled = "cancelled"
    refunded = "refunded"

class ContentType(str, enum.Enum):
    text = "text"
    video = "video"
    audio = "audio"
    pdf = "pdf"

class LessonStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(40), nullable=True)
    avatar = Column(String(500), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.student)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    enrollments = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    carts = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(300), nullable=True)
    headline = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    level = Column(String(80), nullable=True)
    duration = Column(String(80), nullable=True)
    price = Column(Integer, nullable=True)
    currency = Column(String(10), nullable=False, default="BRL")
    status = Column(String(20), nullable=False, default="draft")
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan", order_by="Module.order")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="course", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="course", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="course", cascade="all, delete-orphan")
    upsell_triggers = relationship("UpsellRule", foreign_keys="UpsellRule.trigger_course_id", cascade="all, delete-orphan")
    upsell_targets = relationship("UpsellRule", foreign_keys="UpsellRule.target_course_id", cascade="all, delete-orphan")
    cross_sell_triggers = relationship("CrossSellRule", foreign_keys="CrossSellRule.trigger_course_id", cascade="all, delete-orphan")
    cross_sell_targets = relationship("CrossSellRule", foreign_keys="CrossSellRule.target_course_id", cascade="all, delete-orphan")

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    content_type = Column(Enum(ContentType), nullable=False, default=ContentType.text)
    content_url = Column(String(500), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    module = relationship("Module", back_populates="lessons")
    progresses = relationship("Progress", back_populates="lesson", cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.active)
    access_until = Column(DateTime(timezone=True), nullable=True)
    source = Column(String(40), nullable=False, default="checkout")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    progresses = relationship("Progress", back_populates="enrollment", cascade="all, delete-orphan")
    certificate = relationship("Certificate", back_populates="enrollment", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_enrollment_user_course"),)

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(LessonStatus), nullable=False, default=LessonStatus.not_started)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    enrollment = relationship("Enrollment", back_populates="progresses")
    lesson = relationship("Lesson", back_populates="progresses")

    __table_args__ = (UniqueConstraint("enrollment_id", "lesson_id", name="uq_progress_enrollment_lesson"),)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    gateway = Column(String(40), nullable=False)
    gateway_payment_id = Column(String(200), nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    amount = Column(Integer, nullable=False)
    currency = Column(String(10), nullable=False, default="BRL")
    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")
    course = relationship("Course", back_populates="payments")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.open)
    subtotal = Column(Integer, nullable=False, default=0)
    discount = Column(Integer, nullable=False, default=0)
    total = Column(Integer, nullable=False, default=0)
    currency = Column(String(10), nullable=False, default="BRL")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="items")
    course = relationship("Course", back_populates="order_items")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="carts")
    course = relationship("Course")
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_cart_user_course"),)

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False, unique=True)
    code = Column(String(120), nullable=False, unique=True, index=True)
    pdf_url = Column(String(500), nullable=True)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
    enrollment = relationship("Enrollment", back_populates="certificate")

class UpsellRule(Base):
    __tablename__ = "upsell_rules"

    id = Column(Integer, primary_key=True, index=True)
    trigger_course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    target_course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    discount_percent = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CrossSellRule(Base):
    __tablename__ = "cross_sell_rules"

    id = Column(Integer, primary_key=True, index=True)
    trigger_course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    target_course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    discount_percent = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(80), nullable=False, unique=True, index=True)
    type = Column(String(20), nullable=False, default="percent")
    value = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    valid_from = Column(DateTime(timezone=True), nullable=True)
    valid_to = Column(DateTime(timezone=True), nullable=True)
    usage_limit = Column(Integer, nullable=True)
    usage_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(80), nullable=False, unique=True)
    subject = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(80), nullable=False)
    channel = Column(String(20), nullable=False, default="email")
    template_id = Column(Integer, ForeignKey("email_templates.id", ondelete="SET NULL"), nullable=True)
    delay_minutes = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

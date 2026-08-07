from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from academy.core.models import UserRole, EnrollmentStatus, PaymentStatus, OrderStatus, ContentType, LessonStatus

# Auth
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    status: str
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True

# Courses
class ModuleOut(BaseModel):
    id: int
    order: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True

class LessonOut(BaseModel):
    id: int
    order: int
    title: str
    content_type: ContentType
    content_url: Optional[str]
    duration_minutes: Optional[int]

    class Config:
        from_attributes = True

class CourseOut(BaseModel):
    id: int
    slug: str
    title: str
    subtitle: Optional[str]
    headline: Optional[str]
    description: Optional[str]
    level: Optional[str]
    duration: Optional[str]
    price: Optional[int]
    currency: str
    status: str
    published_at: Optional[datetime]
    modules: List[ModuleOut] = []

    class Config:
        from_attributes = True

# Enrollment / Progress
class EnrollmentOut(BaseModel):
    id: int
    course_id: int
    status: EnrollmentStatus
    access_until: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressOut(BaseModel):
    id: int
    lesson_id: int
    status: LessonStatus
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

# Cart / Order / Payment
class CartItemIn(BaseModel):
    course_id: int

class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    subtotal: int
    discount: int
    total: int
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentIn(BaseModel):
    course_id: int
    gateway: str
    gateway_payment_id: Optional[str] = None

class PaymentOut(BaseModel):
    id: int
    course_id: int
    gateway: str
    status: PaymentStatus
    amount: int
    paid_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# Coupons
class CouponOut(BaseModel):
    id: int
    code: str
    type: str
    value: int
    active: bool
    valid_from: Optional[datetime]
    valid_to: Optional[datetime]
    usage_limit: Optional[int]
    usage_count: int

    class Config:
        from_attributes = True

# Upsell / Cross-sell
class RecommendationOut(BaseModel):
    course_id: int
    title: str
    slug: str
    price: Optional[int]
    discount_percent: int
    reason: str

# Leads
class LeadIn(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = None
    magnet: Optional[str] = None

class LeadOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    source: Optional[str]
    magnet: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class LeadEventOut(BaseModel):
    id: int
    lead_id: int
    event: str
    payload: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

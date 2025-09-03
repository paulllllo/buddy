"""
Rate limiting middleware for onboarding endpoints.
Different limits for different types of operations.
"""
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
import time
import asyncio
from collections import defaultdict

# In-memory rate limit storage (use Redis in production)
rate_limit_storage: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))

class RateLimiter:
    """Rate limiter for onboarding endpoints"""
    
    # Rate limit configurations
    RATE_LIMITS = {
        "session_validation": {"requests": 10, "window": 60},  # 10 requests per minute
        "progress_updates": {"requests": 30, "window": 60},    # 30 requests per minute
        "file_uploads": {"requests": 5, "window": 60},        # 5 uploads per minute
        "general": {"requests": 100, "window": 60}            # 100 requests per minute
    }
    
    @staticmethod
    def get_rate_limit_key(request: Request, session_token: str) -> str:
        """Generate rate limit key based on endpoint and session token"""
        path = request.url.path
        
        if "progress" in path or "complete" in path:
            return f"progress_updates:{session_token}"
        elif "uploads" in path:
            return f"file_uploads:{session_token}"
        elif "session" in path and request.method == "GET":
            return f"session_validation:{session_token}"
        else:
            return f"general:{session_token}"
    
    @staticmethod
    def is_rate_limited(key: str, limit_type: str) -> bool:
        """Check if request is rate limited"""
        now = time.time()
        window = RateLimiter.RATE_LIMITS[limit_type]["window"]
        max_requests = RateLimiter.RATE_LIMITS[limit_type]["requests"]
        
        # Clean old entries
        rate_limit_storage[key] = [
            timestamp for timestamp in rate_limit_storage[key]
            if now - timestamp < window
        ]
        
        # Check if limit exceeded
        if len(rate_limit_storage[key]) >= max_requests:
            return True
        
        # Add current request
        rate_limit_storage[key].append(now)
        return False
    
    @staticmethod
    def get_remaining_requests(key: str, limit_type: str) -> int:
        """Get remaining requests for the current window"""
        now = time.time()
        window = RateLimiter.RATE_LIMITS[limit_type]["window"]
        max_requests = RateLimiter.RATE_LIMITS[limit_type]["requests"]
        
        # Clean old entries
        rate_limit_storage[key] = [
            timestamp for timestamp in rate_limit_storage[key]
            if now - timestamp < window
        ]
        
        return max(0, max_requests - len(rate_limit_storage[key]))

async def rate_limit_onboarding_middleware(request: Request, call_next):
    """Rate limiting middleware for onboarding endpoints"""
    
    # Only apply to onboarding endpoints
    if not request.url.path.startswith("/api/onboarding/"):
        return await call_next(request)
    
    # Extract session token from path
    path_parts = request.url.path.split("/")
    if len(path_parts) < 4:
        return await call_next(request)
    
    session_token = path_parts[3]  # /api/onboarding/{session_token}/...
    
    # Determine rate limit type
    path = request.url.path
    if "progress" in path or "complete" in path:
        limit_type = "progress_updates"
    elif "uploads" in path:
        limit_type = "file_uploads"
    elif "session" in path and request.method == "GET":
        limit_type = "session_validation"
    else:
        limit_type = "general"
    
    # Generate rate limit key
    key = f"{limit_type}:{session_token}"
    
    # Check rate limit
    if RateLimiter.is_rate_limited(key, limit_type):
        remaining_time = RateLimiter.RATE_LIMITS[limit_type]["window"]
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "limit_type": limit_type,
                "retry_after": remaining_time,
                "message": f"Too many {limit_type} requests. Please try again later."
            }
        )
    
    # Add rate limit headers to response
    response = await call_next(request)
    remaining_requests = RateLimiter.get_remaining_requests(key, limit_type)
    
    response.headers["X-RateLimit-Limit"] = str(RateLimiter.RATE_LIMITS[limit_type]["requests"])
    response.headers["X-RateLimit-Remaining"] = str(remaining_requests)
    response.headers["X-RateLimit-Reset"] = str(int(time.time() + RateLimiter.RATE_LIMITS[limit_type]["window"]))
    
    return response 
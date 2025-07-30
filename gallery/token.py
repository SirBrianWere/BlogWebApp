from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from datetime import timedelta
from django.utils.http import base36_to_int

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def __init__(self):
        super().__init__()
        self.timeout = 86400  # 24 hours in seconds


    # Ensure your _make_hash_value includes critical user fields
    def _make_hash_value(self, user, timestamp):
        # Add last_login to catch password changes
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            str(user.pk) + 
            user.password + 
            str(login_timestamp) + 
            str(timestamp) + 
            str(user.is_active)
        )
        
    def check_token(self, user, token):
            print(f"\n--- Token Validation Debug ---")
            print(f"User: {user.email} (Active: {user.is_active})")
            print(f"Token: {token}")
            valid = super().check_token(user, token)
            print(f"Token valid: {valid}")
            return valid
            
        # First verify token structure is valid
            if not super().check_token(user, token):
                print("FAILED: Basic token validation")
                return False
                
            try:
                ts_b36, _ = token.split("-")
                timestamp = base36_to_int(ts_b36)
                print(f"Token timestamp: {timestamp}")
            except (ValueError, AttributeError, TypeError) as e:
                print(f"FAILED: Token parsing - {e}")
                return False

            current_time = timezone.now().timestamp()
            time_diff = current_time - timestamp
            print(f"Current time: {current_time}")
            print(f"Time difference: {time_diff} seconds (max {self.timeout})")

            if time_diff > self.timeout:
                print("FAILED: Token expired")
                return False
                
            print("SUCCESS: Valid token")
            return True

password_reset_token = CustomPasswordResetTokenGenerator()
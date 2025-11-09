"""
Custom exceptions for the application
"""


class AttendanceBotException(Exception):
    """Base exception for attendance bot"""

    pass


class AlreadyCheckedInError(AttendanceBotException):
    """사용자가 이미 오늘 출석했을 때"""

    pass


class UserNotFoundError(AttendanceBotException):
    """사용자를 찾을 수 없을 때"""

    pass


class UserNotRegisteredError(AttendanceBotException):
    """사용자가 등록되지 않았을 때 (.출첵 필요)"""

    pass


class InvalidConfigError(AttendanceBotException):
    """잘못된 설정값"""

    pass

"""
CheckIn Handler - .출첵 명령어 핸들러
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.services.attendance_service import AttendanceService

router = Router()


@router.message(Command("출첵"))
async def check_in_handler(message: Message, attendance_service: AttendanceService):
    """출첵 명령어 핸들러"""
    result = await attendance_service.check_in(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Unknown",
    )

    if result["success"]:
        user = result["user"]
        score = result["score"]
        consecutive_days = result["consecutive_days"]
        is_new_user = result["is_new_user"]

        if is_new_user:
            await message.reply(
                f"🎉 <b>환영합니다!</b>\n\n"
                f"✅ 출석 체크 완료!\n"
                f"📅 연속 출석: {consecutive_days}일\n"
                f"🎁 획득 점수: {score}점\n"
                f"💰 총 점수: {user.total_score:,}점\n"
                f"💬 총 채팅 수: {user.chat_count:,}개\n\n"
                f"💡 이제 채팅할 때마다 랜덤 점수를 받을 수 있어요!"
            )
        else:
            await message.reply(
                f"✅ <b>출석 체크 완료!</b>\n\n"
                f"📅 연속 출석: {consecutive_days}일\n"
                f"🎁 획득 점수: {score}점 (기본 10 + 보너스 {score - 10})\n"
                f"💰 총 점수: {user.total_score:,}점\n"
                f"💬 총 채팅 수: {user.chat_count:,}개\n"
                f"📊 평균 점수/채팅: {user.average_score_per_chat}점"
            )
    else:
        await message.reply(f"❌ {result['error']}")

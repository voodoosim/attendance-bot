"""
UserInfo Handler - .내정보 명령어 핸들러
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.services.user_service import UserService

router = Router()


@router.message(Command("내정보"))
async def user_info_handler(message: Message, user_service: UserService):
    """내정보 명령어 핸들러"""
    result = await user_service.get_user_info(telegram_id=message.from_user.id)

    if not result["success"]:
        await message.reply(f"❌ {result['error']}")
        return

    user = result["user"]
    recent_attendances = result["recent_attendances"]
    top_jackpots = result["top_jackpots"]

    # 최근 출석 현황
    attendance_str = ""
    if recent_attendances:
        attendance_str = "\n".join(
            [
                f"  • {att.date.strftime('%m/%d')}: {att.score}점 ({att.consecutive_days}일 연속)"
                for att in recent_attendances[:5]
            ]
        )
    else:
        attendance_str = "  출석 기록이 없습니다"

    # 최고 잭팟 기록
    jackpot_str = ""
    if top_jackpots:
        jackpot_str = "\n".join(
            [
                f"  • {jp.base_score} x {jp.multiplier}배 = <b>{jp.final_score}점</b>"
                for jp in top_jackpots[:3]
            ]
        )
    else:
        jackpot_str = "  아직 잭팟이 없어요 😢"

    await message.reply(
        f"👤 <b>사용자 정보</b>\n\n"
        f"📅 <b>출석 현황</b>\n"
        f"  • 연속 출석: {user.consecutive_days}일\n"
        f"  • 총 출석: {user.total_attendance}일\n\n"
        f"💰 <b>점수 현황</b>\n"
        f"  • 총 점수: {user.total_score:,}점\n"
        f"  • 총 채팅 수: {user.chat_count:,}개\n"
        f"  • 평균 점수/채팅: {user.average_score_per_chat}점\n\n"
        f"🎰 <b>잭팟 기록</b>\n"
        f"  • 잭팟 횟수: {user.jackpot_count}회\n"
        f"  • 최고 잭팟: {user.max_jackpot}점\n\n"
        f"📝 <b>최근 출석 (최근 5일)</b>\n"
        f"{attendance_str}\n\n"
        f"🔥 <b>TOP 잭팟</b>\n"
        f"{jackpot_str}"
    )

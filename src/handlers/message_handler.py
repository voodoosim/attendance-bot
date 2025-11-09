"""
Message Handler - 일반 메시지 핸들러 (채팅 활동)
"""
from aiogram import F, Router
from aiogram.types import Message

from src.services.chat_activity_service import ChatActivityService

router = Router()


@router.message(F.text & ~F.text.startswith("/") & ~F.text.startswith("."))
async def message_handler(message: Message, chat_activity_service: ChatActivityService):
    """일반 메시지 핸들러 (채팅 활동 점수)"""
    result = await chat_activity_service.process_message(
        telegram_id=message.from_user.id, message_id=message.message_id
    )

    if not result:
        # 미등록 유저 무시
        return

    # 잭팟인 경우만 알림
    if result["is_jackpot"]:
        activity = result["activity"]
        user = result["user"]
        await message.reply(
            f"🎰 <b>잭팟!!</b> 🎰\n\n"
            f"🎲 기본 점수: {activity.base_score}점\n"
            f"✨ 배율: x{activity.multiplier}\n"
            f"💎 획득 점수: <b>{activity.final_score}점!</b>\n\n"
            f"💰 총 점수: {user.total_score:,}점\n"
            f"🎰 잭팟 횟수: {user.jackpot_count}회"
        )
    # 일반 메시지는 조용히 점수만 적립

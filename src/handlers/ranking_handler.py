"""
Ranking Handler - .랭킹 명령어 핸들러
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.core.use_cases.get_ranking_usecase import RankingType
from src.services.user_service import UserService

router = Router()


@router.message(Command("랭킹"))
async def ranking_handler(message: Message, user_service: UserService):
    """랭킹 명령어 핸들러 (점수 랭킹)"""
    result = await user_service.get_ranking(RankingType.SCORE, limit=10)

    if not result["users"]:
        await message.reply("아직 랭킹 데이터가 없습니다!")
        return

    # 랭킹 메시지 생성
    ranking_lines = []
    for idx, user in enumerate(result["users"], 1):
        if idx == 1:
            medal = "👑"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."

        ranking_lines.append(
            f"{medal} @{user.username or 'Unknown'} - "
            f"<b>{user.total_score:,}점</b> ({user.chat_count:,} 메시지)"
        )

    ranking_text = "\n".join(ranking_lines)

    await message.reply(f"🏆 <b>점수 랭킹 TOP 10</b>\n\n{ranking_text}")


@router.message(Command("채팅랭킹"))
async def chat_ranking_handler(message: Message, user_service: UserService):
    """채팅 랭킹 명령어 핸들러"""
    result = await user_service.get_ranking(RankingType.CHAT_COUNT, limit=10)

    if not result["users"]:
        await message.reply("아직 랭킹 데이터가 없습니다!")
        return

    ranking_lines = []
    for idx, user in enumerate(result["users"], 1):
        if idx == 1:
            medal = "👑"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."

        ranking_lines.append(
            f"{medal} @{user.username or 'Unknown'} - "
            f"<b>{user.chat_count:,} 메시지</b> ({user.total_score:,}점)"
        )

    ranking_text = "\n".join(ranking_lines)

    await message.reply(f"💬 <b>채팅 랭킹 TOP 10</b>\n\n{ranking_text}")


@router.message(Command("잭팟랭킹"))
async def jackpot_ranking_handler(message: Message, user_service: UserService):
    """잭팟 랭킹 명령어 핸들러"""
    result = await user_service.get_ranking(RankingType.JACKPOT, limit=10)

    if not result["users"]:
        await message.reply("아직 잭팟 기록이 없습니다!")
        return

    ranking_lines = []
    for idx, user in enumerate(result["users"], 1):
        if idx == 1:
            medal = "👑"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."

        ranking_lines.append(
            f"{medal} @{user.username or 'Unknown'} - "
            f"<b>{user.jackpot_count}회</b> (최고: {user.max_jackpot}점)"
        )

    ranking_text = "\n".join(ranking_lines)

    await message.reply(f"🎰 <b>잭팟 랭킹 TOP 10</b>\n\n{ranking_text}")


@router.message(Command("출석랭킹"))
async def attendance_ranking_handler(message: Message, user_service: UserService):
    """출석 랭킹 명령어 핸들러"""
    result = await user_service.get_ranking(RankingType.CONSECUTIVE_DAYS, limit=10)

    if not result["users"]:
        await message.reply("아직 출석 기록이 없습니다!")
        return

    ranking_lines = []
    for idx, user in enumerate(result["users"], 1):
        if idx == 1:
            medal = "👑"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."

        ranking_lines.append(
            f"{medal} @{user.username or 'Unknown'} - "
            f"<b>{user.consecutive_days}일 연속</b> (총 {user.total_attendance}일)"
        )

    ranking_text = "\n".join(ranking_lines)

    await message.reply(f"📅 <b>출석 랭킹 TOP 10</b>\n\n{ranking_text}")

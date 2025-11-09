"""
Stats Handler - 통계 명령어 핸들러
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.services.stats_service import StatsService

router = Router()


@router.message(Command("일일통계"))
async def daily_stats_handler(message: Message, stats_service: StatsService):
    """일일통계 명령어 핸들러"""
    result = await stats_service.get_daily_stats()

    if not result["success"]:
        await message.reply("❌ 통계를 가져올 수 없습니다.")
        return

    stats = result["stats"]

    # TOP 사용자 목록
    top_users_str = ""
    if stats.top_users:
        top_users_str = "\n".join(
            [
                f"  {i + 1}. @{user.username or 'Unknown'}: {user.total_score:,}점 ({user.chat_count:,} 메시지)"
                for i, user in enumerate(stats.top_users)
            ]
        )
    else:
        top_users_str = "  데이터가 없습니다"

    await message.reply(
        f"📊 <b>일일 통계</b> ({stats.date.strftime('%Y-%m-%d')})\n\n"
        f"👥 <b>활동 현황</b>\n"
        f"  • 활동 사용자: {stats.total_users}명\n"
        f"  • 출석한 사람: {stats.check_in_count}명\n\n"
        f"💬 <b>채팅 현황</b>\n"
        f"  • 총 메시지: {stats.total_messages:,}개\n"
        f"  • 총 획득 점수: {stats.total_score:,}점\n\n"
        f"🎰 <b>잭팟</b>\n"
        f"  • 잭팟 횟수: {stats.jackpot_count}회\n\n"
        f"🏆 <b>오늘의 TOP 3</b>\n"
        f"{top_users_str}"
    )


@router.message(Command("월통계"))
async def monthly_stats_handler(message: Message, stats_service: StatsService):
    """월통계 명령어 핸들러"""
    result = await stats_service.get_monthly_stats()

    if not result["success"]:
        await message.reply("❌ 통계를 가져올 수 없습니다.")
        return

    stats = result["stats"]

    # TOP 사용자 목록
    top_users_str = ""
    if stats.top_users:
        top_users_str = "\n".join(
            [
                f"  {i + 1}. @{user.username or 'Unknown'}: {user.total_score:,}점 ({user.chat_count:,} 메시지)"
                for i, user in enumerate(stats.top_users)
            ]
        )
    else:
        top_users_str = "  데이터가 없습니다"

    # 가장 활발했던 날
    most_active_str = "  데이터가 없습니다"
    if stats.most_active_date:
        most_active_str = (
            f"  {stats.most_active_date.strftime('%m/%d')}: "
            f"{stats.most_active_count:,}개 메시지"
        )

    await message.reply(
        f"📊 <b>월별 통계</b> ({stats.year}년 {stats.month}월)\n\n"
        f"👥 <b>활동 현황</b>\n"
        f"  • 활동 사용자: {stats.total_users}명\n"
        f"  • 총 출석 횟수: {stats.check_in_count}회\n\n"
        f"💬 <b>채팅 현황</b>\n"
        f"  • 총 메시지: {stats.total_messages:,}개\n"
        f"  • 총 획득 점수: {stats.total_score:,}점\n\n"
        f"🎰 <b>잭팟</b>\n"
        f"  • 잭팟 횟수: {stats.jackpot_count}회\n\n"
        f"🔥 <b>가장 활발했던 날</b>\n"
        f"{most_active_str}\n\n"
        f"🏆 <b>이번 달 TOP 5</b>\n"
        f"{top_users_str}"
    )

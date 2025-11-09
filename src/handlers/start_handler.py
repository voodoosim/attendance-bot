"""
Start Handler - /start 명령어 핸들러
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("시작"))
async def start_handler(message: Message):
    """시작 명령어 핸들러"""
    await message.reply(
        f"👋 <b>안녕하세요, {message.from_user.first_name}님!</b>\n\n"
        f"🎮 <b>출석 & 채팅 활동 봇</b>에 오신 것을 환영합니다!\n\n"
        f"📋 <b>주요 기능</b>\n"
        f"  • 출석 체크로 점수 획득\n"
        f"  • 채팅할 때마다 랜덤 점수 (1~6점)\n"
        f"  • 5% 확률로 잭팟 (1~7배 배율)\n"
        f"  • 랭킹 시스템\n\n"
        f"🎯 <b>시작하기</b>\n"
        f"  먼저 <b>/출첵</b> 명령어로 등록해주세요!\n\n"
        f"💡 <b>명령어 목록</b>\n"
        f"  /출첵 - 출석 체크\n"
        f"  /내정보 - 내 정보 보기\n"
        f"  /랭킹 - 점수 랭킹\n"
        f"  /채팅랭킹 - 채팅 수 랭킹\n"
        f"  /잭팟랭킹 - 잭팟 횟수 랭킹\n"
        f"  /출석랭킹 - 연속 출석 랭킹\n"
        f"  /도움말 - 상세 도움말"
    )


@router.message(Command("도움말"))
async def help_handler(message: Message):
    """도움말 명령어 핸들러"""
    await message.reply(
        f"📚 <b>출석 봇 사용 가이드</b>\n\n"
        f"🎯 <b>출석 시스템</b>\n"
        f"  • <b>/출첵</b> - 일일 출석 체크\n"
        f"  • 기본 점수: 10점\n"
        f"  • 연속 출석 보너스: +1~7점\n"
        f"  • 1일 1회만 가능 (자정 초기화)\n\n"
        f"💬 <b>채팅 보상</b>\n"
        f"  • 메시지마다 랜덤 점수: 1~6점\n"
        f"  • 잭팟 확률: 5% (1/20)\n"
        f"  • 잭팟 배율: 1~7배 랜덤\n"
        f"  • 예: 5점 x 7배 = 35점!\n"
        f"  • ⚠️ 출첵 등록 필수!\n\n"
        f"📊 <b>정보 조회</b>\n"
        f"  • <b>/내정보</b> - 내 통계 확인\n"
        f"  • 총 점수, 채팅 수, 잭팟 기록\n"
        f"  • 최근 출석 내역\n"
        f"  • TOP 잭팟 기록\n\n"
        f"🏆 <b>랭킹</b>\n"
        f"  • <b>/랭킹</b> - 점수 순위\n"
        f"  • <b>/채팅랭킹</b> - 채팅 수 순위\n"
        f"  • <b>/잭팟랭킹</b> - 잭팟 횟수 순위\n"
        f"  • <b>/출석랭킹</b> - 연속 출석 순위\n\n"
        f"💡 <b>팁</b>\n"
        f"  • 매일 출첵으로 연속 보너스 받기!\n"
        f"  • 채팅 많이 하면 잭팟 기회 증가!\n"
        f"  • 랭킹 1위를 노려보세요!"
    )

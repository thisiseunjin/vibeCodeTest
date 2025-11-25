#!/usr/bin/env python3
"""간단한 숫자 맞추기 게임 (1-100).

사용:
  python3 guess_game.py          # 대화형 플레이
  python3 guess_game.py --self-test  # 자동 확인(비대화형)
"""
import argparse
import random
import sys


MAX_ATTEMPTS = 5


def _hearts_status(attempts: int, max_attempts: int) -> str:
    """남은/사용한 하트 문자열 생성.

    - '❤️' : 남은 시도
    - '♡' : 이미 사용한 시도
    """
    used = attempts
    remaining = max_attempts - used
    # 이모지가 터미널에서 붙어 보이는 경우가 있어 각 이모지 사이에 공백을 추가합니다.
    hearts = ["❤️"] * remaining + ["♡"] * used
    return " ".join(hearts)


def play_interactive():
    secret = random.randint(1, 100)
    attempts = 0
    print("🎯 1부터 100 사이의 숫자를 맞춰보세요! (최대 5회)")
    while attempts < MAX_ATTEMPTS:
        # 현재 상태 출력 (남은 하트)
        print(f"💖 남은 기회: {_hearts_status(attempts, MAX_ATTEMPTS)}  (시도 {attempts}/{MAX_ATTEMPTS})")
        try:
            s = input(f"📝 {attempts + 1}번째 시도> ")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 게임을 종료합니다.")
            return 1
        s = s.strip()
        if not s:
            print("⚠️ 빈 입력입니다 — 정수를 입력하세요.")
            continue
        try:
            guess = int(s)
        except ValueError:
            print("❗ 정수가 아닙니다 — 숫자를 입력하세요.")
            continue
        if guess < 1 or guess > 100:
            print("🚫 범위는 1에서 100 사이입니다.")
            continue

        # 정답 검사
        if guess == secret:
            attempts += 1
            print(f"🎉 정답입니다! {attempts}번 만에 맞추셨습니다. 축하합니다! 🏆")
            return 0
        # 오답 처리
        attempts += 1
        if guess < secret:
            print("🔽 너무 낮습니다.")
        else:
            print("🔼 너무 높습니다.")

        # 기회 소진 체크
        if attempts >= MAX_ATTEMPTS:
            print(f"💔 기회를 모두 사용했습니다. 정답은 {secret}입니다. 다음에 도전하세요!")
            return 1


def self_test():
    # 셀프 테스트: 제한된 시도 안에서 하트 표시와 성공/실패 경로를 확인합니다.
    # 결정론적으로 secret을 작게 고정해 성공 경로를 테스트합니다.
    secret = 3
    guesses = [1, 2, 3, 4, 5]
    attempts = 0
    for g in guesses[:MAX_ATTEMPTS]:
        print(f"[self-test] 시도 {attempts + 1}/{MAX_ATTEMPTS} 남은: {_hearts_status(attempts, MAX_ATTEMPTS)}")
        if g == secret:
            attempts += 1
            print(f"[self-test] 🤖 secret={secret}, attempts={attempts} (성공)")
            return 0
        attempts += 1
    print(f"[self-test] ❌ 실패: secret={secret}를 {MAX_ATTEMPTS}회 내에 못 찾음")
    return 2


def main(argv=None):
    parser = argparse.ArgumentParser(description="숫자 맞추기 게임")
    parser.add_argument("--self-test", action="store_true", help="자동 비대화형 검사")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    return play_interactive()


if __name__ == "__main__":
    raise SystemExit(main())

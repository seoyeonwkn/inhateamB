from .models import Badge, UserBadge, BadgeLog, BadgeLevel
from question.models import Question
from answer.models import Answer

def check_and_award_badges(user):
    # 이미 보유한 뱃지 ID 집합
    owned_badges = set(
        UserBadge.objects.filter(user=user)
        .values_list('badge_id', flat=True)
    )
    # 모든 뱃지 순회
    badges = Badge.objects.all()

    for badge in badges:
        if badge.id in owned_badges:
            continue  # 이미 획득한 뱃지면 스킵

        # 호기심부자: 질문 올린 횟수 10개 이상
        elif badge.name == "호기심부자":
            q_count = Question.objects.filter(author=user).count()
            if q_count >= 10:
                level = BadgeLevel.objects.filter(badge=badge, level=1).first()
                ub = UserBadge.objects.create(user=user, badge=badge, level=level)
                BadgeLog.objects.create(user_badge=ub, reason="질문 10개 작성")
        
        # 사랑의 큐피트: 연애 카테고리 답변 채택 10회 이상
        elif badge.name == "사랑의 큐피트":
            a_count = Answer.objects.filter(
                user=user,
                is_accepted=True,
                question__category__name="연애"
            ).count()
            if a_count >= 10:
                level = BadgeLevel.objects.filter(badge=badge, level=1).first()
                ub = UserBadge.objects.create(user=user, badge=badge, level=level)
                BadgeLog.objects.create(user_badge=ub, reason="연애 카테고리 답변 채택 10회")

        # 파이썬 전문가 시리즈
        elif badge.name == "파이썬 전문가":
            a_count = Answer.objects.filter(
                user=user,
                is_accepted=True,
                question__category__name="파이썬"
            ).count()
            # 레벨 설정
            if   a_count >= 100: lvl, reason = 4, "파이썬 답변 채택 100회"
            elif a_count >= 50:  lvl, reason = 3, "파이썬 답변 채택 50회"
            elif a_count >= 20:  lvl, reason = 2, "파이썬 답변 채택 20회"
            elif a_count >= 5:   lvl, reason = 1, "파이썬 답변 채택 5회"
            else: continue
            level = BadgeLevel.objects.filter(badge=badge, level=lvl).first()
            ub = UserBadge.objects.create(user=user, badge=badge, level=level)
            BadgeLog.objects.create(user_badge=ub, reason=reason)

        # 냥냥 전문가 시리즈
        elif badge.name == "냥냥 전문가":
            a_count = Answer.objects.filter(
                user=user,
                is_accepted=True,
                question__category__name="고양이"
            ).count()
            if   a_count >= 70: lvl, reason = 4, "냥냥 답변 채택 70회"
            elif a_count >= 30: lvl, reason = 3, "냥냥 답변 채택 30회"
            elif a_count >= 10: lvl, reason = 2, "냥냥 답변 채택 10회"
            elif a_count >= 3:  lvl, reason = 1, "냥냥 답변 채택 3회"
            else: continue
            level = BadgeLevel.objects.filter(badge=badge, level=lvl).first()
            ub = UserBadge.objects.create(user=user, badge=badge, level=level)
            BadgeLog.objects.create(user_badge=ub, reason=reason)

        # (추가할 뱃지가 있으면, 여기에 계속 elif 블록을 이어 붙이기)

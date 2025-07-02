from .models import Badge, UserBadge, BadgeLog, BadgeLevel
from question.models import Question
from answer.models import Answer

def check_and_award_badges(user):
    """
    유저의 활동 내역을 기반으로 조건을 만족하는 뱃지를 찾아 자동 지급

    예: 답변 채택 시 check_and_award_badges 호출하면 됩니다.

    # answer/views.py 나 answer/models.py 에서
    from badge.utils import check_and_award_badges

    # 답변 채택 함수 안에서
    check_and_award_badges(answer.user)
    """

    # 이미 보유한 뱃지 목록
    owned_badges = set(UserBadge.objects.filter(user=user).values_list('badge_id', flat=True))

    # 전체 뱃지 목록
    badges = Badge.objects.all()

    for badge in badges:
        if badge.id in owned_badges:
            continue  # 이미 보유한 뱃지 skip

        # 아래에 뱃지별 조건을 추가하면 됩니다!
        if badge.name == "고양이 전문가":
            # 조건: 고양이 카테고리 질문 중 채택된 답변이 3개 이상
            count = Answer.objects.filter(
                user=user,
                is_accepted=True,
                question__category__name="고양이"
            ).count()
        
            if count >= 3:
                # 1. 지급할 뱃지레벨 선택 (조건에 따라)
                level = BadgeLevel.objects.filter(badge=badge, level=1).first()

                # 2. 지급
                user_badge = UserBadge.objects.create(
                    user=user,
                    badge=badge,
                    level=level  # Null 허용되므로 없어도 괜찮음
                )

                # 3. 지급 로그 남기기
                BadgeLog.objects.create(
                    user_badge=user_badge,
                    reason="고양이 카테고리 채택 답변 3회 이상"
                )

                print(f"{user.login_id}님, '{badge.name}' 뱃지를 획득했어요! (레벨: {level.title if level else '기본'})")


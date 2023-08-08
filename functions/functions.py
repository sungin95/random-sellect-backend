from users.models import User


def page_nation(page_size, page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    page_size = page_size
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)


# 로그인 유저와 user가 다르면 True를 보내 if 문이 실행되게 한다.
def user_not_equal(request_user: User, user: User) -> bool:
    if request_user != user:
        return True
    else:
        return False

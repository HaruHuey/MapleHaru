from django.db import models

# Create your models here.

class MapleDB(models.Model):
    # 생성 날짜
    created_at = models.DateTimeField(auto_now_add=True)

    # 메이플 유저 이름
    MapleName = models.CharField(max_length=50)

    # 서버 아이콘 URL
    ServerIconURL = models.CharField(max_length=500)

    # 길드 명
    GuildName = models.CharField(max_length=50)

    # 레벨
    MapleLevel = models.CharField(max_length=5)

    # 직업 정보
    MapleJob = models.CharField(max_length=50)

    # 서버 이름
    MapleServer = models.CharField(max_length=20)

    # 경험치
    MapleEXP = models.CharField(max_length=100)

    # 인기도
    MaplePopular = models.CharField(max_length=10)

    # 캐릭터 이미지 URL
    MapleCharIMG_URL = models.CharField(max_length=500)

    # 종합랭킹
    TotalRank = models.CharField(max_length=50)

    # 월드랭킹
    WorldRank = models.CharField(max_length=50)

    # 직업랭킹
    JobRank = models.CharField(max_length=50)
    
    # 인기도랭킹
    PopularRank = models.CharField(max_length=50)

    # 메이플 유니온 랭킹
    UnionRank = models.CharField(max_length=50)

    # 업적랭킹
    AchievementsRank = models.CharField(max_length=50)

    object = models.Manager()
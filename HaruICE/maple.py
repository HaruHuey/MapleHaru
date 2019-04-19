import json
import urllib.request
import re
from bs4 import BeautifulSoup
from pprint import pprint

# 넥슨 메이플에서 캐릭터 정보 검색
# 개선 필요 . 현재 코드는 함수 세번 호출로 속도가 저하됨
def NexonMaple(MapleName):
    # 넥슨 메이플스토리 랭킹 검색 페이지 URL
    NexonMapleData_URL = "https://maplestory.nexon.com/Ranking/World/Total?c="
    NexonMapleHome_URL = "https://maplestory.nexon.com"

    # 닉네임 Quote 변경
    MapleName = urllib.parse.quote(MapleName)

    # URL 합치기
    NexonMapleData_URL_N = NexonMapleData_URL + MapleName

    # 메이플스토리 랭킹 검색 페이지 열기
    Open_NexonMapleData_URL = urllib.request.urlopen(NexonMapleData_URL_N, timeout=10)
    # 메이플스토리 랭킹 검색 페이지 읽기
    Read_NexonMapleData_URL = Open_NexonMapleData_URL.read()

    # BeautifulSoup 에서 HTML 형식으로 파싱
    Maple_Soup = BeautifulSoup(Read_NexonMapleData_URL, "html.parser")

    # 메이플스토리 전적검색 정리 데이터
    Find_Maple = Maple_Soup.find(class_="search_com_chk")
    Find_Maple_td = Find_Maple.find_all("td")

    # 메이플스토리 전적검색 - 개인 프로필 링크 + 서버 아이콘
    Find_Maple_charLink = Find_Maple_td[1].find("dl").find("dt").find("a")

    # 메이플스토리 전적검색 - 개인 프로필 링크
    Find_Maple_charLink_Link = NexonMapleHome_URL + Find_Maple_charLink['href']

    # 메이플스토리 전적검색 - 서버 아이콘
    Find_Maple_charLink_SeverIcon = Find_Maple_charLink.img['src']

    # 메이플스토리 전적검색 - 길드 명
    try:
        Find_Maple_GuildName = Find_Maple_td[5].string
        if Find_Maple_GuildName == None:
            raise "길드 값이 없습니다."
        else:
            pass
        
    except:
        Find_Maple_GuildName = "- 내용 없음 -"

    # 함수 리턴 값 정보
    # HomeURL = 넥슨 메이플스토리 홈 URL
    # charLink = 메이플스토리 전적검색 - 개인 프로필 링크
    # ServerIcon = 서버 아이콘 @
    # GuildName = 길드 명 @
    return {"HomeURL": NexonMapleHome_URL, "charLink": Find_Maple_charLink_Link,
            "ServerIcon": Find_Maple_charLink_SeverIcon, "GuildName": Find_Maple_GuildName}

# 메이플스토리 정보검색 - 캐릭터 정보 / 기본 정보 / 링크 분산
def MapleNormalData(MapleName):
    # 함수 호출 - NexonMaple
    NexonMaple_def = NexonMaple(MapleName)

    # 메이플스토리 정보검색 - 개인 링크
    NexonNormal_MapleData_URL = NexonMaple_def["charLink"]

    # 메이플스토리 정보검색 링크 오픈
    Open_NormalMapleData = urllib.request.urlopen(NexonNormal_MapleData_URL, timeout=10)
    Read_NormalMapleData = Open_NormalMapleData.read()

    # BeautifulSoup 에서 HTML 형식으로 파싱
    Maple_Soup = BeautifulSoup(Read_NormalMapleData, "html.parser")

    # 파싱한 데이터 중 랭크의 링크를 가지고 있는 데이터를 가져온다
    Find_Maple_Rank = Maple_Soup.find(class_="lnb_list")
    Find_Maple_Rank = Find_Maple_Rank.find_all("li")[0]
    Find_Maple_Rank = Find_Maple_Rank.a["href"]

    # 메이플스토리 랭킹 정보 URL
    Maple_Rank_URL = NexonMaple_def["HomeURL"] + Find_Maple_Rank

    # 파싱한 데이터 중 char_info 클래스에 해당하는 데이터를 가져온다
    Find_Maple = Maple_Soup.find(class_="char_info")
    Find_Maple_dl = Find_Maple.find_all("dl")
    Find_Maple_div = Find_Maple.find_all("div")

    # 레벨 정보 dl[0]
    Find_MapleLevel = Find_Maple_dl[0].find("dd").string
    Find_MapleLevel = str(re.sub(r"LV.", "", str(Find_MapleLevel)))

    # 직업 정보 dl[1]
    Find_MapleJob = Find_Maple_dl[1].find("dd").string

    # 서버 정보 dl[2]
    Find_MapleServer = Find_Maple_dl[2].find("dd")
    Find_MapleServer = str(re.sub(r'<img.*/>', "", str(Find_MapleServer)))
    Find_MapleServer = Find_MapleServer.replace("<dd>", "").replace("</dd>", "")

    # 경험치 정보 div[0]
    Find_MapleEXP = Find_Maple_div[0].find_all("span")[0]
    Find_MapleEXP = str(re.sub(r'<em>.*</em>', "", str(Find_MapleEXP)))
    Find_MapleEXP = Find_MapleEXP.replace('<span>', "").replace('</span>', "")

    # 인기도 정보 div[0]
    Find_MaplePopular = Find_Maple_div[0].find_all("span")[1]
    Find_MaplePopular = str(re.sub(r'<em>.*</em>', "", str(Find_MaplePopular)))
    Find_MaplePopular = Find_MaplePopular.replace('<span class="pop_data">', "").replace('</span>', "")

    # 캐릭터 이미지 링크 div[1]
    Find_MapleCharIMG_URL = Find_Maple_div[1].find("img")["src"]

    # 함수 리턴 값 정보
    # * ServerIcon = 서버 아이콘 * NexonMaple["ServerIcon"] * 이전
    # * GuildName = 길드 명 * NexonMaple["GuildName"] * 이전

    # RankURL = 랭크 정보 URL
    # MapleLevel = 레벨 @
    # MapleJob = 직업 정보 @
    # MapleServer = 서버 이름 @
    # MapleEXP = 경험치 @
    # MaplePopular = 인기도 @
    # MapleCharIMG_URL = 캐릭터 이미지 URL @
    return {"RankURL": Maple_Rank_URL, "MapleLevel": Find_MapleLevel, "MapleJob": Find_MapleJob,
            "MapleServer": Find_MapleServer, "MapleEXP": Find_MapleEXP, "MaplePopular": Find_MaplePopular,
            "MapleCharIMG_URL": Find_MapleCharIMG_URL}

# 메이플스토리 정보검색 - 캐릭터 정보 / 랭킹 정보
def MapleRankingData(MapleName):
    # 메이플스토리 정보검색 - 일반 정보 함수
    MapleNormalData_def = MapleNormalData(MapleName)

    # 메이플스토리 랭킹 정보 URL 할당
    MapleRanking_URL = MapleNormalData_def["RankURL"]

    Open_MapleRanking = urllib.request.urlopen(MapleRanking_URL, timeout=10)
    Read_MapleRanking = Open_MapleRanking.read()

    Maple_RankSoup = BeautifulSoup(Read_MapleRanking, "html.parser")

    Maple_RankList = Maple_RankSoup.find(class_="n_rank_list")
    Maple_RankList = Maple_RankList.find_all("li")

    # 종합랭킹 [0]
    Maple_TotalRank = Maple_RankList[0].dl.find_all("dd")
    Maple_TotalRank = Maple_TotalRank[1].string.replace(" 위", "")

    # 월드랭킹 [1]
    Maple_WorldRank = Maple_RankList[1].dl.find_all("dd")
    Maple_WorldRank = Maple_WorldRank[1].string.replace(" 위", "")

    # 직업랭킹 [2]
    Maple_JobRank = Maple_RankList[2].dl.find_all("dd")
    Maple_JobRank = Maple_JobRank[1].string.replace(" 위", "")

    # 인기도랭킹 [3]
    Maple_PopularRank = Maple_RankList[3].dl.find_all("dd")
    Maple_PopularRank = Maple_PopularRank[1].string.replace(" 위", "")

    # 메이플 유니온 [4]
    try:
        Maple_UnionRank = Maple_RankList[4].dl.find_all("dd")
        Maple_UnionRank = Maple_UnionRank[1].string.replace(" 위", "")
    except:
        Maple_UnionRank = "0"

    # 업적랭킹 [5]
    Maple_AchievementsRank = Maple_RankList[5].dl.find_all("dd")
    Maple_AchievementsRank = Maple_AchievementsRank[1].string.replace(" 위", "")

    # 함수 리턴 값 정보
    # Maple_TotalRank = 종합랭킹 @
    # Maple_WorldRank = 월드랭킹 @
    # Maple_JobRank = 직업랭킹 @
    # Maple_PopularRank = 인기도랭킹 @
    # Maple_UnionRank = 메이플 유니온 랭킹 @
    # Maple_AchievementsRank = 업적랭킹 @
    return {"TotalRank": Maple_TotalRank, "WorldRank": Maple_WorldRank,
            "JobRank": Maple_JobRank, "PopularRank": Maple_PopularRank,
            "UnionRank": Maple_UnionRank, "AchievementsRank": Maple_AchievementsRank}

# 메이플스토리 정보검색 - 최종 호출 함수
def MapleIndexSearch(MapleName):
    # 함수 가져오기
    NexonMaple_def = NexonMaple(MapleName)
    MapleNormalData_def = MapleNormalData(MapleName)
    MapleRankingData_def = MapleRankingData(MapleName)

    # 메이플 유저 이름
    print("메이플 유저 이름 : " + MapleName)

    # 서버 아이콘 URL
    print("서버 아이콘 URL : " + NexonMaple_def["ServerIcon"])

    # 길드 명
    print("길드 명 : " + NexonMaple_def["GuildName"])

    # 레벨
    print("유저 레벨 : " + MapleNormalData_def["MapleLevel"])

    # 직업 정보
    print("직업 정보 : " + MapleNormalData_def["MapleJob"])

    # 서버 이름
    print("서버 이름 : " + MapleNormalData_def["MapleServer"])

    # 경험치
    print("경험치 : " + MapleNormalData_def["MapleEXP"])

    # 인기도
    print("인기도 : " + MapleNormalData_def["MaplePopular"])

    # 캐릭터 이미지 URL
    print("캐릭터 이미지 URL : " + MapleNormalData_def["MapleCharIMG_URL"])

    # 종합랭킹
    print("종합 랭킹 : " + MapleRankingData_def["TotalRank"])

    # 월드랭킹
    print("월드 랭킹 : " + MapleRankingData_def["WorldRank"])

    # 직업랭킹
    print("직업 랭킹 : " + MapleRankingData_def["JobRank"])

    # 인기도랭킹
    print("인기도 랭킹 : " + MapleRankingData_def["PopularRank"])

    # 메이플 유니온 랭킹
    print("메이플 유니온 랭킹 : " + MapleRankingData_def["UnionRank"])

    # 업적랭킹
    print("업적 랭킹 : " + MapleRankingData_def["AchievementsRank"])

    # 리턴 None
    return None

'''
MapleName = input("메이플스토리 닉네임을 적어주세요 : ")
try:
    MapleIndexSearch(MapleName)
except:
    print("메이플 유저 이름 : " + MapleName)
    print("해당 유저는 존재하지 않습니다.")
'''
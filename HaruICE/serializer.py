# 데이터 집합 중간 처리
from HaruICE.maple import *
from HaruICE.forms import *
from HaruICE.models import *

def MapleData(MapleName):
    try:
        NexonMaple_def = NexonMaple(MapleName)
        MapleNormalData_def = MapleNormalData(MapleName)
        MapleRankingData_def = MapleRankingData(MapleName)
        Validator_Maple = True

    except:
        NexonMaple_def = {
            "ServerIcon": 'X',
            "GuildName": 'X'
        }

        MapleNormalData_def = {
            "MapleLevel": 'X',
            "MapleJob": 'X',
            "MapleServer": 'X',
            "MapleEXP": 'X',
            "MaplePopular": 'X',
            "MapleCharIMG_URL": 'X',
        }

        MapleRankingData_def = {
            "TotalRank": 'X',
            "WorldRank": 'X',
            "JobRank": 'X',
            "PopularRank": 'X',
            "UnionRank": 'X',
            "AchievementsRank": 'X',
        }

        Validator_Maple = False

    Data = {
                'Validator_Maple': Validator_Maple,
                'form': MapleNameForm(),
                'MapleName': MapleName,
                'ServerIcon': NexonMaple_def['ServerIcon'],
                'GuildName': NexonMaple_def["GuildName"],
                'MapleLevel': MapleNormalData_def["MapleLevel"],
                'MapleJob': MapleNormalData_def["MapleJob"],
                'MapleServer': MapleNormalData_def["MapleServer"],
                'MapleEXP': MapleNormalData_def["MapleEXP"],
                'MaplePopular': MapleNormalData_def["MaplePopular"],
                'MapleCharIMG_URL': MapleNormalData_def["MapleCharIMG_URL"],
                'TotalRank': MapleRankingData_def["TotalRank"],
                'WorldRank': MapleRankingData_def["WorldRank"],
                'JobRank': MapleRankingData_def["JobRank"],
                'PopularRank': MapleRankingData_def["PopularRank"],
                'UnionRank': MapleRankingData_def["UnionRank"],
                'AchievementsRank': MapleRankingData_def["AchievementsRank"]
            }

    if Validator_Maple == True:
        # DB 저장
        MapleDB.object.create(
            MapleName = MapleName,
            ServerIconURL = NexonMaple_def['ServerIcon'],
            GuildName = NexonMaple_def["GuildName"],
            MapleLevel = MapleNormalData_def["MapleLevel"],
            MapleJob = MapleNormalData_def["MapleJob"],
            MapleServer = MapleNormalData_def["MapleServer"],
            MapleEXP = MapleNormalData_def["MapleEXP"],
            MaplePopular = MapleNormalData_def["MaplePopular"],
            MapleCharIMG_URL = MapleNormalData_def["MapleCharIMG_URL"],
            TotalRank = MapleRankingData_def["TotalRank"],
            WorldRank = MapleRankingData_def["WorldRank"],
            JobRank = MapleRankingData_def["JobRank"],
            PopularRank = MapleRankingData_def["PopularRank"],
            UnionRank = MapleRankingData_def["UnionRank"],
            AchievementsRank = MapleRankingData_def["AchievementsRank"]
        )
    
    elif Validator_Maple == False:
        # DB 저장 스킵
        pass

    else:
        # 넘기기
        pass

    try:
        MapleDB_Data = reversed(MapleDB.object.all())
        Data['MapleDB_Logs'] = MapleDB_Data
    except:
        pass

    return Data

def MapleData_GET():
    try:
        Data = {}
        MapleDB_Data = reversed(MapleDB.object.all())
        Data['MapleDB_Logs'] = MapleDB_Data
        Data['form'] = MapleNameForm()
    except:
        Data = {
            'form': MapleNameForm(),
            'MapleDB_Logs': 'None'
        }

    return Data
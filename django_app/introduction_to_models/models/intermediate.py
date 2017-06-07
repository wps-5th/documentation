from datetime import date, timezone, datetime
from django.db import models
from django.db.models import Q


class Player(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
        # current_club 프로퍼티에 현재 속하는 Club 리턴
        # current_tradeinfo 프로터피에 현재 자신의 TradeInfo 리턴

    @property
    def current_club(self):
        return self.current_tradeinfo.club


    @property
    def current_tradeinfo(self):
        return self.tradeinfo_set.get(date_leaved__isnull=True)


    # @property
    # def current_club(self):
    #     return self.club_set.get(tradeinfo__date_leaved__isnull=True).name
    #
    # # date_leaved=None 을 통해 최근 팀에서 뛰고 있는 선수들을 찾는다. (최근 정보를 원함으로 과거 이적현황을 알 필요 없다)
    # @property
    # def current_tradeinfo(self):
    #     player_info = TradeInfo.objects.get(
    #         player__name=self.id,
    #         date_leaved=None,
    #     )
    #     return '{} : {}', format(player_info.player, player_info.club)


class Club(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(
        Player,
        through='TradeInfo',
        through_fields=('club', 'player'),
    )

    def __str__(self):
        return self.name


    def squad(self, year=None):
        if year:
            return self.players.filter(
                Q(tradeinfo__date_joined__lt=datetime(year+1,1,1)) &
                (   Q(tradeinfo__date_leaved__gt=datetime(year,1,1))|
                    Q(tradeinfo__date_leaved__isnull=True)
                )
            )
        else:
            return self.players.filter(tradeinfo__date_leaved__isnull=True)

    # # club과 year를 매개변수로 받지만 year 값이 없다면 팀에 합류한 시점이 현재보다 이전인 그리고 이적을 가지 않은 상태의 선수를 본다.
    # # year 값이 주어진다면 해당 년도의 마지막 날까지 합류한 팀의 선수를 확인한다.
    # def squad(self, year=None):
    #     if year == None:
    #
    #         return TradeInfo.objects.filter(date_leaved__isnull=True, date_joined__lte=timezone.now())
    #     else:
    #         return TradeInfo.objects.filter(date_joined__gte=timezone.datetime(year, 12, 31)).name
    #         # squad 메서드에 현직 선수들만 리턴
    #         # 인수로 년도(2017, 2015 ...)을 받아 해당년도의 현직 선수들을 리턴
    #         # 주어지지 않으면 현재를 기준으로 함


class TradeInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)
    recommender = models.ForeignKey(Player, on_delete=models.PROTECT,null=True,blank=True,related_name='tradeinfo_set_by_recommender')
    prev_club = models.ForeignKey(Club, on_delete=models.PROTECT,null=True,blank=True,related_name='+')

    def __str__(self):
        return '{} : {} ({}~{})'.format(self.player, self.club, self.date_joined,self.date_leaved if self.date_leaved else '현직')
    ### self.date_leaved or '현직' : 참인값을 반환


    @property
    def is_current(self):
        return self.date_leaved is None
    ### return not self.date_leaved

    # prev_club = models.ForeignKey(
    #     Club,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    #
    # recommender = models.ForeignKey(
    #     Player,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    #
    # def __str__(self):
    #     return '{} {} {} {} {}'.format(self.player, self.club, self.date_joined, self.date_leaved, self.prev_club)

        # property 로 is_current 속성이 TradeInfo가 현재 현직(leave 하지 않았는지) 여부 반환
        # recommender와 prev_club을 활성화시키고 Club의 MTM필드에 through_fields를 명시

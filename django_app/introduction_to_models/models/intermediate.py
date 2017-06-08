from datetime import date, timezone, datetime
from django.db import models
from django.db.models import Q


class Player(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    @property
    def current_club(self):
        return self.current_tradeinfo.club

    @property
    def current_tradeinfo(self):
        return self.tradeinfo_set.get(date_leaved__isnull=True)


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
                Q(tradeinfo__date_joined__lt=datetime(year + 1, 1, 1)) &
                (Q(tradeinfo__date_leaved__gt=datetime(year, 1, 1)) |
                 Q(tradeinfo__date_leaved__isnull=True)
                 )
            )
        else:
            return self.players.filter(tradeinfo__date_leaved__isnull=True)


class TradeInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    date_joined = models.DateField()
    date_leaved = models.DateField(null=True, blank=True)
    recommender = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, blank=True,
                                    related_name='tradeinfo_set_by_recommender')
    prev_club = models.ForeignKey(Club, on_delete=models.PROTECT, null=True, blank=True, related_name='+')

    def __str__(self):
        return '{} : {} ({}~{})'.format(self.player, self.club, self.date_joined,
                                        self.date_leaved if self.date_leaved else '현직')

    ### self.date_leaved or '현직' : 참인값을 반환


    @property
    def is_current(self):
        return self.date_leaved is None
        ### return not self.date_leaved

from datetime import date
from django.test import TestCase

# Create your tests here.
from introduction_to_models.models import Player, Club, TradeInfo


class Inter(TestCase):
    def test_inter(self):
        a = Player.objects.create(name='bale')
        # c = Player.objects.create(name='nnn')
        b = Club.objects.create(name='tottenham')
        TradeInfo.objects.create(player=a, club=b, date_joined=date(2000, 3, 3))
        # TradeInfo.objects.create(player=c, club=b, date_joined=date(2000,3,3), date_leaved=date(2010,1,1))
        self.assertEqual(a.current_club,'tottenham')
        # self.assertEqual(c.current_club,'tottenham')
        self.assertEqual(a.current_tradeinfo,'tottenham')
        # self.assertEqual(c.current_tradeinfo)
